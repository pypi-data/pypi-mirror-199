import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from employee.models import AddressTL, ContactInfo, CurEmpDivision, CurEmpPosition, DriverLicence,\
	EmpDependency, FIDNumber, FormalEducation, IIDNumber, LIDNumber, LocationInter, LocationTL,\
	NonFormalEducation, Photo, WorkExperience, EmployeeUser, EmpSignature,EmpSpecialize, EmpLanguage
from contract.models import Contract, EmpSalary, EmpPlacement
from users.forms import UserUpdateForm, UserUpdateForm2
from settings_app.user_utils import c_staff

@login_required
def ProfileDetail(request):
	group = request.user.groups.all()[0].name
	objects = c_staff(request.user)
	
	fidnum = FIDNumber.objects.filter(employee=objects).first()
	lidnum = LIDNumber.objects.filter(employee=objects).first()
	iidnum = IIDNumber.objects.filter(employee=objects).first()
	contactinfo = ContactInfo.objects.filter(employee=objects).first()
	loctl = LocationTL.objects.filter(employee=objects).first()
	addtl = AddressTL.objects.filter(employee=objects).first()
	locinter = LocationInter.objects.filter(employee=objects).first()
	img = Photo.objects.filter(employee=objects).first()
	driver = DriverLicence.objects.filter(employee=objects).first()
	empcont = Contract.objects.filter(employee=objects, is_active=True).last()
	empsalary = EmpSalary.objects.filter(contract=empcont).last()
	signature = EmpSignature.objects.filter(employee=objects).last()
	emppos = CurEmpPosition.objects.filter(employee=objects).first()
	empdiv = CurEmpDivision.objects.filter(employee=objects).first()
	empdepend = EmpDependency.objects.filter(employee=objects).all()
	formaledu = FormalEducation.objects.filter(employee=objects).last()
	empplacement = EmpPlacement.objects.filter(employee=objects, is_active=True).last()
	nonformaledu = NonFormalEducation.objects.filter(employee=objects).last()
	workexp = WorkExperience.objects.filter(employee=objects).last()
	emplang = EmpLanguage.objects.filter(employee=objects).all()
	empspecs = EmpSpecialize.objects.filter(employee=objects).all()
	context = {
		'group': group, 'objects': objects, 'fidnum': fidnum, 'lidnum': lidnum, 'iidnum': iidnum,
		'contactinfo': contactinfo, 'loctl':loctl, 'addtl': addtl, 'locinter':locinter, 'img': img,
		'empcont': empcont, 'empsalary': empsalary, 'emppos': emppos, 'empdiv': empdiv,
		'formaledu': formaledu, 'nonformaledu': nonformaledu, 'workexp': workexp,
		'empdepend': empdepend, 'driver': driver, 'emplang': emplang, 'empspecs': empspecs,
		'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu', 'empplacement':empplacement,
		 'employee': objects, 'signature':signature
	}
	return render(request, 'profile/profile.html', context)

@login_required
def AccountUpdate(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		if group == "students":
			u_form = UserUpdateForm(request.POST, instance=request.user)
		else:
			u_form = UserUpdateForm2(request.POST, instance=request.user)
		if u_form.is_valid():
			u_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('user-account')
	else:
		if group == "students":
			u_form = UserUpdateForm(instance=request.user)
		else:
			u_form = UserUpdateForm2(instance=request.user)
	context = {
		'u_form': u_form,
		'title': 'Account Info', 'legend': 'Account Info',
	}
	return render(request, 'auth/account.html', context)

class UserPasswordChangeView(PasswordChangeView):
	template_name = 'auth/change_password.html'
	success_url = reverse_lazy('user-change-password-done')

class UserPasswordChangeDoneView(PasswordResetDoneView):
	template_name = 'auth/change_password_done.html'