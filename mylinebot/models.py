from django.db import models

# Create your models here.
class Manager(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    line_id = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True, default='no')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Manager"