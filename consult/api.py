from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import ConsultType, Visit
from consult.forms import ConsultForm


@api_view(['GET'])
def get_all_consult_types(request):
    try:
        consulttypes = ConsultType.objects.all()
        if consulttypes.count() == 0:
            return JsonResponse({"message": "ConsultType matching query does not exist"}, status=404)
        response = serializers.serialize("json", consulttypes)
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['POST'])
def create_new_consult_type(request):
    try:
        if 'consult_type' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'consult_type' not found"}, status=400)
        consult_type_field = request.POST['consult_type']
        consulttype = ConsultType(type=consult_type_field)
        consulttype.save()
        response = serializers.serialize("json", [consulttype, ])
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['POST'])
@csrf_exempt
def create_new_consult(request):
    try:
        if 'visit' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'visit' not found"}, status=400)
        if 'doctor' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'doctor' not found"}, status=400)
        if 'consult_type' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'consult_type' not found"}, status=400)
        visit_id = request.POST['visit']
        doctor_id = request.POST['doctor']
        consult_type_name = request.POST['consult_type']
        Visit.objects.get(pk=visit_id)
        User.objects.get(pk=doctor_id)
        consult_type = ConsultType.objects.get(type=consult_type_name)

        consult_form = ConsultForm(request.POST)
        consult_form.consult_type = consult_type
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
