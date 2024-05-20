from django.urls import path
from .import views

urlpatterns = [
    path('',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('home',views.home,name='home'),
    path('adminpanel',views.adminpanel,name='adminpanel'),
    path('admin',views.admin,name='admin'),
    path('delete/<int:pk>/',views.admin_delete,name='delete'),
    path('edit/<int:user_id>/',views.admin_edit,name='edit'),
    path('createuser',views.createuser,name='createuser'),
    path('logouthome',views.logouthome,name='logouthome'),
    path('logoutadmin',views.logoutadmin,name='logoutadmin'),
]