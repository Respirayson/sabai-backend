import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from clinicmodels.models import Patient
from patient.forms import PatientForm
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView

"""
Handles all operations regarding the retrieval, update of patient models.
"""


class PatientView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            patient_name = request.GET.get('name', '')

            patients = Patient.objects.all()

            if (patient_name):
                patients = patients.filter(name__icontains=patient_name)
            response = serializers.serialize("json", patients)
            return HttpResponse(response, content_type='application/json')
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            response = serializers.serialize("json", [patient])
            return HttpResponse(response, content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def post(self, request):
        '''
        POST request with multipart form to create a new patient
        :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
        :return: Http Response with corresponding status code
        '''
        try:
            form = PatientForm(request.POST, request.FILES)
            print(form)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.save()
                response = serializers.serialize("json", [patient, ])
                return HttpResponse(response, content_type="application/json")
            else:
                return JsonResponse(form.errors, status=400)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def put(self, request, pk):
        '''
        Update patient data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        '''
        try:
            patient = Patient.objects.get(pk=pk)
            form = PatientForm(json.loads(request.body)
                               or None, instance=patient)
            if form.is_valid():
                patient = form.save()
                response = serializers.serialize("json", [patient, ])
                return HttpResponse(response, content_type="application/json")

            else:
                return JsonResponse(form.errors, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            patient.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)

# @api_view(['GET'])
# def get_patient_image_by_id(request):
#     '''
#     GET image of patient by id
#     :param request: GET with parameter id of patient you want the image of
#     :return: FileResponse if image is found, 404 if not
#     '''
#     try:
#         if 'id' not in request.GET:
#             return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
#         patient_id = request.GET['id']
#         patient = Patient.objects.get(pk=patient_id)
#         image = patient.picture
#         if "jpeg" in image.name.lower() or "jpg" in image.name.lower():
#             return HttpResponse(image.file.read(), content_type="image/jpeg")
#         elif "png" in image.name.lower():
#             return HttpResponse(image.file.read(), content_type="image/png")
#         else:
#             return JsonResponse({"message": "Patient image is in the wrong format"}, status=400)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({"message": str(e)}, status=404)
#     except ValueError as e:
#         return JsonResponse({"message": str(e)}, status=400)


# @api_view(['POST'])
