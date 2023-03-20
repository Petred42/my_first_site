from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Student
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, FileResponse
from django.contrib.auth import forms
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required

from .utils import DataMixin


def register(request): # страница регистрации
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            student = Student.objects.create(
                name="Введите ФИО", phone="Введите контактный телефон", about="", user=form.save(), image="zoro.jpg"
            )# создание профиля для пользователя
            messages.success(request, f'Вы успешно зарегистрировались. Теперь вы можете войти.')
            return HttpResponseRedirect("log_in")  # перевод на страницу входа
        else:
            messages.success(request, f'Ошибка! Проверьте корректность введенных данных')  # сообщение об ошибке
    form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, "pages_accounts/Регистрация.html", context)


def main(request):  # главная страница
    return render(request, "pages_accounts/Главная.html")


def autorization(request):  # страница авторизации
    return render(request, "pages_accounts/Авторизация.html")


@login_required
def edit_profile(request):  # страница редактирования профиля
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = StudentUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.student)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')  # сообщение об успехе
            return redirect('profile')  # перевод на страницу профиля

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = StudentUpdateForm(instance=request.user.student)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, "pages/Редактировать_профиль.html", context)


@login_required
def profile(request):  # страница профиля
    stud = Student.objects.get(user=request.user)
    if stud.name == "Введите ФИО":  # перевод на страницу редактирования профиля
        return HttpResponseRedirect("edit_profile")
    return render(request, "pages/Профиль.html")


@login_required
def articles(request):  # страница статьей
    article = Articles.objects.filter(user=request.user)
    context = {
        'articles': article
    }
    return render(request, "pages/Мои-статьи.html", context)


@login_required
def article_regist(request):  # добавление статьи
    if request.method == 'POST':
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, f'Ваша статья успешно добавлена.')
            return redirect('my_articles')
        else:
            messages.success(request, f'Ваша статья не была добавлена. Проверьте корректность введенных данных')
    else:
        form = ArticlesForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, "pages/Регистрация_статьи.html", context)


@login_required
def edit_article(request, id):  # страница редактирования статьи
    article = get_object_or_404(Articles, pk=id)
    if request.method == 'POST':
        form = ArticlesUpdateForm(request.POST,
                                  request.FILES,
                                  instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ваша статья успешно обновлена.')
            return HttpResponseRedirect("success")
    else:
        form = ArticlesUpdateForm(instance=article)
    context = {
        'form': form,
    }
    return render(request, "pages/Редактировать_статью.html", context)


@login_required
def success(request, id):  # страница изменения статьи
    article = get_object_or_404(Articles, pk=id)
    context = {
        'article': article,
    }
    return render(request, "pages/success.html", context)


@login_required
def show_article(request, pk):  # страница информации о статье
    article = get_object_or_404(Articles, pk=pk)
    context = {
        'article': article,
    }
    return render(request, "pages/Просмотр_статьи.html", context)


@login_required
def download(request, id):  # загрузка статьи
    obj = Articles.objects.get(id=id)
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response


@login_required
def delete_article(request, pk):  # страница удаления статьи
    article = get_object_or_404(Articles, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, f'Ваша статья успешно удалена.')
        return redirect('my_articles')
    context = {
        'article': article,
    }
    return render(request, "pages/Удаление_статьи.html", context)


class LoginUser(DataMixin, LoginView):  # класс для авторизации пользователя
    form_class = LoginForm
    template_name = 'pages_accounts/Авторизация.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('profile')


def redir(request):
    return redirect('main')


"""
def event_registration(request):
    if request.method == "POST":
        event = Events()
        event.name = request.POST["name"]
        event.date = request.POST["date"]
        event.place = request.POST["place"]
        event.article = request.POST["article"]
        #event.author = request.POST.get("author")
        event.save()
        return HttpResponseRedirect("my_events")
    return render(request, "pages/Регистрация_события.html")

class events(LoginRequiredMixin, ListView):
    login_url = "log_in"
    model = Events
    template_name = "pages/Мои-мероприятия.html"


def events(request):
    context = {
        'events': Events.objects.all()
    }
    return render(request, "pages/Мои-мероприятия.html", context)
"""
