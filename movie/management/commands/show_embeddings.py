from django.core.management.base import BaseCommand
from movie.models import Movie
import numpy as np
import random

class Command(BaseCommand):
    help = "Muestra los embeddings de una película seleccionada al azar"

    def handle(self, *args, **kwargs):
        movies = list(Movie.objects.all())
        if not movies:
            self.stdout.write("❌ No hay películas en la base de datos")
            return

        movie = random.choice(movies)
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
        self.stdout.write(f"🎬 {movie.title}")
        self.stdout.write(f"Primeros valores del embedding: {embedding_vector[:10]}")
