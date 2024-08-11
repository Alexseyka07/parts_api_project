from django.db import models



# Create your models here.
class mark(models.Model):
    name = models.CharField(max_length=200)
    producer_country_name = models.CharField(max_length=200)
    is_visible = models.BooleanField(default=True)


class model(models.Model):
    name = models.CharField(max_length=200)
    mark = models.ForeignKey(mark, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)


class part(models.Model):
    name = models.CharField(max_length=200)
    mark = models.ForeignKey(mark, on_delete=models.CASCADE)
    model = models.ForeignKey(model, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, default=0)
    json_data = models.JSONField(null=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["name", "mark", "json_data", "is_visible"]),
            models.Index(fields=["mark", "json_data", "is_visible"]),
        ]
