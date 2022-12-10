from datetime import datetime

import vacation as vacation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DeleteView

from office_tool_app.form import RegistrationForm, LoginForm, UserUpdateForm, AddressHomeForm, \
    AddressCoreForm, MedicalLeaveForm, DelegationForm, VacationForm
from office_tool_app.models import User, Group, AddressHome, AddressCore, Vacation, Delegation, MedicalLeave


class HomeView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        ctx = {}
        if user.is_authenticated:
            today = str(datetime.now().date())
            group = user.group
            group_users = group.user_set.all()
            # group_users2 = User.objects.filter(group=group)
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

    def get(self, request):
        user = request.user
        form = UserUpdateForm(instance=user)
        address_home = AddressHome.objects.filter(employee=user)
        address_core = AddressCore.objects.filter(employee=user)
        if not address_home:
            form_home = AddressHomeForm()
        else:
            form_home = AddressHomeForm(instance=address_home[0])
        if not address_core:
            form_core = AddressCoreForm()
        else:
            form_core = AddressCoreForm(instance=address_core[0])
        ctx = {
            'form': form,
            'form_home': form_home,
            'form_core': form_core,
        }
        return render(request, "office_tool_app/profile.html", ctx)

    def post(self, request):
        user = request.user
        form = UserUpdateForm(request.POST, instance=user)
        ctx = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.success(request, f"Your profile has been updated!")
            return redirect('profile')
        messages.error(request, "Something goes wrong")
        return render(request, 'office_tool_app/profile.html', ctx)


class VacationDetailView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        vacations_today = user.vacation_employee.filter(status='pending').filter(vacation_from__gte=today)
        vacations_past = user.vacation_employee.filter(status='accepted').filter(vacation_from__lte=today)
        vacations_future = user.vacation_employee.filter(status='accepted').filter(vacation_from__gt=today)
        ctx = {
            'vacations_today': vacations_today,
            'vacations_past': vacations_past,
            'vacations_future': vacations_future,
        }
        return render(request, 'office_tool_app/vacationDetail.html', ctx)


class VacationCreateView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = VacationForm()
        ctx = {
            'form': form,
            'user': user,
        }
        return render(request, 'office_tool_app/form2.html', ctx)

    def post(self, request):
        user = request.user
        form = VacationForm(request.POST)
        if form.is_valid():
            vacation = form.save(commit=False)
            vacation.employee = user
            vacation.status = 'pending'
            vacation.save()
            return redirect('vacation-detail')


class VacationDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacation
    success_url = reverse_lazy("vacation-detail")


class VacationAcceptView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def post(self, request, pk):
        vacation = Vacation.objects.get(id=pk)
        vacation.status = 'accepted'
        vacation.save()
        user = vacation.employee
        print(user)
        today = str(datetime.now().date())

        return redirect('manage-detail', user.username)


class VacationRejectView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def post(self, request, pk):
        vacation = Vacation.objects.get(id=pk)
        vacation.status = 'accepted'
        vacation.save()
        user = vacation.employee
        print(user)
        return redirect('manage-detail', user.username)


class DelegationDetailView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        delegations_today = user.delegation_employee.filter(status='pending').filter(start_date__gte=today)
        delegations_past = user.delegation_employee.filter(status='accepted').filter(start_date__lte=today)
        delegations_future = user.delegation_employee.filter(status='accepted').filter(start_date__gt=today)
        ctx = {
            'delegations_today': delegations_today,
            'delegations_past': delegations_past,
            'delegations_future': delegations_future,
        }
        return render(request, 'office_tool_app/delegationDetail.html', ctx)


class DelegationCreateView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = DelegationForm()
        ctx = {
            'form': form,
            'user': user,
        }
        return render(request, 'office_tool_app/form2.html', ctx)

    def post(self, request):
        user = request.user
        form = DelegationForm(request.POST)
        if form.is_valid():
            delegation = form.save(commit=False)
            delegation.employee = user
            delegation.status = 'pending'
            delegation.save()
            return redirect('delegation-detail')


class DelegationDeleteView(LoginRequiredMixin, DeleteView):
    model = Delegation
    success_url = reverse_lazy("delegation-detail")


