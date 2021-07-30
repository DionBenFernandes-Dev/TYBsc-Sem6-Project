from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class ChatMessageForm(ModelForm):
	class Meta:
		model = ChatMessage
		fields = ['member_message']

class TeamForm(ModelForm):
	class Meta:
		model = Team
		fields = ['name','skill']

class SkillForm(ModelForm):
	class Meta:
		model = Skill
		fields = ['name']

class MemberForm(ModelForm):
	class Meta:
		model = Member
		fields = [
					'first_name',
					'middle_name',
					'last_name',
					'profile_image',
					'email',
					'skills',
				]

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']