from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
import numpy as np
from collections import Counter
from .models import Movie
from openai import OpenAI
import os
from dotenv import load_dotenv

matplotlib.use('Agg')

# ============================
# Vista de estadísticas
# ============================
def statistics_view(request):
    movies = Movie.objects.all()

    # --- Gráfico por año ---
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

    # --- Gráfico por género ---
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

# ============================
# Vistas existentes
# ============================
def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

# ============================
# NUEVA vista de recomendación
# ============================
def recommend_view(request):
    recommended_movie = None
    user_prompt = None

    if request.method == "POST":
        user_prompt = request.POST.get("query")

        # Cargar API key
        load_dotenv("openAI.env")
        api_key = os.getenv("openai_apikey")
        client = OpenAI(api_key=api_key)

        # Generar embedding del prompt
        response = client.embeddings.create(
            input=[user_prompt],
            model="text-embedding-3-small"
        )
        prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

        # Función de similitud coseno
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # Buscar la película más parecida
        max_similarity = -1
        for movie in Movie.objects.all():
            if movie.emb:
                movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                similarity = cosine_similarity(prompt_emb, movie_emb)
                if similarity > max_similarity:
                    max_similarity = similarity
                    recommended_movie = movie

    return render(request, 'recommend.html', {
        "query": user_prompt,
        "recommended_movie": recommended_movie
    })
