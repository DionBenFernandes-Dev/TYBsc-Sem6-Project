from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import time

# Create your views here.
from .models import *
from .forms import *
# from .filters import OrderFilter

def registerPage(request):
	print('RegisterPage\n')
	if request.user.is_authenticated:
		return redirect('home',request.user.username)
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				email = form.cleaned_data.get('email')
				messages.success(request, 'Account was created for ' + user)
				member,status = Member.objects.get_or_create(user_name=user,email=email)
				print('Member:',member)
				print('Status:',status)
				return redirect('login')

		context = {'form':form}
		return render(request, 'teams/register.html', context)

def loginPage(request):
	print('LoginPage\n')
	if request.user.is_authenticated:
		#print('login: '+request.user.username)
		return redirect('home',request.user.username)
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home',username)
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'teams/login.html', context)

def logoutUser(request):
	print('LogoutPage\n')
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def profile(request,pk_test):
	print('ProfilePage\n')
	user = User.objects.get(username=pk_test)
	member = Member.objects.get(user_name=user.username)

	context = {
					"member":member,
					"user":user
	}
	return render(request,'teams/profile.html',context)

@login_required(login_url='login')
def profileUpdate(request,pk_test):
	print('ProfileUpdatePage\n')
	user = User.objects.get(username=pk_test)
	member = Member.objects.get(user_name=user.username)
	print('Member',member)

	form = MemberForm(instance=member)
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = MemberForm(request.POST,request.FILES,instance=member)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			user.email = email
			user.save()
			return redirect('profile',user.username)
	context = {
					"form":form,
					"member":member,
					"user":user
	}
	return render(request,'teams/profileUpdate.html',context)

@login_required(login_url='login')
def home(request,pk_test):
	print('HomePage\n')
	user = User.objects.get(username=pk_test)
	m = Member.objects.get(user_name=pk_test)
	if (m.first_name == None ) :
		return redirect('profileUpdate',user.username)	
	else:
		member = Member.objects.get(user_name=pk_test)
		
		team = Team.objects.all()
		mteam = member.teams.all()
		mteam_count = mteam.count()
		pteam = team.filter(owner=member.user_name)
		pteam_count = pteam.count()
		print("Member:",member)
		print('Teams:',team)
		print('Member-Team:',mteam)
		print('Create-Team:',pteam)
		print('Create-Team-Count:',pteam_count)
		print('Member-Team-Count:',mteam_count)

		context = {
					'member':member,
					'user':user,
					'team':team,
					'pteam_count':pteam_count,
					'mteam_count':mteam_count,
				}
	return render(request,'teams/home.html',context)

@login_required(login_url='login')
def team(request,pk_test):
	print('TeamPage\n')
	user = User.objects.get(username=pk_test)
	member = Member.objects.get(user_name=pk_test)
	
	team = Team.objects.all()
	mteam = member.teams.all()
	mteam_count = mteam.count()
	pteam = team.filter(owner=member.user_name)
	pteam_count = pteam.count()
	print('Teams:',team)
	print('Member-Team:',mteam)
	print('Create-Team:',pteam)
	print('Create-Team-Count:',pteam_count)
	print('Member-Team-Count:',mteam_count)

	rs = []
	for s in member.skills.all():
		rs.append(s)
	print(rs)

	rt_test = team.filter(skill__in=rs)
	print(rt_test)
	rt = []
	for i in rt_test:
		if i not in mteam and i not in rt:
			print(i)
			rt.append(i)
	print(rt)

	context = {
				'member':member,
				'user':user,
				'team':team,
				'rs':rs,
				'rt':rt,
				'pteam_count':pteam_count,
				'mteam_count':mteam_count,
			}
	return render(request,'teams/team.html',context)

@login_required(login_url='login')
def teamCreate(request,pk_test):
	print('TeamCreatePage\n')
	user = User.objects.get(username=pk_test)
	member = Member.objects.get(user_name=pk_test)
	team = Team.objects.all()
	team_chatrooms = TeamChatRoom.objects.all()

	tg = []
	for i in team.all():
		tg.append(i.name)
	print(tg)

	form = TeamForm()
	if request.method == 'POST':
		form = TeamForm(request.POST)
		messages.info(request,'')
		if form.is_valid():
			t = form.cleaned_data.get('name')
			if t in tg:
				messages.info(request, t+' already exists')
			else:
				form.save()
				nt = team.get(name=t)
				nt.owner = user.username
				nt.save()
				member.teams.add(nt)
				messages.success(request, t + ' has been created.')
				chatroom = team_chatrooms.create(team_chat_name=team.get(name=t))
				return redirect('team', user.username )

	context = {
				'form':form,
	}
	return render(request, 'teams/teamCreate.html', context)

@login_required(login_url='login')
def skillCreate(request,pk_user):
	print('SkillCreatePage\n')
	user = User.objects.get(username=pk_user)
	skills = Skill.objects.all()
	form = SkillForm()
	if request.method == 'POST':
		form = SkillForm(request.POST)
		messages.info(request,'')
		if form.is_valid():
			skill = form.cleaned_data.get('name').upper()
			if (skills.filter(name=skill)):
				messages.info(request, skill+' already exists')
			else:
				form.save()
				time.sleep(3)
				messages.success(request, skill + ' has been added. You can update your Profile.')
				return redirect('profileUpdate',user.username)

	context = {
				'form':form,
				'skills':skills
	}
	return render(request, 'teams/skillCreate.html', context)

