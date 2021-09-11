from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    c_at = models.DateTimeField(auto_now_add=True)
    u_at = models.DateTimeField(auto_now=True)
