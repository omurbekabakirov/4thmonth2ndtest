from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView

from tasks.form import SearchForm, TaskForm
from tasks.models import Task


def main_view(request):
    return render(request, 'base.html')


def task_list_view(request):
    tasks = Task.objects.all()
    search = request.GET.get('search', None)
    category = request.GET.getlist('category', None)
    search_form = SearchForm(request.GET)
    orderings = request.GET.getlist('orderings', None)

    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if category:
        tasks = tasks.filter(category__id__in=category)
    page = int(request.GET.get('page', 1))
    limit = 5
    max_pages = tasks.count() / limit
    if round(max_pages) < max_pages:
        max_pages = round(max_pages) + 1
    else:
        max_pages = round(max_pages)
    start = (page - 1) * limit
    end = page * limit
    tasks = tasks[start:end]
    if orderings:
        tasks = tasks.order_by(orderings)
    context = {'tasks': tasks, 'search_form': search_form, 'max_pages': range(1, max_pages + 1)}

    return render(request, 'tasks/task_list.html', context=context)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    lookup_url_kwarg = 'task_id'


def task_create_view(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'tasks/task_create.html', context={'form': form})
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if not form.is_valid():
            return render(request, 'tasks/task_create.html', context={'form': form})
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        Task.objects.create(
            title=title,
            description=description,)
        return redirect('/tasks/')
