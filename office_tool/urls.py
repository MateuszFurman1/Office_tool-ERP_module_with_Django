"""office_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from office_tool_app.views import HomeView, RegistrationView, LoginView, LogoutView, ProfileView, VacationDetailView, \
    DelegationDetailView, ManageView, MedicalLeaveView, ManageDetailView, MedicalLeaveCreateView, DelegationCreateView, \
    DelegationDeleteView, VacationCreateView, VacationDeleteView, MedicalDeleteView, VacationAcceptView, \
    DelegationRejectView, DelegationAcceptView, VacationRejectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
    path('vacation-detail/', VacationDetailView.as_view(), name='vacation-detail'),
    path('delegation-detail/', DelegationDetailView.as_view(), name='delegation-detail'),
    path('manage/', ManageView.as_view(), name='manage'),
    path('medical-leave/', MedicalLeaveView.as_view(), name='medical-leave'),
    path('delete-medical/<int:pk>/', MedicalDeleteView.as_view(), name='delete-medical'),
    path('manage-detail/<username>/', ManageDetailView.as_view(), name='manage-detail'),
    path('create-medicalleave/<username>/', MedicalLeaveCreateView.as_view(), name='create-medical'),
    path('create-delegation', DelegationCreateView.as_view(), name='create-delegation'),
    path('delete-delegation/<int:pk>/', DelegationDeleteView.as_view(), name='delete-delegation'),
    path('accept-delegation/<int:pk>/', DelegationAcceptView.as_view(), name='accept-delegation'),
    path('reject-delegation/<int:pk>/', DelegationRejectView.as_view(), name='reject-delegation'),
    path('create-vacation', VacationCreateView.as_view(), name='create-vacation'),
    path('delete-vacation/<int:pk>/', VacationDeleteView.as_view(), name='delete-vacation'),
    path('accept-vacation/<int:pk>/', VacationAcceptView.as_view(), name='accept-vacation'),
    path('reject-vacation/<int:pk>/', VacationRejectView.as_view(), name='reject-vacation'),

]