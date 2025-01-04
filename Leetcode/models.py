from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=255)  # Problem title
    link = models.URLField()  # Link to the LeetCode problem
    category = models.CharField(max_length=50)  # e.g., 'Array', 'String', etc.
    difficulty = models.CharField(
        max_length=10,
        choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
        default='Easy'
    )  # Problem difficulty

    def __str__(self):
        return f"{self.title} ({self.difficulty})"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The logged-in user
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)  # The specific problem
    completed = models.BooleanField(default=False)  # Track if the problem is completed

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
