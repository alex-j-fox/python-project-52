from django.urls import path

from task_manager.users import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='users_index'),
    path('create/', views.UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='users_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='users_delete'),
]

# GET /users/ — страница со списком всех пользователей
# GET /users/create/ — страница регистрации нового пользователя
# POST /users/create/ — создание пользователя
# GET /users/<int:pk>/update/ — страница редактирования пользователя
# POST /users/<int:pk>/update/ — обновление пользователя
# GET /users/<int:pk>/delete/ — страница удаления пользователя
# POST /users/<int:pk>/delete/ — удаление пользователя
# GET /login/ — страница входа
# POST /login/ — аутентификация (вход)
# POST /logout/ — завершение сессии (выход)
