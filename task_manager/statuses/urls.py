from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='statuses_index'),
    path('create/', views.StatusCreateView.as_view(), name='statuses_create'),
    path('<int:pk>/update', views.StatusUpdateView.as_view(), name='statuses_update'),
    path('<int:pk>/delete', views.StatusDeleteView.as_view(), name='statuses_delete'),
]
