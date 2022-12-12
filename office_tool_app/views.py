from datetime import datetime

import vacation as vacation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DeleteView

from office_tool_app.form import RegistrationForm, LoginForm, UserUpdateForm, AddressHomeForm, \
    AddressCoreForm, MedicalLeaveForm, DelegationForm, VacationForm
from office_tool_app.models import User, Group, AddressHome, AddressCore, Vacation, Delegation, MedicalLeave, Messages


class HomeView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        ctx = {}
        if user.is_authenticated:
            today = str(datetime.now().date())
            group = user.group
            # group_users = group.user_set.all()
            group_users = User.objects.filter(group=group).exclude(first_name=user.first_name)
            vacations = user.vacation_employee.filter(status='pending').filter(vacation_from__gte=today)
            messages = user.messages_to_employee.all().order_by('-sending_date')[:5]
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
        vacations_past = user.vacation_employee.filter(status='accepted').filter(vacation_from__lte=today)[:5]
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
        ctx = {
            'form': form,
            'user': user,
        }
        if form.is_valid():
            vacation = form.save(commit=False)
            vacation.employee = user
            all_vacations = Vacation.objects.filter(employee=user)
            vacation_from = form.cleaned_data['vacation_from']
            vacation_to = form.cleaned_data['vacation_to']
            for one_vacation in all_vacations:
                if (one_vacation.vacation_from <= vacation_from) and (one_vacation.vacation_to >= vacation_from) or \
                        (one_vacation.vacation_from <= vacation_to) and (one_vacation.vacation_to >= vacation_to):
                    messages.error(request, "Vacation in this date already exist!")
                    return render(request, 'office_tool_app/form2.html', ctx)
            if request.user == vacation.replacement:
                messages.error(request, "Replacement employee validation error!")
                return render(request, 'office_tool_app/form2.html', ctx)
            vacation.status = 'pending'
            vacation.save()
            return redirect('vacation-detail')

        return render(request, 'office_tool_app/form2.html', ctx)


class VacationDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacation
    success_url = reverse_lazy("vacation-detail")


class VacationAcceptView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def get(self, request, pk):
        vacation = get_object_or_404(Vacation, pk=pk)
        user = vacation.employee
        ctx = {
            "vacation": vacation,
            'user': user,
        }
        return render(request, "office_tool_app/vacation_confirm_accept.html", ctx)

    def post(self, request, pk):
        vacation = Vacation.objects.get(id=pk)
        vacation.status = 'accepted'
        vacation.save()
        user_reciver = vacation.employee
        user_sender = request.user
        today = str(datetime.now().date())
        message = f"Your vacation from: {vacation.vacation_from} to {vacation.vacation_to} has been accepted by " \
                  f"{user_sender}"
        Messages.objects.create(from_employee=user_sender, to_employee=user_reciver, sending_date=today,
                                message=message)

        return redirect('manage-detail', user_reciver.username)


class VacationRejectView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def get(self, request, pk):
        vacation = get_object_or_404(Vacation, pk=pk)
        user = vacation.employee
        ctx = {
            "vacation": vacation,
            'user': user,
        }
        return render(request, "office_tool_app/vacation_confirm_accept.html", ctx)

    def post(self, request, pk):
        vacation = Vacation.objects.get(id=pk)
        vacation.status = 'accepted'
        vacation.save()
        user_reciver = vacation.employee
        user_sender = request.user
        today = str(datetime.now().date())
        message = f"Your vacation from: {vacation.vacation_from} to {vacation.vacation_to} has been rejected by " \
                  f"{user_sender}"
        Messages.objects.create(from_employee=user_sender, to_employee=user_reciver, sending_date=today,
                                message=message)
        return redirect('manage-detail', user_reciver.username)


class DelegationDetailView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        delegations_today = user.delegation_employee.filter(status='pending').filter(start_date__gte=today)
        delegations_past = user.delegation_employee.filter(status='accepted').filter(start_date__lte=today)[:5]
        delegations_future = user.delegation_employee.filter(status='accepted').filter(start_date__gt=today)
        ctx = {
            'delegations_today': delegations_today,
            'delegations_past': delegations_past,
            'delegations_future': delegations_future,
        }
        return render(request, 'office_tool_app/delegationDetail.html', ctx)


