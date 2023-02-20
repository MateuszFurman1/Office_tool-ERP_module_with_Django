from datetime import datetime

import vacation as vacation
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from office_tool_app.form import (AddressCoreForm, AddressHomeForm,
                                  DelegationForm, LoginForm, MedicalLeaveForm,
                                  RegistrationForm, UserUpdateForm,
                                  VacationForm)
from office_tool_app.models import (AddressCore, AddressHome, Delegation,
                                    Group, MedicalLeave, Messages, User,
                                    Vacation)


class HomeView(LoginRequiredMixin, View):
    '''
    Display pending delegations and vacations request, messages received from manager
    and employees from user group.
    Login require
    return django home.html templates
    '''
    login_url = "/login/"

    def get(self, request):
        user = request.user
        ctx = {}
        if user.is_authenticated:
            today = str(datetime.now().date())
            group = user.group
            # group_users = group.user_set.all()
            group_users = User.objects.filter(
                group=group).exclude(first_name=user.first_name)
            vacations = user.vacation_employee.filter(
                status='pending').filter(vacation_from__gte=today)
            messages = user.messages_to_employee.all().order_by(
                '-sending_date')[:5]
            delegations = user.delegation_employee.filter(
                status='pending').filter(start_date__gte=today)

            ctx = {
                'group_users': group_users,
                'vacations': vacations,
                'messages': messages,
                'delegations': delegations,
            }

        return render(request, "office_tool_app/Home.html", ctx)


class RegistrationView(View):
    '''
    Registration views. Generate form to fill information and save them to
    postgres database
    if success:
    return redirect to login view
    if error:
    return form again
    '''

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
    '''
    Render login form. On post side check password and authorize user.
    If password is the same in both form fields:
    return redirect to home view
    If password is wrong:
    return form again
    '''

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
    '''
    Logout user. After logout. Display success message
    return redirect to login views
    '''

    def get(self, request):
        logout(request)
        messages.success(request, "Logout successfully")
        return redirect('login')


class ProfileView(LoginRequiredMixin, View):
    '''
    Display all information about login user. Pass instance with current login user
    Load information from 3 models: User, AddressHome, AddressCore
    return profile template
    '''
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
    '''
    Display detail information about current login user vacations.
    Display pending vacation reguests, historical vacation, approval future vacation
    return vacation template
    '''
    login_url = "/login/"

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        vacations_today = user.vacation_employee.filter(
            status='pending').filter(vacation_from__gte=today)
        vacations_past = user.vacation_employee.filter(
            status='accepted').filter(vacation_from__lte=today)[:5]
        vacations_future = user.vacation_employee.filter(
            status='accepted').filter(vacation_from__gt=today)
        ctx = {
            'vacations_today': vacations_today,
            'vacations_past': vacations_past,
            'vacations_future': vacations_future,
        }
        return render(request, 'office_tool_app/vacationDetail.html', ctx)


class VacationCreateView(LoginRequiredMixin, View):
    '''
    Create vacation instance for current login user.
    Validate:
    - replacement employee can not be login user,
    - if vacation request already exist in database for this period of time,
    - if vacation date is not from the past
    if success return redirect to vacation detail view
    if error return form again
    '''

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
            all_delegations = Delegation.objects.filter(employee=user)
            all_vacations = Vacation.objects.filter(employee=user)
            vacation_from = form.cleaned_data['vacation_from']
            vacation_to = form.cleaned_data['vacation_to']
            start_date = form.cleaned_data['vacation_from']
            end_date = form.cleaned_data['vacation_to']
            for one_delegations in all_delegations:
                if (one_delegations.start_date <= start_date) and (one_delegations.end_date >= start_date) or \
                        (one_delegations.start_date <= end_date) and (one_delegations.end_date >= end_date):
                    messages.error(
                        request, "Delegation in this date already exist!")
                    return render(request, 'office_tool_app/form2.html', ctx)
            for one_vacation in all_vacations:
                if (one_vacation.vacation_from <= vacation_from) and (one_vacation.vacation_to >= vacation_from) or \
                        (one_vacation.vacation_from <= vacation_to) and (one_vacation.vacation_to >= vacation_to):
                    messages.error(
                        request, "Vacation in this date already exist!")
                    return render(request, 'office_tool_app/form2.html', ctx)
            if request.user == vacation.replacement:
                messages.error(
                    request, "Replacement employee validation error!")
                return render(request, 'office_tool_app/form2.html', ctx)
            vacation.status = 'pending'
            vacation.save()
            return redirect('vacation-detail')

        return render(request, 'office_tool_app/form2.html', ctx)


class VacationDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Generic view which delete pointed vacation.
    parm: primary key of vacation
    return redirect to vacation-detail
    '''
    model = Vacation
    success_url = reverse_lazy("vacation-detail")


class VacationAcceptView(PermissionRequiredMixin, View):
    '''
    View with permission to manage employees.
    Get the vacation pending request form employee and change status to accepted.
    Also created message to him with information about accepting request.
    parm: primary key of vacation
    return redirect to manage-detail view with parm. username
    '''
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
    '''
    View with permission to manage employees.
    Get the vacation pending request form employee and change status to rejected.
    Also created message to him with information about rejected request.
    parm: primary key of vacation
    return redirect to manage-detail view with parm. username
    '''
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
    '''
    Display detail information about current login user delegation.
    Display pending delegation reguests, historical delegation, approval future delegation
    return delegation template
    '''
    login_url = "/login/"

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        delegations_today = user.delegation_employee.filter(
            status='pending').filter(start_date__gte=today)
        delegations_past = user.delegation_employee.filter(
            status='accepted').filter(start_date__lte=today)[:5]
        delegations_future = user.delegation_employee.filter(
            status='accepted').filter(start_date__gt=today)
        ctx = {
            'delegations_today': delegations_today,
            'delegations_past': delegations_past,
            'delegations_future': delegations_future,
        }
        return render(request, 'office_tool_app/delegationDetail.html', ctx)


class DelegationCreateView(LoginRequiredMixin, View):
    '''
    Create delegation instance for current login user.
    Validate:
    - if delegation request already exist in database for this period of time,
    - if delegation date is not from the past
    if success return redirect to delegation detail view
    if error return form again
    '''
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
            vacation.employee = user
            all_vacations = Vacation.objects.filter(employee=user)
            vacation_from = form.cleaned_data['start_date']
            vacation_to = form.cleaned_data['end_date']
            for one_vacation in all_vacations:
                if (one_vacation.vacation_from <= vacation_from) and (one_vacation.vacation_to >= vacation_from) or \
                        (one_vacation.vacation_from <= vacation_to) and (one_vacation.vacation_to >= vacation_to):
                    messages.error(
                        request, "Vacation in this date already exist!")
                    return render(request, 'office_tool_app/form2.html', ctx)
            for one_delegations in all_delegations:
                if (one_delegations.start_date <= start_date) and (one_delegations.end_date >= start_date) or \
                        (one_delegations.start_date <= end_date) and (one_delegations.end_date >= end_date):
                    messages.error(
                        request, "Delegation in this date already exist!")
                    return render(request, 'office_tool_app/form2.html', ctx)
            delegation.status = 'pending'
            delegation.save()
            return redirect('delegation-detail')

        return render(request, 'office_tool_app/form2.html', ctx)


class DelegationDeleteView(LoginRequiredMixin, DeleteView):
    '''
    Generic view which delete pointed delegation.
    parm: primary key of delegation
    return redirect to delegation-detail
    '''
    model = Delegation
    success_url = reverse_lazy("delegation-detail")


class DelegationAcceptView(PermissionRequiredMixin, View):
    '''
    View with permission to manage employees.
    Get the delegation pending request form employee and change status to accepted.
    Also created message to him with information about accepting request.
    parm: primary key of delegation
    return redirect to manage-detail view with parm. username
    '''
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
    '''
    View with permission to manage employees.
    Get the delegation pending request form employee and change status to rejected.
    Also created message to him with information about rejected request.
    parm: primary key of delegation
    return redirect to manage-detail view with parm. username
    '''
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
    '''
    Display detail information about current login user medical leave.
    return medical leave template
    '''
    login_url = "/login/"

    def get(self, request):
        user = request.user
        medicals = user.medical_employee.all()[:5]
        ctx = {
            'medicals': medicals

        }
        return render(request, 'office_tool_app/MedicalLeave.html', ctx)


class MedicalLeaveCreateView(PermissionRequiredMixin, View):
    '''
    Create medical leave instance for current login user.
    Validate:
    - if medical leave request already exist in database for this period of time,
    - if medical leave date is not from the past
    if success return redirect to manage detail view with parm. username
    if error return form again
    '''
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
                    messages.error(
                        request, "Medical Leave in this date already exist!")
                    return render(request, 'office_tool_app/form2.html', ctx)
            medical_leave.save()
            return redirect('manage-detail', user.username)

        return render(request, "office_tool_app/form2.html", ctx)


class MedicalDeleteView(LoginRequiredMixin, View):
    '''
    Delete pointed medical leave.
    parm: primary key of medical leave
    return redirect to manage detail view with parm. username
    '''
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
    '''
    Display detail information about current login user messages.
    return messages template
    '''
    login_url = "/login/"

    def get(self, request):
        user = request.user
        messages = Messages.objects.filter(to_employee=user)[:10]
        ctx = {
            'messages': messages,
        }
        return render(request, 'office_tool_app/messagesDetail.html', ctx)


class ManageView(PermissionRequiredMixin, View):
    '''
    Require permission for manage employees
    Manage view for manager to managing of subordinates members.
    Display group name and members of manager group.
    Display who of subordinates members is already on vacation and delegations
    Display subordinates members.
    return manage templates
    '''
    permission_required = 'can_manage_employees'

    def get(self, request):
        user = request.user
        today = str(datetime.now().date())
        group = Group.objects.filter(name='employee').first()
        group_manage = Group.objects.filter(name='manager').first()
        group_manage_users = group_manage.user_set.all()
        group_users = group.user_set.all()
        vacations = Vacation.objects.all().filter(
            employee__group=group).filter(vacation_from__gte=today)
        vacations_list = []
        for i in vacations:
            if i.employee not in vacations_list:
                vacations_list.append(i.employee)
        delegations = Delegation.objects.all().filter(
            employee__group=group).filter(start_date__gte=today)
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
    '''
    Required permission for manage employees.
    Display pending delegation and vacation request for accepting by manager.
    Display all approved delegation, vacation and medical leave for employee
    parm. user username
    return manage detail template
    '''
    permission_required = 'can_manage_employees'

    def get(self, request, username):
        user = User.objects.get(username=username)
        today = str(datetime.now().date())
        group = user.group
        group_users = group.user_set.all()
        medicals = user.medical_employee.all()[:5]
        vacations = user.vacation_employee.filter(
            status='pending').filter(vacation_from__gte=today)
        messages = user.messages_to_employee.all().order_by('-sending_date')
        delegations = user.delegation_employee.filter(
            status='pending').filter(start_date__gte=today)
        vacations_accepted = user.vacation_employee.filter(
            status='accepted').filter(vacation_from__gte=today)[:5]
        delegations_accepted = user.delegation_employee.filter(
            status='accepted').filter(start_date__gte=today)[:5]

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
