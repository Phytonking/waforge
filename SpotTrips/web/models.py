from django.db import models

# Create your models here.
class Itenerary(models.Model):
    id = models.UUIDField(primary_key=True)
    json = models.TextField()

    def __str__(self):
        return str(self.id)