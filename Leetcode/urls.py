from django.urls import path
from . import views
app_name = 'leetcode'  # This is the namespace for the Leetcode app

urlpatterns = [
    path('', views.roadmap_view, name='roadmap'),
    path('leetcode/update-problem-status/<int:problem_id>/', views.update_problem_status, name='update_problem_status'),

]
