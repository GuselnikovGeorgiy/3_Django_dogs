from django.test import TestCase

from dogs.models import Dog, Breed
from dogs.serializers import DogListSerializer, BreedSerializer


class BreedSerializerTestCase(TestCase):
    def test_breed_serializer(self):
        breed_1 = Breed.objects.create(
            name="breed1",
            size="Small",
            friendliness=1,
            trainability=2,
            shedding_amount=3,
            exercise_needs=4,
        )
        breed_2 = Breed.objects.create(
            name="breed2",
            size="Medium",
            friendliness=5,
            trainability=4,
            shedding_amount=3,
            exercise_needs=2,
        )
        data = BreedSerializer([breed_1, breed_2], many=True).data
        expected_data = [
            {
                "id": breed_1.id,
                "name": "breed1",
                "size": "Small",
                "friendliness": 1,
                "trainability": 2,
                "shedding_amount": 3,
                "exercise_needs": 4,
            },
            {
                "id": breed_2.id,
                "name": "breed2",
                "size": "Medium",
                "friendliness": 5,
                "trainability": 4,
                "shedding_amount": 3,
                "exercise_needs": 2,
            },
        ]
        self.assertEqual(expected_data, data)


class DogSerializerTestCase(TestCase):
    def test_dog_serializer(self):
        breed_1 = Breed.objects.create(
            name="breed1",
            size="Small",
            friendliness=1,
            trainability=2,
            shedding_amount=3,
            exercise_needs=4,
        )
        breed_2 = Breed.objects.create(
            name="breed2",
            size="Medium",
            friendliness=5,
            trainability=4,
            shedding_amount=3,
            exercise_needs=2,
        )
        dog_1 = Dog.objects.create(
            name="dog1",
            age=1,
            breed=breed_1,
            gender="Male",
            color="white",
            favorite_food="bone",
            favorite_toy="ball",
        )
        dog_2 = Dog.objects.create(
            name="dog2",
            age=2,
            breed=breed_2,
            gender="Female",
            color="black",
            favorite_food="bone",
            favorite_toy="ball",
        )
        data = DogListSerializer([dog_1, dog_2], many=True).data
        expected_data = [
            {
                "id": dog_1.id,
                "name": "dog1",
                "age": 1,
                "gender": "Male",
                "color": "white",
                "favorite_food": "bone",
                "favorite_toy": "ball",
                "breed": breed_1.id,
            },
            {
                "id": dog_2.id,
                "name": "dog2",
                "age": 2,
                "gender": "Female",
                "color": "black",
                "favorite_food": "bone",
                "favorite_toy": "ball",
                "breed": breed_2.id,
            },
        ]
        self.assertEqual(expected_data, data)
