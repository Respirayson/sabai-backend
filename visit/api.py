from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import Patient, Visit, VisitConsult, ConsultType
from visit.forms import VisitForm


@api_view(['POST'])
@csrf_exempt
def create_new_visit(request):
    try:
        print(request.POST)
        required_consults = request.POST.getlist('consult_required')
        if 'patient' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'patient' not found"}, status=400)
        patient_id = request.POST['patient']
        print(required_consults)

        # Patient exists, go on to create a new visit
        Patient.objects.get(pk=patient_id)

        visit_form = VisitForm(request.POST)
        if visit_form.is_valid():
            visit = visit_form.save()

            if required_consults is not None:
                print("size: ", len(required_consults))
                for consult in required_consults:
                    consult_type = ConsultType.objects.get(type=consult)
                    visitconsult = VisitConsult(visit=visit, consult_type=consult_type)
                    visitconsult.save()
            else:
                consult_type = ConsultType.objects.all()[0]
                visitconsult = VisitConsult(visit=visit, consult_type=consult_type)
                visitconsult.save()
            response = serializers.serialize("json", [visit, ])
            return HttpResponse(response, content_type='application/json')
        else:
            return JsonResponse(visit_form.errors, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)


@api_view(['POST'])
@csrf_exempt
def update_visit(request):
    try:
        if 'id' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'id' not found"}, status=400)
        visit_id = request.POST['id']
        visit = Visit.objects.get(pk=visit_id)
        if 'status' in request.POST:
            visit.status = request.POST['status']
        visit.save()
        response = serializers.serialize("json", [visit, ])
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=404)


@api_view(['GET'])
def get_visit_by_id(request):
    try:
        if 'id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
        visit_id = request.GET['id']
        visit = Visit.objects.get(pk=visit_id)
        response = serializers.serialize("json", [visit, ])
        return HttpResponse(response, content_type="application/json")
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_visit_by_patient(request):
    try:
        if 'patient_id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'patient_id' not found"}, status=400)
        patient_id = request.GET['patient_id']
        visits = Visit.objects.filter(patient=patient_id)
        if visits.count() == 0:
            return JsonResponse({"message": "Visit matching query does not exist"}, status=404)
        response = serializers.serialize("json", visits)
        return HttpResponse(response, content_type="application/json")
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_visit_by_status(request):
    try:
        if 'status' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'status' not found"}, status=400)
        status = request.GET['status']
        visits = Visit.objects.filter(status=status)
        if visits.count() == 0:
            return JsonResponse({"message": "Visit matching query does not exist"}, status=404)
        response = serializers.serialize("json", visits)
        return HttpResponse(response, content_type="application/json")
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_visit_by_patient_and_status(request):
    try:
        if 'status' not in request.GET and 'patient' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'status' or 'patient' not found"}, status=400)
        status = request.GET['status']
        patient = request.GET['patient']
        visit = Visit.objects.filter(status=status, patient=patient)
        if visit.count() == 0:
            return JsonResponse({"message": "Visit matching query does not exist"}, status=404)
        response = serializers.serialize("json", visit)
        return HttpResponse(response, content_type="application/json")
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)
