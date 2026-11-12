from django.urls import path
from django.conf import settings

from . import views
app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/1/detail
    #path("<int:pk>/detail/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/1/results
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/1/vote
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # ex: /polls/all
    path('all/', views.AllView.as_view(), name='all'),
    # ex: /polls/1/frequency
    path('<int:pk>/frequency/', views.FrequencyView.as_view(), name='frequency'),
    # ex: /polls/statistics
    path('statistics/', views.statistics, name='statistics'),
    # ex: /polls/add
    path('add/', views.add, name='add'),
    # ex: /polls/confirm_add
    #path('confirm_add/', views.confirm_add, name='confirm_add'),
    ] 
