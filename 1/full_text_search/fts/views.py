from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import *
from .models import *


def unos(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MovieForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            movie_description = MovieDescriptions.objects.create(description=form.cleaned_data['description'])
            movie = Movies.objects.create(title=form.cleaned_data['title'], category=form.cleaned_data['category'],
                                          summary=form.cleaned_data['summary'], description=movie_description.id)

            # redirect to a new URL:
            return HttpResponseRedirect('/' + movie.id + '/detail/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MovieForm()

    return render(request, 'fts/fts.html', {'form': form})


def pretraga(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'fts/pretraga.html', {'form': form})


def detail(request, movie_id):
    return HttpResponse("Test test movie %s." % movie_id)


def results(request):
    return HttpResponse("Test test results.")