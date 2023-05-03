import json
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from clinicmodels.models import Visit, Consult
from consult.forms import ConsultForm


class ConsultView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            consults = Consult.objects.all()

            response = serializers.serialize("json", consults)
            return HttpResponse(response, content_type='application/json')
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            consult = Consult.objects.get(pk=pk)
            response = serializers.serialize("json", [consult])
            return HttpResponse(response, content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def post(self, request):
        '''
        POST request with multipart form to create a new consult
        :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
        :return: Http Response with corresponding status code
        '''
        try:
            data = json.loads(request.body) or None
            if 'visit' not in data:
                return JsonResponse({"message": "POST: parameter 'visit' not found"}, status=400)
            if 'doctor' not in data:
                return JsonResponse({"message": "POST: parameter 'doctor' not found"}, status=400)
            visit_id = data['visit']
            doctor_id = data['doctor']
            Visit.objects.get(pk=visit_id)
            User.objects.get(pk=doctor_id)

            consult_form = ConsultForm(data)
            if consult_form.is_valid():
                consult = consult_form.save()
                response = serializers.serialize("json", [consult, ])
                return HttpResponse(response, content_type='application/json')
            else:
                return JsonResponse({"message": consult_form.errors}, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def put(self, request, pk):
        '''
        Update consult data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        '''
        try:
            consult = Consult.objects.get(pk=pk)
            form = ConsultForm(json.loads(request.body)
                               or None, instance=consult)
            if form.is_valid():
                consult = form.save()
                response = serializers.serialize("json", [consult, ])
                return HttpResponse(response, content_type="application/json")

            else:
                return JsonResponse(form.errors, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            consult = Consult.objects.get(pk=pk)
            consult.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)


# @api_view(['GET'])
# def get_all_consult_types(request):
#     try:
#         consulttypes = ConsultType.objects.all()
#         if consulttypes.count() == 0:
#             return JsonResponse({"message": "ConsultType matching query does not exist"}, status=404)
#         response = serializers.serialize("json", consulttypes)
#         return HttpResponse(response, content_type='application/json')
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except DataError as e:
#         return JsonResponse({"message": str(e)}, status=400)


# @api_view(['POST'])
# def create_new_consult_type(request):
#     try:
#         if 'consult_type' not in request.POST:
#             return JsonResponse({"message": "POST: parameter 'consult_type' not found"}, status=400)
#         consult_type_field = request.POST['consult_type']
#         consulttype = ConsultType(type=consult_type_field)
#         consulttype.save()
#         response = serializers.serialize("json", [consulttype, ])
#         return HttpResponse(response, content_type='application/json')
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except DataError as e:
#         return JsonResponse({"message": str(e)}, status=400)
