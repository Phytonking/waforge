from django.db import models

# Create your models here.
class Itenerary(models.Model):
    id = models.UUIDField(primary_key=True)
    json = models.TextField()
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    departing_from = models.TextField(null=True)

    def __str__(self):
        return str(self.id)