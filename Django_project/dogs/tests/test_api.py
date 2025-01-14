from django.db.models import Subquery, OuterRef, Avg, Count
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dogs.models import Dog, Breed
from dogs.serializers import DogListSerializer, DogDetailSerializer, BreedSerializer


class DogsApiTestCase(APITestCase):
    def setUp(self):
        self.breed_1 = Breed.objects.create(name="breed1", size="Small", friendliness=1, trainability=2,
                                            shedding_amount=3, exercise_needs=4)
        self.breed_2 = Breed.objects.create(name="breed2", size="Medium", friendliness=5, trainability=4,
                                            shedding_amount=3, exercise_needs=2)
        self.dog_1 = Dog.objects.create(name="dog1", age=1, breed=self.breed_1, gender="Male", color="white",
                                        favorite_food="bone", favorite_toy="ball")
        self.dog_2 = Dog.objects.create(name="dog2", age=2, breed=self.breed_2, gender="Female", color="black",
                                        favorite_food="bone", favorite_toy="ball")
        self.dog_3 = Dog.objects.create(name="dog3", age=4, breed=self.breed_2, gender="Female", color="black",
                                        favorite_food="bone", favorite_toy="ball")

    def test_get_list_dogs(self):
        url = reverse("dog-list")
        response = self.client.get(url)
        dogs = Dog.objects.all().annotate(
            avg_breed_age=Subquery(
                Dog.objects.filter(breed=OuterRef('breed'))
                .values('breed')
                .annotate(avg_age=Avg('age'))
                .values('avg_age')
            )
        )
        serializer_data = DogListSerializer(dogs, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[2]['avg_breed_age'], "3.00")

    def test_get_detail_dog(self):
        url = reverse("dog-detail", args=[self.dog_1.id])
        response = self.client.get(url)
        dog = Dog.objects.annotate(
            same_breed_count=Count('breed__dogs'),
        ).get(id=self.dog_1.id)
        serializer_data = DogDetailSerializer(dog, many=False).data
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data)

    def test_create_dog(self):
        self.assertEqual(Dog.objects.all().count(), 3)
        url = reverse("dog-list")
        data = {
            "name": "dog4",
            "age": 5,
            "breed": self.breed_1.id,
            "gender": "Male",
            "color": "white",
            "favorite_food": "bone",
            "favorite_toy": "ball"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dog.objects.count(), 4)

    def test_update_dog(self):
        url = reverse("dog-detail", args=[self.dog_1.id])
        data = {
            "name": "dog1",
            "age": 10,
            "breed": self.breed_1.id,
            "gender": "Female",
            "color": "Red",
            "favorite_food": "bone",
            "favorite_toy": "ball"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dog_1.refresh_from_db()
        self.assertEqual(self.dog_1.name, data["name"])
        self.assertEqual(self.dog_1.age, data["age"])
        self.assertEqual(self.dog_1.breed.id, data["breed"])
        self.assertEqual(self.dog_1.gender, data["gender"])
        self.assertEqual(self.dog_1.color, data["color"])
        self.assertEqual(self.dog_1.favorite_food, data["favorite_food"])

    def test_delete_dog(self):
        url = reverse("dog-detail", args=[self.dog_1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dog.objects.count(), 2)


class BreedApiTestCase(APITestCase):
    def setUp(self):
        self.breed_1 = Breed.objects.create(name="breed1", size="Small", friendliness=1, trainability=2,
                                            shedding_amount=3, exercise_needs=4)
        self.breed_2 = Breed.objects.create(name="breed2", size="Medium", friendliness=5, trainability=4,
                                            shedding_amount=3, exercise_needs=2)
        self.dog_1 = Dog.objects.create(name="dog1", age=1, breed=self.breed_1, gender="Male", color="white",
                                        favorite_food="bone", favorite_toy="ball")
        self.dog_2 = Dog.objects.create(name="dog2", age=2, breed=self.breed_2, gender="Female", color="black",
                                        favorite_food="bone", favorite_toy="ball")
        self.dog_3 = Dog.objects.create(name="dog3", age=4, breed=self.breed_2, gender="Female", color="black",
                                        favorite_food="bone", favorite_toy="ball")

    def test_get_list_breeds(self):
        url = reverse("breed-list")
        response = self.client.get(url)
        breeds = Breed.objects.all().annotate(dogs_count=Count('dogs'))
        serializer_data = BreedSerializer(breeds, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['dogs_count'], 1)
        self.assertEqual(serializer_data[1]['dogs_count'], 2)

    def test_create_breed(self):
        self.assertEqual(Breed.objects.all().count(), 2)
        url = reverse("breed-list")
        data = {
            "name": "breed3",
            "size": "Small",
            "friendliness": 1,
            "trainability": 2,
            "shedding_amount": 3,
            "exercise_needs": 4
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Breed.objects.count(), 3)

    def test_update_breed(self):
        url = reverse("breed-detail", args=[self.breed_1.id])
        data = {
            "name": "Updated name breed1",
            "size": "Small",
            "friendliness": 1,
            "trainability": 2,
            "shedding_amount": 3,
            "exercise_needs": 4
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.breed_1.refresh_from_db()
        self.assertEqual(self.breed_1.name, data["name"])
        self.assertEqual(self.breed_1.size, data["size"])
        self.assertEqual(self.breed_1.friendliness, data["friendliness"])

    def test_delete_breed(self):
        url = reverse("breed-detail", args=[self.breed_1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Breed.objects.all().count(), 1)