class DelegationCreateView(LoginRequiredMixin, View):
    login_url = "/login/"

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
        ctx = {
            'form': form,
            'user': user,
        }
        if form.is_valid():
            delegation = form.save(commit=False)
            delegation.employee = user
            all_delegations = Delegation.objects.filter(employee=user)
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            for one_delegations in all_delegations:
                if (one_delegations.start_date <= start_date) and (one_delegations.end_date >= start_date) or \
                        (one_delegations.start_date <= end_date) and (one_delegations.end_date >= end_date):
                    messages.error(request, "Delegation in this date already exist!")
                    return render(request, 'office_tool_app/form2.html', ctx)
            delegation.status = 'pending'
            delegation.save()
            return redirect('delegation-detail')

        return render(request, 'office_tool_app/form2.html', ctx)


class DelegationDeleteView(LoginRequiredMixin, DeleteView):
    model = Delegation
    success_url = reverse_lazy("delegation-detail")


class DelegationAcceptView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

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
        user_reciver = delegation.employee
        user_sender = request.user
        today = str(datetime.now().date())
        message = f"Your delegation from: {delegation.start_date} to {delegation.end_date} to " \
                  f"{delegation.delegation_country} has been accepted by " \
                  f"{user_sender}"
        Messages.objects.create(from_employee=user_sender, to_employee=user_reciver, sending_date=today,
                                message=message)
        return redirect('manage-detail', user_reciver.username)


class DelegationRejectView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

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
        user_reciver = delegation.employee
        user_sender = request.user
        today = str(datetime.now().date())
        message = f"Your delegation from: {delegation.start_date} to {delegation.end_date} to " \
                  f"{delegation.delegation_country} has been rejected by " \
                  f"{user_sender}"
        Messages.objects.create(from_employee=user_sender, to_employee=user_reciver, sending_date=today,
                                message=message)
        return redirect('manage-detail', user_reciver.username)


class MedicalLeaveView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        medicals = user.medical_employee.all()[:5]
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
        ctx = {
            "form": form,
            'user': user,
        }
        if form.is_valid():
            medical_leave = form.save(commit=False)
            medical_leave.employee = user
            all_medical_leave = MedicalLeave.objects.filter(employee=user)
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            for one_medical_leave in all_medical_leave:
                if (one_medical_leave.from_date <= from_date) and (one_medical_leave.to_date >= from_date) or \
                        (one_medical_leave.from_date <= to_date) and (one_medical_leave.to_date >= to_date):
                    messages.error(request, "Medical Leave in this date already exist!")
                    return render(request, 'office_tool_app/form2.html', ctx)
            medical_leave.save()
            return redirect('manage-detail', user.username)

        return render(request, "office_tool_app/form2.html", ctx)


class MedicalDeleteView(LoginRequiredMixin, View):
    login_url = "/login/"

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
        messages.success(request, f"{medical_leave} has been deleted")
        return redirect('manage-detail', user.username)


class MessagesView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        user = request.user
        messages = Messages.objects.filter(to_employee=user)[:10]
        ctx = {
            'messages': messages,
        }
        return render(request, 'office_tool_app/messagesDetail.html', ctx)


class ManageView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        group = Group.objects.get(name='employee')
        group_manage = Group.objects.get(name='manager')
        group_manage_users = group_manage.user_set.all()
        group_users = group.user_set.all()
        vacations = Vacation.objects.all().filter(employee__group=group).filter(vacation_from__gte=today)
        vacations_list = []
        for i in vacations:
            if i.employee not in vacations_list:
                vacations_list.append(i.employee)
        delegations = Delegation.objects.all().filter(employee__group=group).filter(start_date__gte=today)
        delegations_list = []
        for i in delegations:
            if i.employee not in delegations_list:
                delegations_list.append(i.employee)
        ctx = {
            'group': group,
            'group_users': group_users,
            'group_manage': group_manage,
            'group_manage_users': group_manage_users,
            'vacations': vacations,
            'delegations': delegations,
            'user': user,
            'delegations_list': delegations_list,
            'vacations_list': vacations_list,

        }
        return render(request, 'office_tool_app/manage.html', ctx)


class ManageDetailView(PermissionRequiredMixin, View):
    permission_required = 'can_manage_employees'

    def get(self, request, username):
        user = User.objects.get(username=username)
        today = str(datetime.now().date())
        group = user.group
        group_users = group.user_set.all()
        medicals = user.medical_employee.all()[:5]
        vacations = user.vacation_employee.filter(status='pending').filter(vacation_from__gte=today)
        messages = user.messages_to_employee.all().order_by('-sending_date')
        delegations = user.delegation_employee.filter(status='pending').filter(start_date__gte=today)
        vacations_accepted = user.vacation_employee.filter(status='accepted').filter(vacation_from__gte=today)[:5]
        delegations_accepted = user.delegation_employee.filter(status='accepted').filter(start_date__gte=today)[:5]

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