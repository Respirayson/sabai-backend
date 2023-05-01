"""sabaibiometrics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from vitals import api as vitals
from visit import api as visit
from login import api as login
from consult import api as consult
from patient.api import PatientView
from postreferral import api as postreferral
from medication.api import MedicationView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login.HelloView.as_view()),

    # JWT Token Endpoints
    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    # Patient Creation/Retrieval Endpoints
    path('patients', PatientView.as_view(), name='patients_list'),
    path('patients/<int:pk>', PatientView.as_view(), name='patients_detail'),

    # Visit Creation/Retrieval Endpoints
    path('visit/new', visit.create_new_visit, name='create_visit'),
    path('visit/update_by_id', visit.update_visit, name='update_visit_by_id'),
    path('visit/by_id', visit.get_visit_by_id, name='get_visit_by_id'),
    path('visit/by_patient', visit.get_visit_by_patient,
         name='get_visit_by_patient'),
    path('visit/by_status', visit.get_visit_by_status, name='get_visit_by_status'),
    path('visit/by_patient_and_status', visit.get_visit_by_patient_and_status,
         name='get_visit_by_patient_and_status'),

    # Vitals Creation/Retrieval Endpoints
    path('vitals/new', vitals.create_new_vitals, name='create_vitals'),
    path('vitals/update_by_id', vitals.update_vitals, name='update_vitals_by_id'),
    path('vitals/by_id', vitals.get_vitals_by_id, name='get_vitals_by_id'),
    path('vitals/by_visit', vitals.get_vitals_by_visit,
         name='get_vitals_by_visit'),
    path('vitals/by_patient', vitals.get_vitals_by_patient,
         name='get_vitals_by_patient'),

    # Postreferral Creation/Retrieval Endpoints
    path('postreferral/new', postreferral.create_new_postreferral,
         name='create_postreferral'),
    path('postreferral/update_by_id', postreferral.update_postreferral,
         name='update_postreferral_by_id'),
    path('postreferral/by_id', postreferral.get_postreferral_by_id,
         name='get_postreferral_by_id'),
    path('postreferral/by_visit', postreferral.get_postreferral_by_visit,
         name='get_postreferral_by_visit'),
    path('postreferral/by_patient', postreferral.get_postreferral_by_patient,
         name='get_postreferral_by_patient'),

    # Consult Creation/Retrieval Endpoints
    path('consulttype/all', consult.get_all_consult_types,
         name='get_all_consult_types'),
    path('consulttype/new', consult.create_new_consult_type,
         name='create_new_consult_type'),
    path('consult/new', consult.create_new_consult, name='create_new_consult'),

    # Medication Creation/Retrieval Endpoints
    path('medications', MedicationView.as_view(), name='medications_list'),
    path('medications/<int:pk>', MedicationView.as_view(), name='medications_detail'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
