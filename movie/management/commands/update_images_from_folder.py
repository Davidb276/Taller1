import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images in the database from the media/movie/images folder"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        updated_count = 0

        if not os.path.exists(images_folder):
            self.stderr.write(f"Folder '{images_folder}' not found.")
            return

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")

        for movie in movies:
            # Nombre esperado del archivo
            image_filename = f"m_{movie.title}.png"
            image_path = os.path.join(images_folder, image_filename)

            if os.path.exists(image_path):
                movie.image = os.path.join('movie/images', image_filename)
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title}")

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies with images."))        
