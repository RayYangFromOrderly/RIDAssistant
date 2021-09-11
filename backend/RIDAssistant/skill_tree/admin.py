from django.contrib import admin
from django.db import models

from .models import Skill, SkillTree, SkillPrerequisite

# Register your models here.

@admin.register(SkillTree)
class SkillTreeAdmin(admin.ModelAdmin):
    fields = ('c_at', 'u_at', 'name')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    fields = ('c_at', 'u_at', 'name')


@admin.register(SkillPrerequisite)
class SkillPrerequisite(admin.ModelAdmin):
    fields = ('c_at', 'u_at', 'skill')