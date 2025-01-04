from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import UserProgress, Problem
from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProgress, Problem

@login_required
def roadmap_view(request):
    # Fetch problems by category
    array_problems = Problem.objects.filter(category='Array')
    string_problems = Problem.objects.filter(category='String')
    binary_search_problems = Problem.objects.filter(category='Binary Search')
    linked_list_problems = Problem.objects.filter(category='Linked List')
    two_pointers_problems = Problem.objects.filter(category='Two Pointers')

    # Fetch user progress for the logged-in user
    user_progress = UserProgress.objects.filter(user=request.user)
    user_progress_dict = {progress.problem.id: progress.completed for progress in user_progress}

    # Attach the completion status to each problem
    for problem in array_problems:
        problem.completed = user_progress_dict.get(problem.id, False)
    for problem in string_problems:
        problem.completed = user_progress_dict.get(problem.id, False)
    for problem in binary_search_problems:
        problem.completed = user_progress_dict.get(problem.id, False)
    for problem in linked_list_problems:
        problem.completed = user_progress_dict.get(problem.id, False)
    for problem in two_pointers_problems:
        problem.completed = user_progress_dict.get(problem.id, False)

    # Calculate overall progress
    total_problems = Problem.objects.count()
    completed_problems = user_progress.filter(completed=True).count()
    progress_percentage = (completed_problems / total_problems * 100) if total_problems > 0 else 0

    # Calculate progress by difficulty
    difficulties = ['Easy', 'Medium', 'Hard']
    difficulty_progress = {
        difficulty: {
            'total': Problem.objects.filter(difficulty=difficulty).count(),
            'completed': user_progress.filter(problem__difficulty=difficulty, completed=True).count()
        }
        for difficulty in difficulties
    }

    context = {
        'array_problems': array_problems,
        'string_problems': string_problems,
        'binary_search_problems': binary_search_problems,
        'linked_list_problems': linked_list_problems,
        'two_pointers_problems': two_pointers_problems,
        'total_problems': total_problems,
        'completed_problems': completed_problems,
        'progress_percentage': progress_percentage,
        'difficulty_progress': difficulty_progress,
        'username': request.user.username  # Add the username to the context
    }

    return render(request, 'leetcode2.html', context)


@login_required
def update_problem_status(request, problem_id):
    if request.method == 'POST' or request.method == 'GET':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            completed = data.get('completed')  # This is already a boolean

            # Get or create the user progress record
            user_progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                problem_id=problem_id
            )
            user_progress.completed = completed
            user_progress.save()

            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        
    return JsonResponse({'success': False}, status=400)