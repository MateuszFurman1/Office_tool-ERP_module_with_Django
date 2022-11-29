from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from office_tool_app.form import RegistrationForm, LoginForm, UserUpdateForm
from office_tool_app.models import User, Group


class HomeView(View):
    def get(self, request):
        user = request.user
        ctx = {}
        if user.is_authenticated:
            today = str(datetime.now().date())
            group = user.group
            group_users = Group.objects.all()[0]
            print(group_users.user_set)
            print(group_users)
            address = user.address_set.all()
            print(address)
            vacations = user.vacation_employee.filter(status='pending').filter(vacation_from__gte=today)
            messages = user.messages_to_employee.all().order_by('-sending_date')
            delegations = user.delegation_set.filter(status='pending').filter(start_date__gte=today)

            ctx = {
                'group': group,
                'address': address,
                'vacations': vacations,
                'messages': messages,
                'delegations': delegations,
            }

        return render(request, "office_tool_app/Home.html", ctx)


class VacationDetailView(LoginRequiredMixin, View):
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
    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        delegations_today = user.delegation_set.filter(status='pending').filter(start_date__gte=today)
        delegations = user.delegation_set.filter(start_date__lt=today)
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
        messages.info(request, "Logout successfully")
        return redirect('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    def get(self, request, username):

        user = get_object_or_404(User, username=username)
        form = UserUpdateForm(instance=user)
        ctx = {
            'form': form,
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
