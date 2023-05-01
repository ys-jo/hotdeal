# 장고형식을 json형태로 보내주는 역할을 함

from rest_framework import serializers
from .models import Deal

class DealSerializers(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ('__all__')