# user/models.py

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Plan(models.Model):
    PLAN_CHOICES = [
        ('Child Plan', 'Child Plan'),
        ('Young Adult Plan', 'Young Adult Plan'),
        ('Adult Plan', 'Adult Plan'),
        ('Senior Plan', 'Senior Plan'),
    ]

    user = models.ManyToManyField(User, related_name='plans')
    plan_type = models.CharField(max_length=50, choices=PLAN_CHOICES)
    from_days = models.DateField(null=True, blank=True)
    to_days = models.DateField(null=True, blank=True)
    from_year = models.IntegerField(null=True, blank=True)
    to_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.plan_type} for {self.user.name}"