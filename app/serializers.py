from rest_framework import serializers
from .models import Box


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = '__all__'


class CreateBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('length', 'breadth', 'height')


class UpdateBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('length', 'breadth', 'height')
