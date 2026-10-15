from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from .forms import TodoForm
from .models import Todo


def todo_list(request):
    status = request.GET.get('status', 'all')
    if status not in ('all', 'active', 'completed'):
        status = 'all'
    todos = Todo.objects.all()
    counts = todos.aggregate(total=Count('id'), completed=Count('id', filter=Q(is_completed=True)))
    counts['active'] = counts['total'] - counts['completed']
    if status != 'all':
        todos = todos.filter(is_completed=(status == 'completed'))
    return render(request, 'todos/list.html', {'todos': todos, 'status': status, 'counts': counts})


@require_http_methods(['GET', 'POST'])
def todo_edit(request, pk=None):
    todo = get_object_or_404(Todo, pk=pk) if pk is not None else None
    form = TodoForm(request.POST if request.method == 'POST' else None, instance=todo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '할 일을 수정했습니다.' if todo else '새 할 일을 등록했습니다.')
        return redirect('todos:list')
    return render(request, 'todos/form.html', {'form': form, 'todo': todo})


@require_http_methods(['GET', 'POST'])
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, '할 일을 삭제했습니다.')
        return redirect('todos:list')
    return render(request, 'todos/delete.html', {'todo': todo})


@require_POST
def todo_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    # Assign requested state, so repeating the same request cannot toggle it back.
    todo.is_completed = request.POST.get('is_completed') == 'on'
    todo.save(update_fields=['is_completed'])
    return redirect('todos:list')
