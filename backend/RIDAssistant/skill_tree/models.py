from django.db import models

# Create your models here.

from core.models import BaseModel

class SkillTree(BaseModel):
    name = models.CharField(max_length=64)


class Skill(BaseModel):
    name = models.CharField(max_length=64)


class SkillPrerequisite(BaseModel):
    skill = models.ForeignKey(Skill, on_delete=models.deletion.CASCADE)