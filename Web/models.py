from django import forms
from django.db import models


class MoviePage(models.Model):
    querystring = models.CharField(max_length=50)
    title = models.CharField(max_length=50)


class MovieForm(forms.ModelForm):
    class Meta:
        model = MoviePage
        fields = ('title', 'querystring')
