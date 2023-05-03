import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


from clinicmodels.models import Vitals
from vitals.forms import VitalsForm
from sabaibiometrics.serializers.vitals_serializer import VitalsSerializer


class VitalsView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            visit = request.GET.get('visit', '')
            vitals = Vitals.objects.all()
            if visit:
                vitals = vitals.filter(visit=visit)
            serializer = VitalsSerializer(vitals, many=True)
            return HttpResponse(json.dumps(serializer.data), content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            vitals = Vitals.objects.get(pk=pk)
            serializer = VitalsSerializer(vitals)
            return HttpResponse(json.dumps(serializer.data), content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def post(self, request):
        '''
        POST request with multipart form to create a new vitals
        :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
        :return: Http Response with corresponding status code
        '''
        try:
            data = json.loads(request.body) or None
            form = VitalsForm(data)
            if form.is_valid():
                vitals = form.save()
                serializer = VitalsSerializer(vitals)
                return HttpResponse(json.dumps(serializer.data), content_type="application/json")
            else:
                return JsonResponse(form.errors, status=400)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def put(self, request, pk):
        '''
        Update vitals data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        '''
        try:
            vitals = Vitals.objects.get(pk=pk)
            form = VitalsForm(json.loads(request.body)
                              or None, instance=vitals)
            if form.is_valid():
                vitals = form.save()
                serializer = VitalsSerializer(vitals)
                return HttpResponse(json.dumps(serializer.data), content_type="application/json")

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
            vitals = Vitals.objects.get(pk=pk)
            vitals.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
