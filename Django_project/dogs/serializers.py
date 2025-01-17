from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from dogs.models import Dog, Breed


class DogSerializer(ModelSerializer):
    class Meta:
        model = Dog
        fields = "__all__"


class DogListSerializer(DogSerializer):
    avg_breed_age = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )


class DogDetailSerializer(DogSerializer):
    same_breed_count = serializers.IntegerField(read_only=True)


class BreedSerializer(ModelSerializer):
    dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = "__all__"
