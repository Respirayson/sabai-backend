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

"""
Handles all operations regarding the retrieval, update of patient models.
"""


@api_view(['GET'])
def get_all_patients(request):
    patients = Patient.objects.all()
    response = serializers.serialize("json", patients)
    return HttpResponse(response, content_type="application/json")


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def get_patient_by_name(request):
    """
    GET patient by name
    :param request: GET request with a name parameter
    :return: JSON Response with an array of users matching name
    """
    try:
        # user = User.objects.get(username=request.user)
        # print(user.email)
        if 'name' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'name' not found"}, status=400)
        patient_name = request.GET['name']
        patient = Patient.objects.filter(name__contains=patient_name)
        if patient.count() == 0:
            return JsonResponse({"message": "Patient matching query does not exist"}, status=404)
        response = serializers.serialize("json", patient)
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_patient_by_id(request):
    '''
    GET patient identified by id
    :param request: GET request with an id parameter
    :return: JSON Response with an array of users mathing id
    '''

    try:
        if 'id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
        patient_id = request.GET['id']
        patient = Patient.objects.filter(id=patient_id)
        response = serializers.serialize("json", patient)
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_patient_image_by_id(request):
    '''
    GET image of patient by id
    :param request: GET with parameter id of patient you want the image of
    :return: FileResponse if image is found, 404 if not
    '''
    try:
        if 'id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
        patient_id = request.GET['id']
        patient = Patient.objects.get(pk=patient_id)
        image = patient.picture
        if "jpeg" in image.name.lower() or "jpg" in image.name.lower():
            return HttpResponse(image.file.read(), content_type="image/jpeg")
        elif "png" in image.name.lower():
            return HttpResponse(image.file.read(), content_type="image/png")
        else:
            return JsonResponse({"message": "Patient image is in the wrong format"}, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['POST'])
@csrf_exempt
def create_new_patient(request):
    '''
    POST request with multipart form to create a new patient
    :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
    :return: Http Response with corresponding status code
    '''
    try:
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
            response = serializers.serialize("json", [patient, ])
            return HttpResponse(response, content_type="application/json")
        else:
            return JsonResponse(form.errors, status=400)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['POST'])
@csrf_exempt
def update_patient(request):
    '''
    Update patient data based on the parameters
    :param request: POST with data
    :return: JSON Response with new data, or error
    '''
    if 'id' not in request.POST:
        return JsonResponse({"message": "POST: parameter 'id' not found"}, status=400)
    patient_id = request.POST['id']
    try:
        patient = Patient.objects.get(pk=patient_id)
        if 'village_prefix' in request.POST:
            patient.village_prefix = request.POST['village_prefix']
        if 'name' in request.POST:
            patient.name = request.POST['name']
        if 'contact_no' in request.POST:
            patient.contact_no = request.POST['contact_no']
        if 'gender' in request.POST:
            patient.gender = request.POST['gender']
        if 'travelling_time_to_village' in request.POST:
            patient.travelling_time_to_village = request.POST['travelling_time_to_village']
        if 'date_of_birth' in request.POST['date_of_birth']:
            patient.date_of_birth = request.POST['date_of_birth']
        if 'drug_allergy' in request.POST:
            patient.drug_allergy = request.POST['drug_allergy']
        if 'parent' in request.POST:
            patient.parent = request.POST['parent']
        if 'face_encodings' in request.POST:
            patient.face_encodings = request.POST['face_encodings']
        if 'picture' in request.FILES:
            patient.picture = request.FILES['picture']
        patient.save()
        response = serializers.serialize("json", [patient, ])
        return HttpResponse(response, content_type="application/json")
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)
