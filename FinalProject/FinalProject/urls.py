"""FinalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FinalApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('navbar/',views.navbar,name='navbar'),

    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),

    path('student/',views.student,name='student'),
    path('staff/',views.staff,name='staff'),
    path('admin1/',views.admin1,name='admin1'),

    path('register_student/',views.register_student,name='register_student'),
    path('register_accountant/',views.register_accountant,name='register_accountant'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('update_fee/<int:student_id>/',views.update_fee,name='update_fee'),
    path('balance/', views.balance_view, name='balance'),
    path('make_payment/<int:student_id>/', views.make_payment, name='make_payment'),

]
