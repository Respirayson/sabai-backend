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
from visit.api import VisitView
from login.api import LoginView
from signup.api import SignUpView
from user.api import UserView
from consult import api as consult
from patient.api import PatientView
from postreferral import api as postreferral
from medication.api import MedicationView
from order.api import OrderView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin', admin.site.urls),
    path('login', LoginView.as_view()),
    path('signup', SignUpView.as_view(), name='signup_list'),
    path('users', UserView.as_view(), name='users_list'),
    path('users/<int:pk>', UserView.as_view(), name='user_detail'),


    # JWT Token Endpoints
    path('api/token', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    # Patient Endpoints
    path('patients', PatientView.as_view(), name='patients_list'),
    path('patients/<int:pk>', PatientView.as_view(), name='patient_detail'),

    # Visit Endpoints
    path('visits', VisitView.as_view(), name='visits_list'),
    path('visits/<int:pk>', VisitView.as_view(), name='visit_detail'),


    # Vitals Endpoints
    path('vitals/new', vitals.create_new_vitals, name='create_vitals'),
    path('vitals/update_by_id', vitals.update_vitals, name='update_vitals_by_id'),
    path('vitals/by_id', vitals.get_vitals_by_id, name='get_vitals_by_id'),
    path('vitals/by_visit', vitals.get_vitals_by_visit,
         name='get_vitals_by_visit'),
    path('vitals/by_patient', vitals.get_vitals_by_patient,
         name='get_vitals_by_patient'),

    # Postreferral Endpoints
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

    # Consult Endpoints
    path('consulttype/all', consult.get_all_consult_types,
         name='get_all_consult_types'),
    path('consulttype/new', consult.create_new_consult_type,
         name='create_new_consult_type'),
    path('consult/new', consult.create_new_consult, name='create_new_consult'),

    # Medication Creation/Retrieval Endpoints
    path('medications', MedicationView.as_view(), name='medications_list'),
    path('medications/<int:pk>', MedicationView.as_view(),
         name='medication_detail'),


    # Order Creation/Retrieval Endpoints
    path('orders', OrderView.as_view(), name='orders_list'),
    path('orders/<int:pk>', OrderView.as_view(), name='order_detail'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
