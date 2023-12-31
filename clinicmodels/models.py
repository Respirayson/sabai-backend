from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Patient(models.Model):
    class Meta:
        db_table = "patients"

    village_prefix = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    local_name = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=255)
    gender = models.CharField(max_length=6)
    travelling_time_to_village = models.IntegerField(default=0)
    date_of_birth = models.DateField(default=timezone.now)
    drug_allergy = models.TextField(default="None")
    parent = models.IntegerField(blank=True, null=True)
    face_encodings = models.CharField(max_length=3000, blank=True, null=True)
    picture = CloudinaryField('image')


class Fingerprint(models.Model):
    class Meta:
        db_table = "fingerprints"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fg_value = models.BinaryField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    fg_image = models.BinaryField(blank=True, null=True)


class Visit(models.Model):
    class Meta:
        db_table = "visits"

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100)


class Vitals(models.Model):
    class Meta:
        db_table = "vitals"

    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, blank=True, null=True)
    height = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    weight = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    systolic = models.IntegerField(default=0)
    diastolic = models.IntegerField(default=0)
    temperature = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    hiv_positive = models.BooleanField(default=False)
    ptb_positive = models.BooleanField(default=False)
    hepc_positive = models.BooleanField(default=False)
    diabetes_mellitus = models.TextField(blank=True, null=True, default="Haven't Asked / Not Applicable")
    heart_rate = models.IntegerField(default=0)
    urine_test = models.TextField(blank=True, null=True)
    hemocue_count = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    blood_glucose = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    left_eye_degree = models.TextField(blank=True, null=True)
    right_eye_degree = models.TextField(blank=True, null=True)
    left_eye_pinhole = models.TextField(blank=True, null=True)
    right_eye_pinhole = models.TextField(blank=True, null=True)
    eye_pressure = models.TextField(blank=True, null=True)
    cataracts = models.TextField(blank=True, null=True)
    others = models.TextField(blank=True, null=True)


class PostReferral(models.Model):
    class Meta:
        db_table = "postreferrals"

    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    recorder = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)


class Consult(models.Model):
    class Meta:
        db_table = "consults"

    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    doctor = models.ForeignKey(
        User,
        related_name="doctor_create",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    problems = models.TextField(blank=True, null=True)
    referrals = models.TextField(blank=True, null=True)
    chronic_referral = models.BooleanField(blank=True, null=True)
    addendum = models.TextField(blank=True, null=True)
    addendum_doctor = models.ForeignKey(
        User,
        related_name="doctor_addendum",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    addendum_time = models.DateTimeField(blank=True, null=True)


class Medication(models.Model):
    class Meta:
        db_table = "medication"

    medicine_name = models.CharField(max_length=255)
    reserve_quantity = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)


class Order(models.Model):
    class Meta:
        db_table = "order"

    medicine = models.ForeignKey(
        Medication, on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.IntegerField(default=0, blank=True)
    consult = models.ForeignKey(
        Consult, on_delete=models.SET_NULL, blank=True, null=True
    )
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    order_status = models.CharField(max_length=255)
