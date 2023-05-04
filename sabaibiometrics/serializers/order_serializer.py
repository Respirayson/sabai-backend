from rest_framework import serializers
from clinicmodels.models import Order
from .medication_serializer import MedicationSerializer


class OrderSerializer(serializers.ModelSerializer):
    medicine = MedicationSerializer()

    class Meta:
        model = Order
        fields = "__all__"
