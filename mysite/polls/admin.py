from django.contrib import admin

# Register your models here.
from .models import Question,Choice

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields=('pub_date',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)