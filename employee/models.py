from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Company(models.Model):
    name = models.CharField(max_length = 50, null=True, blank=True)
    name2 = models.CharField(max_length = 50, null=True, blank=True)

    def __str__(self):
        return self.name

        class Meta:
            db_table = "Company"



class employee(models.Model):
    gongHao = models.CharField(max_length=50, primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True, blank=True)
    lineid = models.CharField(max_length=50, null=False, blank=True, default='no')
    contact_num = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "employee"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
	    employee.objects.create(user=instance)





