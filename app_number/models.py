from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Statistic(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(blank=True, null=True)


    def get_absolute_url(self):
        return reverse("app_number:dashboard", kwargs={"slug": self.slug})


    @property
    def data(self):
        return self.dataitem_set.all()
    

    def __str__(self):
        return f"{self.name} - {self.slug}"
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class DataItem(models.Model):
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    owner = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.owner} - {self.value}"
