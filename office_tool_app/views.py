from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from office_tool_app.form import RegistrationForm, LoginForm, UserUpdateForm, AddressHomeForm, \
    AddressCoreForm
from office_tool_app.models import User, Group, AddressHome, AddressCore


class HomeView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        ctx = {}
        if user.is_authenticated:
            today = str(datetime.now().date())
            group = user.group
            group_users = group.user_set.all()
            print(group_users)
            group_users2 = User.objects.filter(group=group)
            vacations = user.vacation_employee.filter(status='pending').filter(vacation_from__gte=today)
            messages = user.messages_to_employee.all().order_by('-sending_date')
            delegations = user.delegation_employee.filter(status='pending').filter(start_date__gte=today)

            ctx = {
                'group_users': group_users,
                'vacations': vacations,
                'messages': messages,
                'delegations': delegations,
            }

        return render(request, "office_tool_app/Home.html", ctx)


class VacationDetailView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        vacations_today = user.vacation_employee.filter(status='pending').filter(vacation_from__gte=today)
        vacations = user.vacation_employee.filter(vacation_from__lt=today)
        ctx = {
            'vacations_today': vacations_today,
            'vacations': vacations
        }
        return render(request, 'office_tool_app/vacationDetail.html', ctx)


class DelegationDetailView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        delegations_today = user.delegation_employee.filter(status='pending').filter(start_date__gte=today)
        delegations = user.delegation_employee.filter(start_date__lt=today)
        ctx = {
            'delegations_today': delegations_today,
            'delegations': delegations
        }
        return render(request, 'office_tool_app/delegationDetail.html', ctx)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        page = 'registration'
        ctx = {
            "form": form,
            'page': page
        }
        return render(request, "office_tool_app/form.html", ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        ctx = {
            "form": form,
        }
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Sign up successfully")
            return redirect('login')
        messages.error(request, "Something goes wrong. Try again")
        return render(request, 'office_tool_app/form.html', ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        page = 'login'
        ctx = {
            "form": form,
            'page': page
        }
        return render(request, 'office_tool_app/form.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successfully")
                return redirect('home')
            else:
                messages.error(request, "Wrong name/password!")
                ctx = {
                    "form": form
                    }
                return render(request, 'office_tool_app/form.html', ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout successfully")
        return redirect('login')


class ProfileView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        form = UserUpdateForm(instance=user)
        address_home = AddressHome.objects.filter(employee=user)
        address_core = AddressCore.objects.filter(employee=user)
        form_home = AddressHomeForm(instance=address_home[0])
        form_core = AddressCoreForm(instance=address_core[0])
        ctx = {
            'form': form,
            'form_home': form_home,
            'form_core': form_core,
            'username': username
        }
        return render(request, "office_tool_app/profile.html", ctx)

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        form = UserUpdateForm(request.POST, instance=user)
        ctx = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.success(request, f"Your profile has been updated!")
            return redirect('profile', user.username)
        messages.error(request, "Something goes wrong")
        return render(request, 'office_tool_app/profile.html', ctx)


class ManageView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def get(self, request):
        user = request.user
        group_one = Group.objects.get(pk=1)
        members_one = group_one.user_set
        print(members_one)
        group_two = Group.objects.get(pk=2)
        members_two = group_one.user_set
        print(members_two)
        ctx = {
            'group_one': group_one,
            'members_one': members_one,
            'group_two': group_two,
            'members_two': members_two,

        }
        return render(request, 'office_tool_app/manage.html', ctx)


class MedicalLeaveView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        medicals = user.medicalleave_set.all()
        ctx = {
            'medicals': medicals

        }
        return render(request, 'office_tool_app/MedicalLeave.html', ctx)