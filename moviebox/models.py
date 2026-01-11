


from django.db import models

class register(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=120)
    password=models.CharField(max_length=120)

class Prediction(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE)
    release_year = models.IntegerField()
    release_day = models.IntegerField()
    release_month = models.IntegerField()
    status = models.CharField(max_length=50)
    original_language = models.CharField(max_length=10)
    budget = models.FloatField()
    popularity = models.FloatField()
    genres_count = models.IntegerField()
    production_companies = models.CharField(max_length=100)
    production_countries = models.CharField(max_length=100)
    spoken_languages_count = models.IntegerField()
    cast_count = models.IntegerField()
    crew_count = models.IntegerField()
    runtime = models.FloatField()
    predicted_revenue = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
