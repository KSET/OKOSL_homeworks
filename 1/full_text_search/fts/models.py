# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.db.models.functions import Concat
from django.contrib.postgres.search import SearchVector, SearchVectorField


class Movies(models.Model):
    categoryChoices = [
                ('Com', 'Comedy'), 
                ('Ani', 'Animation'), 
                ('Mus', 'Music'), 
                ('For', 'Foreign'),
                ('Doc', 'Documentary'), 
                ('Cla', 'Classics'), 
                ('Act', 'Action'), 
                ('New', 'New'),
                ('Spo', 'Sports'), 
                ('Fam', 'Family'),
                ('Chi', 'Children'), 
                ('Tra', 'Travel'),
                ('Hor', 'Horror'), 
                ('Gam', 'Games'), 
                ('Dra', 'Drama'), 
                ('SF', 'Sci-Fi')]

    movieID = models.BigAutoField(primary_key=True, db_column='movie_id')
    title = models.CharField(max_length=255, blank=True, null=True)
    categories = models.CharField(max_length=50, blank=True, null=True, choices=categoryChoices)
    summary = models.TextField(blank=True, null=True)
    movieDescriptionID = models.ForeignKey('MovieDescriptions', models.DO_NOTHING, db_column='moviedescriptionid', blank=True, null=True)
    search_vector = SearchVectorField('title')# + SearchVectorField('summary')

    class Meta:
        managed = True
        db_table = 'movie'

    def __str__(self):
        return self.title


class MovieDescriptions(models.Model):
    movieDescriptionID = models.BigAutoField(primary_key=True, db_column='moviedescriptionid')
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'moviedescriptions'

    def __str__(self):
        """return ID+the first 100 characters of description or the whole description if it is shorter than 100 chars"""
        return str(self.movieDescriptionID) + ": " + str(self.description[:(100 if len(self.description) >= 100 else len(self.description)-1)])

