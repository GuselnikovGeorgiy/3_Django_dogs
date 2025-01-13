from django.db.models import Avg, Count, Subquery, OuterRef
from rest_framework.viewsets import ModelViewSet

from dogs.models import Dog, Breed
from dogs.serializers import DogListSerializer, DogDetailSerializer, BreedSerializer


class DogViewSet(ModelViewSet):
    queryset = Dog.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            return Dog.objects.all().annotate(
                avg_breed_age=Subquery(
                    Dog.objects.filter(breed=OuterRef('breed'))
                    .values('breed')
                    .annotate(avg_age=Avg('age'))
                    .values('avg_age')
                )
            )
        elif self.action == 'retrieve':
            return Dog.objects.all().annotate(
                same_breed_count=Count('breed__dogs'),
            )
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            return DogListSerializer
        elif self.action == 'retrieve':
            return DogDetailSerializer
        return super().get_serializer_class()


class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all().annotate(
        dogs_count=Count('dogs')
    )
    serializer_class = BreedSerializer
