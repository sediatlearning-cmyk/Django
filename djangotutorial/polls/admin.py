from django.contrib import admin
from .models import Question
from .models import Choice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    list_filter = ('question_text', 'pub_date')
    ordering = ('question_text', 'pub_date')
    search_fields = ('question_text', 'pub_date')
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'votes')
    list_filter = ('question', 'choice_text', 'votes')
    ordering = ('question', 'choice_text', 'votes')
    search_fields = ('choice_text')

admin.site.register(Question)
admin.site.register(Choice)
