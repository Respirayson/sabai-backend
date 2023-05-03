from rest_framework import serializers
from clinicmodels.models import Order
from .medication_serializer import MedicationSerializer
from .visit_serializer import VisitSerializer


class OrderSerializer(serializers.ModelSerializer):
    medicine = MedicationSerializer()
    visit = VisitSerializer()

    class Meta:
        model = Order
        fields = "__all__"
