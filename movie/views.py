from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
import matplotlib
matplotlib.use('Agg')
from collections import Counter
from .models import Movie

# Create your views here.

def statistics_view(request):
    movies = Movie.objects.all()

    
    years = [m.year for m in movies if m.year]
    year_counts = Counter(years)

    plt.bar(year_counts.keys(), year_counts.values(), width=0.5, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    plt.close()
    graphic_year = base64.b64encode(buffer1.getvalue()).decode('utf-8')
    buffer1.close()


    genres = [m.genre.split(",")[0].strip() for m in movies if m.genre]
    genre_counts = Counter(genres)

    plt.bar(genre_counts.keys(), genre_counts.values(), width=0.5, align='center', color='orange')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()
    graphic_genre = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    buffer2.close()

    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })

def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email =request.GET.get('email')
    return render(request, 'signup.html', {'email':email})