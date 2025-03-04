from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Root URL loads login page
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # You can keep this too if needed
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-salary/', views.add_salary, name='add_salary'),
    path('view-salary/', views.view_salary, name='view_salary'),
    path('download-salary-pdf/<int:year>/', views.download_salary_pdf, name='download_salary_pdf'),
    path('edit-salary/<int:id>/', views.edit_salary, name='edit_salary'),
    path('delete-salary/<int:id>/', views.delete_salary, name='delete_salary'),
    path('logout/', views.logout_view, name='logout'),
]



