from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from first_att import views as user_views
from django.contrib.auth import views as auth_views

from Site import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # страница администрирования
    path('main', user_views.main, name='main'),
    path('log_in', user_views.LoginView.as_view(template_name='pages_accounts/Авторизация.html'), name='log_in'),  # главная страница
    re_path('log_out', auth_views.LogoutView.as_view(template_name='pages_accounts/Выход.html'), name='log_out'),  # страница выхода
    re_path(r'^profile/article_registration', user_views.article_regist, name='article_registration'),  # страница регистрации статьи
    path('profile/articles/<int:pk>/', user_views.show_article, name='articles'),  # страница просмотра статьи
    path('profile/delete_article/<int:pk>/', user_views.delete_article, name='delete_article'),  # страница удаления статьи
    path('profile/articles/<int:id>/download', user_views.download, name='download'),  # страница загрузки статьи
    path('profile/articles/<int:id>/edit', user_views.edit_article, name='edit_article'),  # страница редактирования статьи
    path('profile/articles/<int:id>/success', user_views.success, name='success'),  # страница успешного редактирования статьи
    re_path(r'^profile/my_articles', user_views.articles, name='my_articles'),  # страница со списком статей
    re_path(r'^profile/edit_profile', user_views.edit_profile, name='edit_profile'),  # страница редактирования профиля
    path('register', user_views.register, name='register'),  # страница регистрации
    re_path('profile/$', user_views.profile, name='profile'),  # страница профиля
    path('', user_views.redir),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# re_path(r'^profile/event_registration', user_views.event_registration, name='event_registration'),
# re_path(r'^profile/my_events$', user_views.events, name='my_events'),
