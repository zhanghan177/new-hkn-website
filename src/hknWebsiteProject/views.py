from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login
from utils import has_complete_profile
from django.core.mail import send_mail

from users.models import Member
from electeeManagement.models import Electee
from users.forms import NewMemberForm
from hknWebsiteProject import settings
class MyError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def home(request):
	context = {}
	if not request.user.is_anonymous():
		# display prompt to ask member to complete their profile
		if not has_complete_profile(request.user.username):
			context = {
				'has_not_complete_profile' : True
			}
	return render(request, "home.html", context)
	
def about(request):
	return render(request, "about.html", {})

def corporate(request):
	return render(request, "corporate.html", {})

def make_members(form, electee):
	uniqnames = form.cleaned_data.get('new_members').split(',')
	try:
		# validate each submitted uniqname to make sure that a member 
		# 	with that uniqname does not alread exist, and that it is
		# 	alphabetic and a valid number of characters
		for name in uniqnames:
			if Member.objects.filter(uniqname = name).exists():
				raise MyError('Uniqname already exists')
	except MyError:
		context = {
			'error' : True,
			'error_msg' : 'Uniqname ' + name + ' alread exists!' 
		}
	else:
		# display message saying members were successfully submitted
		for name in uniqnames:	
			m = Member(uniqname = name)
			if electee:
				m.status = 'E'
			else:
				m.status = 'A'
			m.save()

			if electee:
				Electee(member = m).save()

			subject = '[HKN] Welcome to the HKN Beta Epsilon Website'
			message = welcome_msg
			from_email = settings.EMAIL_HOST_USER
			to_email = [name + '@umich.edu']

			send_mail(subject, 
					  message, 
					  from_email, 
					  to_email,
					  fail_silently=False)

def create_new_members(request):
	context = {}
	context['new_members_submitted'] = False

	form_electee = NewMemberForm(request.POST or None, prefix='electee')
	form_active = NewMemberForm(request.POST or None, prefix='active')

	if form_electee.is_valid():
		make_members(form_electee, True)
		form_electee = NewMemberForm()	
		context['new_members_submitted'] = True

	if form_active.is_valid():
		make_members(form_active, False)
		form_active = NewMemberForm()	
		context['new_members_submitted'] = True

	context['form_electee'] = form_electee
	context['form_active'] = form_active

	return render(request, "create_new_members.html", context)

def login_user(request):
	email = request.user.email
	email_base, provider = email.split('@')
	if not provider == 'umich.edu':
		request = badUser(request)
	else:
		try:
			m = Member.objects.get(uniqname = email_base)
			
			# If the user doesn't have name in thier profile, defualt to the 
			# name registered with their login info
			if not m.first_name:
				m.first_name = request.user.first_name
			if not m.last_name:
				m.last_name = request.user.last_name
			m.save()
		except Member.DoesNotExist:
			request = badUser(request)

	return redirect('/')

def badUser(request):
	User.objects.get(username__exact=request.user).delete()
	return AnonymousUser()


welcome_msg = '''
Welcome to the HKN website! An accout has been created for you.

Please go to hkn.eecs.umich.edu and log in with your umich account to complete your profile. Once you complete your profile, you will appear in the memeber list and you resume will be included in the resume book.

Thanks,
HKN Website
'''