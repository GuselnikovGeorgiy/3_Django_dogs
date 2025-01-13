from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from dogs.models import Dog, Breed


class DogListSerializer(ModelSerializer):
    avg_breed_age = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True) # all dogs

    class Meta:
        model = Dog
        fields = "__all__"


class DogDetailSerializer(ModelSerializer):
    same_breed_count = serializers.IntegerField(read_only=True)  # one dog

    class Meta:
        model = Dog
        fields = "__all__"


class BreedSerializer(ModelSerializer):
    dogs_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Breed
        fields = "__all__"
