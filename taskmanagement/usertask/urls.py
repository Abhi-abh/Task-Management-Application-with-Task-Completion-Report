from django.urls import path
from . import views
from .views import RegisterView, LoginView, ProtectedView, LogoutView, TokenRefreshView, UserTasksView, UpdateTaskStatusView, TaskReportView

urlpatterns = [
    path('',views.login,name='login'),
    path('login1/',views.login1,name='login1'),
    path('signup/',views.signup,name='signup'),
    path('home/',views.home,name='home'),
    path('home1/',views.home1,name='home1'),
    path('Addtask/',views.Addtask,name='Addtask'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('view/<int:id>/',views.views_page,name='view'),
    path('logout/',views.loggout,name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('loginapi/', LoginView.as_view(), name='login'),
    path('logoutapi/', LogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='refreshtoken'),
    path('tasks/', UserTasksView.as_view(), name='user_tasks'),
    path('tasks/<int:id>/', UpdateTaskStatusView.as_view(), name='update_task_status'),
    path('tasks/<int:id>/report/', TaskReportView.as_view(), name='task_report'),
]

