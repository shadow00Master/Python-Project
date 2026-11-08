from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import Task_Form
from .models import Todo_task

@login_required
def all_task(request):
    task = Todo_task.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'TODO/all_task.html', {'task':task})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = Task_Form(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('TODO:all_task')
    else:
        form = Task_Form()

    return render(request, 'TODO/add_task.html', {'form': form})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Todo_task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = Task_Form(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('TODO:all_task')
    else:
        form = Task_Form(instance=task)
    return render(request, 'TODO/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Todo_task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect('TODO:all_task')