class DelegationAcceptView(LoginRequiredMixin, View):
    # permission_required = 'can_manage_employees'
    def get(self, request, pk):
        delegation = get_object_or_404(Delegation, pk=pk)
        user = delegation.employee
        ctx = {
            "delegation": delegation,
            'user': user,
        }
        return render(request, "office_tool_app/delegation_confirm_accept.html", ctx)

    def post(self, request, pk):

        delegation = Delegation.objects.get(id=pk)
        delegation.status = 'accepted'
        delegation.save()
        user = delegation.employee
        print(user)
        return redirect('manage-detail', user.username)


class DelegationRejectView(LoginRequiredMixin, View):
    # permission_required = 'can_manage_employees'
    def get(self, request, pk):
        delegation = get_object_or_404(Delegation, pk=pk)
        user = delegation.employee
        ctx = {
            "delegation": delegation,
            'user': user,
        }
        return render(request, "office_tool_app/delegation_confirm_accept.html", ctx)

    def post(self, request, pk):

        delegation = Delegation.objects.get(id=pk)
        delegation.status = 'rejected'
        delegation.save()
        user = delegation.employee
        print(user)
        return redirect('manage-detail', user.username)


class MedicalLeaveView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        medicals = user.medical_employee.all()
        ctx = {
            'medicals': medicals

        }
        return render(request, 'office_tool_app/MedicalLeave.html', ctx)


class MedicalLeaveCreateView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def get(self, request, username):
        user = User.objects.get(username=username)
        form = MedicalLeaveForm()
        ctx = {
            "form": form,
            'user': user,
        }
        return render(request, "office_tool_app/form2.html", ctx)

    def post(self, request, username):
        user = User.objects.get(username=username)
        form = MedicalLeaveForm(request.POST)
        if form.is_valid():
            medical_leave = form.save(commit=False)
            medical_leave.employee = user
            medical_leave.save()
            return redirect('manage-detail', user.username)


class MedicalDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        medical_leave = get_object_or_404(MedicalLeave, pk=pk)
        user = medical_leave.employee
        ctx = {
            "medical_leave": medical_leave,
            'user': user,
        }
        return render(request, "office_tool_app/medicalleave_confirm_delete.html", ctx)

    def post(self, request, pk):
        medical_leave = get_object_or_404(MedicalLeave, pk=pk)
        medical_leave.delete()
        user = medical_leave.employee
        print(user)
        messages.success(request, f"{medical_leave} has been deleted")
        return redirect('manage-detail', user.username)


class ManageView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        group_one = Group.objects.get(pk=1)
        group_one_users = group_one.user_set.all()
        group_two = Group.objects.get(pk=2)
        group_two_users = group_two.user_set.all()
        vacations = Vacation.objects.all().filter(employee__group=group_two).filter(vacation_from__gte=today)
        delegations = Delegation.objects.all().filter(employee__group=group_two).filter(start_date__gte=today)
        ctx = {
            'group_one': group_one,
            'group_one_users': group_one_users,
            'group_two': group_two,
            'group_two_users': group_two_users,
            'vacations': vacations,
            'delegations': delegations,
            'user': user,
        }
        return render(request, 'office_tool_app/manage.html', ctx)


class ManageDetailView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def get(self, request, username):
        user = User.objects.get(username=username)
        today = str(datetime.now().date())
        group = user.group
        group_users = group.user_set.all()
        medicals = user.medical_employee.all()
        vacations = user.vacation_employee.filter(status='pending').filter(vacation_from__gte=today)
        messages = user.messages_to_employee.all().order_by('-sending_date')
        delegations = user.delegation_employee.filter(status='pending').filter(start_date__gte=today)
        vacations_accepted = user.vacation_employee.filter(status='accepted').filter(vacation_from__gte=today)
        delegations_accepted = user.delegation_employee.filter(status='accepted').filter(start_date__gte=today)

        ctx = {
            'group_users': group_users,
            'vacations': vacations,
            'messages': messages,
            'delegations': delegations,
            'medicals': medicals,
            'user': user,
            'vacations_accepted': vacations_accepted,
            'delegations_accepted': delegations_accepted,
        }
        return render(request, 'office_tool_app/manageDetail.html', ctx)