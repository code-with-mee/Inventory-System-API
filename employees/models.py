from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password (in future)

    def __str__(self):
        return self.name