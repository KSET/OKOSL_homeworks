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
from django.contrib.postgres.search import SearchVector



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Movies(models.Model):
    movieID = models.BigAutoField(primary_key=True, db_column='movie_id')
    title = models.CharField(max_length=255, blank=True, null=True)
    categories = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    movieDescriptionID = models.ForeignKey('MovieDescriptions', models.DO_NOTHING, db_column='moviedescriptionid', blank=True, null=True)
    search_vector = SearchVector(editable=False)

    class Meta:
        managed = False
        db_table = 'movie'

    def __str__(self):
        return self.title

    # def save(self):
    #     document = Concat(
    #         'title', models.Value(self.title),
    #         'categories', models.Value(self.categories),
    #         'summary', models.Value(self.summary),
    #         'description', models.Value(MovieDescriptions.objects.get(pk=self.movieDescriptionID_id))
    #     )
    #     vector = SearchVector('title', weight='A') + \
    #              SearchVector('categories', weight='C') + \
    #              SearchVector('summary', weight='B') + \
    #              SearchVector('description', weight='D')
    #
    #     self.search_vector = Movies.objects.annotate(document=vector).values_list('document', flat=True)[0]
    #     super(Movies, self).save()


class MovieDescriptions(models.Model):
    movieDescriptionID = models.BigAutoField(primary_key=True, db_column='moviedescriptionid')
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'moviedescriptions'

    def __str__(self):
        return str(self.movieDescriptionID)


class SearchVectorTriggeredField(models.Field):

    def db_type(self, connection):
        return 'tsvector'



