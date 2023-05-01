import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import Patient, Visit, VisitConsult, ConsultType
from visit.forms import VisitForm
from rest_framework.views import APIView


class VisitView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            status = request.GET.get('status', '')
            patient = request.GET.get('patient', '')

            visits = Visit.objects.all()
            if status:
                visits = visits.filter(status=status)
            if patient:
                visits = visits.filter(patient=patient)
            response = serializers.serialize("json", visits)
            return HttpResponse(response, content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            visit = Visit.objects.get(pk=pk)
            response = serializers.serialize("json", [visit])
            return HttpResponse(response, content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def post(self, request):
        '''
        POST request with multipart form to create a new visit
        :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
        :return: Http Response with corresponding status code
        '''
        try:
            form = VisitForm(json.loads(request.body)
                             or None)
            if form.is_valid():
                visit = form.save(commit=False)
                visit.save()
                response = serializers.serialize("json", [visit, ])
                return HttpResponse(response, content_type="application/json")
            else:
                return JsonResponse(form.errors, status=400)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def put(self, request, pk):
        '''
        Update visit data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        '''
        try:
            visit = Visit.objects.get(pk=pk)
            form = VisitForm(json.loads(request.body)
                             or None, instance=visit)
            if form.is_valid():
                visit = form.save()
                response = serializers.serialize("json", [visit, ])
                return HttpResponse(response, content_type="application/json")

            else:
                return JsonResponse(form.errors, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=404)

    def delete(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
            visit.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