@login_required(login_url='login')
def joinTeam(request,pk_user,pk_team):
	print('JoinTeamPage\n')
	print(pk_user)
	print(pk_team)
	member = Member.objects.get(user_name=pk_user)
	team = Team.objects.get(name=pk_team)
	if request.method == "POST":
		member.teams.add(team)
		return redirect('/')
	context = {
				"member":member,
				"team":team,
	}
	return render(request,'teams/jointeam.html',context)

@login_required(login_url='login')
def leaveTeam(request,pk_user,pk_team):
	print('LeaveTeamPage\n')
	print(pk_user)
	print(pk_team)
	member = Member.objects.get(user_name=pk_user)
	team = Team.objects.get(name=pk_team)
	if request.method == "POST":
		member.teams.remove(team)
		if not team.member_set.all():
			team.delete()
		else:
			team.owner = team.member_set.first().user_name
			team.save()
		return redirect('/')

	context = {
				"member":member,
				"team":team,
	}
	return render(request,'teams/leaveteam.html',context)

@login_required(login_url='login')
def deleteTeam(request,pk_user,pk_team):
	print('DeleteTeamPage\n')
	print(pk_user)
	print(pk_team)
	member = Member.objects.get(user_name=pk_user)
	team = Team.objects.get(name=pk_team)
	if request.method == "POST":
		t = team.name
		team.delete()
		messages.success(request, t + ' has been deleted.')
		return redirect('/')

	context = {
				"member":member,
				"team":team,
	}
	return render(request,'teams/deleteteam.html',context)

@login_required(login_url='login')
def teamChatRoom(request,pk_user,pk_team):
	print("TeamChatRoomPage:\n")
	user = User.objects.get(username=pk_user)
	member = Member.objects.get(user_name=user.username)
	team = Team.objects.get(name=pk_team)
	team_chatrooms = TeamChatRoom.objects.all()
	team_chat_messages = ChatMessage.objects.all()

	if (member.teams.filter(name=team.name)):
		print("In ChatRoom")
		member_list = team.member_set.all()
		team_skill_list = team.skill.all()

		chatroom = team_chatrooms.get(team_chat_name=team.id)
		chat_messages = team_chat_messages.filter(team_name=team.id).order_by('date_created')

		print("Current Member:",member.user_name)

		print("ChatRoom:",chatroom)
		print("Chat-Messages:",chat_messages)

		print("Team-Name:",team)
		print("Member-List:",member_list)
		print("Team-Skill-List:",team_skill_list)

		
		display_chat_messages = []
		count = 0
		for i in reversed(chat_messages):
			display_chat_messages.append(i)
			if count == 15:
				break
			else:
				count += 1

		form = ChatMessageForm()
		if request.method == 'POST':
			#print('Printing POST:', request.POST)
			new = team_chat_messages.create(team_name=chatroom,member_username=member.user_name)
			form = ChatMessageForm(request.POST,instance=new)
			print('Form:',form)
			print("Form-Valid:",form.is_valid())
			print("Form-Error:",form.errors)
			if form.is_valid():
				form.save()
				return redirect('teamChatRoom',pk_user=pk_user,pk_team=pk_team)

		context = {
					"team":team,
					"member_list":member_list,
					"team_skill_list":team_skill_list,
					"member":member,
					"chatroom":chatroom,
					"chat_messages":chat_messages,
					"form":form,
					"display_chat_messages":display_chat_messages,
					"user":user,
		}
	return render(request,"teams/chatroom.html",context) 

@login_required(login_url='login')
def search(request,pk_user):
	print('SearchPage:\n')
	user = User.objects.get(username=pk_user)
	member_user = Member.objects.get(user_name=user.username)
	member_list=[]
	team_list=[]
	if request.method == 'GET':
		#print('Printing GET:', request.GET)
		word = request.GET.get('search')
		print("Search:",word)
		if word != None:
			member_list = Member.objects.filter(user_name__icontains=word)
			print("Member-List:",member_list)
			team_list = Team.objects.filter(name__icontains=word)
			print("Team-List:",team_list)
			
	context = {
				"member_list":member_list,
				"team_list":team_list,
				"word":word,
				"user":user,
				"member_user":member_user,
			}
	return render(request,"teams/search.html",context)

@login_required(login_url='login')
def removeMember(request,pk_user,pk_team,pk_member):
	print('RemoveMemberPage\n')
	print(pk_user)
	print(pk_team)
	print(pk_member)
	user = User.objects.get(username = pk_user)
	member = Member.objects.get(user_name=pk_member)
	team = Team.objects.get(name=pk_team)
	if request.method == "POST":
		member.teams.remove(team)
		return redirect('teamChatRoom',pk_user=user.username,pk_team=team.name)

	context = {
				"member":member,
				"team":team,
				"user":user,
	}
	return render(request,'teams/removemember.html',context)

@login_required(login_url='login')
def profileMember(request,pk_user,pk_member):
	print('ProfileMemberPage\n')

	user = User.objects.get(username=pk_user)
	member = Member.objects.get(user_name=pk_member)

	context = {
					"member":member,
					"user":user
	}
	return render(request,'teams/profileMember.html',context)





# class SearchView(ListView):
#     model = Member
#     template_name = 'search.html'
#     context_object_name = 'all_search_results'

#     def get_queryset(self):
#        result = super(SearchView, self).get_queryset()
#        query = self.request.GET.get('search')
#        if query:
#           postresult = Member.objects.filter(title__contains=query)
#           result = postresult
#        else:
#            result = None
#        return result