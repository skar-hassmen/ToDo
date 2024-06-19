from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, RedirectView, UpdateView

from personal_area.forms import CreateTaskForm, EditTaskForm
from personal_area.models import Tasks
from datetime import datetime


def check_overdue(request, tasks):
    not_done, done, overdue = 0, 1, 2
    for task in tasks:
        if task.date_deadline < datetime.now().date() and task.status != done:
            task.status = overdue
            task.save()
        elif task.status != done:
            task.status = not_done
            task.save()


def filter_task(request, argument):
    not_done, done, overdue = 0, 1, 2
    current_user = request.user
    if argument == 'all':
        tasks = Tasks.objects.filter(user=current_user)
        check_overdue(request, tasks)
    elif argument == 'done':
        tasks = Tasks.objects.filter(user=current_user, status=done)
    elif argument == 'not_done':
        tasks = Tasks.objects.filter(user=current_user, status=not_done)
    elif argument == 'overdue':
        tasks = Tasks.objects.filter(user=current_user, status=overdue)
    else:
        tasks = Tasks.objects.filter(user=current_user)
    return tasks


def sorted_task_priority(request, tasks):
    priority1, priority2, priority3 = [], [], []
    for task in tasks:
        if task.priority == 3:
            priority3.append(task)
        elif task.priority == 2:
            priority2.append(task)
        else:
            priority1.append(task)
    return priority3 + priority2 + priority1


def sorted_task_date(request, tasks):
    for i in range(len(tasks) - 1, -1, -1):
        for j in range(0, i):
            if (tasks[j].date_deadline > tasks[j + 1].date_deadline):
                temp = tasks[j]
                tasks[j] = tasks[j + 1]
                tasks[j + 1] = temp
    return tasks


def replace_priority_names(request, tasks):
    priority_names = ('низкий', 'средний', 'высокий',)
    for i in range(len(tasks)):
        tasks[i].priority = priority_names[tasks[i].priority - 1] 
    return tasks


class Account(TemplateView):
    success_url = reverse_lazy('profile_main')
    template_name = 'personal_area/account.html'

    def get_context_data(self, **kwargs):
        context = super(Account, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            done, overdue = 1, 2
            current_user = self.request.user
            tasks = filter_task(self.request, kwargs['filter'])
            if kwargs['sorted'] == 'priority':
                tasks = sorted_task_priority(self.request, tasks)
            elif kwargs['sorted'] == 'date':
                tasks = sorted_task_date(self.request, list(tasks))
            context['tasks'] = replace_priority_names(self.request, tasks)
            context['all_cnt'] = Tasks.objects.filter(user=current_user).count()
            context['done_cnt'] = Tasks.objects.filter(user=current_user, status=done).count()
            context['overdue_cnt'] = Tasks.objects.filter(user=current_user, status=overdue).count()
            context['not_done_cnt'] = context['all_cnt'] - context['done_cnt']
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous is True:
            return redirect('login_error')
        else:
            return super(Account, self).dispatch(request, *args, **kwargs)


class CreateTask(CreateView):
    model = Tasks
    form_class = CreateTaskForm
    success_url = reverse_lazy('profile_main')
    template_name = 'personal_area/actions_task.html'

    def get_context_data(self, **kwargs):
        context = super(CreateTask, self).get_context_data(**kwargs)
        context['title'] = 'Создание задачи'
        return context

    def form_valid(self, form):
        form_valid = super(CreateTask, self).form_valid(form)
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return form_valid

    def form_invalid(self, form):
        super(CreateTask, self).form_invalid(form)
        return redirect('create_task_error')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous is True:
            return redirect('login_error')
        else:
            return super(CreateTask, self).dispatch(request, *args, **kwargs)


class DoneTask(RedirectView):
    url = reverse_lazy('profile_main')

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            current_user, done = self.request.user, 1
            task = get_object_or_404(Tasks, user=current_user, id=kwargs['id_task'])
            if task.status != done:
                task.status = done
                task.save()
        return super().get_redirect_url(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous is True:
            return redirect('login_error')
        else:
            return super(DoneTask, self).dispatch(request, *args, **kwargs)


class DeleteTask(RedirectView):
    url = reverse_lazy('profile_main')

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            current_user = self.request.user
            task = get_object_or_404(Tasks, user=current_user, id=kwargs['id_task'])
            task.delete()
        return super().get_redirect_url(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous is True:
            return redirect('login_error')
        else:
            return super(DeleteTask, self).dispatch(request, *args, **kwargs)


class EditTask(UpdateView):
    model = Tasks
    form_class = EditTaskForm
    success_url = reverse_lazy('profile_main')
    template_name = 'personal_area/actions_task.html'

    def get_context_data(self, **kwargs):
        context = super(EditTask, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование задачи'
        return context

    def get(self, request, *args, **kwargs):
        get = super(EditTask, self).get(request, *args, **kwargs)
        if self.object.user != request.user:
            raise Http404()
        return get

    def post(self, request, *args, **kwargs):
        post = super(EditTask, self).post(request, *args, **kwargs)
        if self.object.user != request.user:
            raise Http404()
        return post

    def form_invalid(self, form):
        super(EditTask, self).form_invalid(form)
        return redirect('edit_task_error')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous is True:
            return redirect('login_error')
        else:
            return super(EditTask, self).dispatch(request, *args, **kwargs)


class CreateTaskError(TemplateView):
    success_url = reverse_lazy('create_task_error')
    template_name = 'personal_area/errorPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        error_empty_task = {
            'Error': 'Ошибка Создания',
            'str0': 'Произошла ошибка!',
            'str1': 'Возможно, Вы ввели некорректные данные или попытались создать пустую задачу.',
            'str2': 'Заполните все поля и попробуйте снова!',
            'url_come_back': reverse_lazy('create_task'),
            'come_back': 'Вернуться к созданию задачи',
        }
        return context | error_empty_task


class LoginError(TemplateView):
    success_url = reverse_lazy('login_error')
    template_name = 'personal_area/errorPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        error_access_anonumous = {
            'Error': 'Ошибка Доступа',
            'str0': 'Произошла ошибка!',
            'str1': 'Возможно, Вы были не авторизованы, поэтому у вас нет доступа к личному кабинету.',
            'str2': 'Авторизируйтесь и попробуйте снова!',
            'url_come_back': reverse_lazy('login'),
            'come_back': 'Вернуться к авторизации',
        }
        return context | error_access_anonumous


class EditTaskError(TemplateView):
    success_url = reverse_lazy('edit_task_error')
    template_name = 'personal_area/errorPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        error_access_anonumous = {
            'Error': 'Ошибка Редактирования',
            'str0': 'Произошла ошибка!',
            'str1': 'Возможно, Вы ввели некорректные данные.',
            'str2': 'Попробуйте снова!',
            'url_come_back': reverse_lazy('create_task'),
            'come_back': 'Вернуться к созданию задачи',
        }
        return context | error_access_anonumous