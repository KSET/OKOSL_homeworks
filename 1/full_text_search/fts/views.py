from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.db.models.functions import Concat
from django.db.models import TextField, Value as V
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchVector

from .forms import *
from .models import *


def unos(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        movie_form = MovieForm(request.POST)
        desc_form = DescriptionForm(request.POST)
        # check whether it's valid:
        if movie_form.is_valid() and desc_form.is_valid():
            # process the data in form.cleaned_data as required
            movie_description = MovieDescriptions.objects.create(description=desc_form.cleaned_data['description'])
            movie_description.save()
            movie = Movies.objects.create(title=movie_form.cleaned_data['title'], categories=movie_form.cleaned_data['categories'],
                                          summary=movie_form.cleaned_data['summary'], movieDescriptionID=movie_description)
            movie.save()
            print(movie)
            print(movie.movieID)
            print(Movies.objects.filter(movie.movieID).search_vector)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('fts:detail', args=(movie.movieID,)))
            # return HttpResponseRedirect(str(movie.id) + '/detail/')

    # if a GET (or any other method) we'll create a blank form
    else:
        movie_form = MovieForm()
        desc_form = DescriptionForm()

    return render(request, 'fts/fts.html', {'movie_form': movie_form, 'desc_form': desc_form})


def pretraga(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            summary = form.cleaned_data['summary']
            description = form.cleaned_data['description']

            document = Concat(
                'title', models.Value(title),
                'categories', models.Value(category),
                'summary', models.Value(summary),
                #'description', models.Value(description),
                output_field=TextField()
            )

            vector = SearchVector('title', weight='A') + \
                        SearchVector('categories', weight='C') + \
                        SearchVector('summary', weight='B') + \
                        SearchVector('description', weight='D')

            result_set = Movies.objects.annotate(search=vector).filter(document=document)

            # document = Concat(
            #     'title', V(' '),
            #     'categories', V(' '),
            #     'summary', V(' '),
            #     output_field=TextField()
            # )
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('fts:results', args=(result_set,)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'fts/pretraga.html', {'form': form})


def detail(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    movie_description = get_object_or_404(MovieDescriptions, pk=movie.movieDescriptionID_id)
    return render(request, 'fts/detail.html', {'movie': movie, 'movie_description': movie_description})


def results(request, result_set):
    return render(request, 'fts/results.html', {'results': result_set})