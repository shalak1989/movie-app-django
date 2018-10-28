from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
from django.utils.html import escape

import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    print(str(request.GET.get('query', '')))
    user_query = str(request.GET.get('query', ''))
    if user_query == "":
        search_result = AT.get_all()
    else:
        search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")

    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):
    if request.method == 'POST':
        noPictureUrl = 'https://vignette.wikia.nocookie.net/sqmegapolis/images/2/2d/RealWorld_Stonehenge.jpg'
        data = {
               'Name': request.POST.get('name'),
               'Pictures': [{ 'url': request.POST.get('url') or noPictureUrl }],
               'Rating': int(request.POST.get('rating')),
               'Notes': request.POST.get('notes')
           }
        try:
            response = AT.insert(data)
            messages.success(request, 'New Movie Added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Error creating movie: {}'.format(e))
    return redirect('/')

def edit(request, movie_id):
        try:
            if request.method == 'POST':
                data = {
                        'Name': request.POST.get('name'),
                        'Pictures': [{ 'url': request.POST.get('url') or noPictureUrl }],
                        'Rating': int(request.POST.get('rating')),
                        'Notes': request.POST.get('notes')
                    }
                response = AT.update(movie_id, data)
                messages.success(request, 'Movie Edited: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Got an error when trying to update a movie {}'.format(e))
        return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        messages.warning(request, 'Movie Deleted: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request, "Error deleting a movie: {}".format(e))
    return redirect('/')



