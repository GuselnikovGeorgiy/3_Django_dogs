from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    # breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    favorite_food = models.CharField(max_length=100)
    favorite_toy = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}: {self.name}"

# class Breed(models.Model):
#     pass
