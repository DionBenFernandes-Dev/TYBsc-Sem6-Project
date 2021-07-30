from django.urls import path
from . import views

urlpatterns = [
    # register
	path('register/', views.registerPage, name="register"),
    # login
	path('', views.loginPage, name="login"),  
    # logout
	path('logout/', views.logoutUser, name="logout"),

    # home : pk_test=user.username
    path('home/<str:pk_test>/', views.home, name="home"),

    # profile : pk_test=user.username
    path('profile/<str:pk_test>/', views.profile, name="profile"),
    # profileUpdate : pk_test=user.username
    path('profileUpdate/<str:pk_test>/', views.profileUpdate, name="profileUpdate"),

    # skillCreate : pk_user=user.username
    path('<str:pk_user>/skillCreate/', views.skillCreate, name="skillCreate"),

    # team : pk_test=user.username
    path('team/<str:pk_test>/', views.team, name="team"),
    # teamCreate : pk_test=user.username
    path('teamCreate/<str:pk_test>/', views.teamCreate, name="teamCreate"),
    # joinTeam : pk_user=user.username , pk_team=team.name
    path('<str:pk_user>/join/<str:pk_team>/', views.joinTeam, name="joinTeam"),
    # leaveTeam : pk_user=user.username , pk_team=team.name
    path('<str:pk_user>/leave/<str:pk_team>', views.leaveTeam, name="leaveTeam"),
    # deleteTeam : pk_user=user.username , pk_team=team.name
    path('<str:pk_user>/delete/<str:pk_team>/', views.deleteTeam, name="deleteTeam"),

    # teamChatRoom : pk_user=user.username , pk_team=team.name
    path('<str:pk_team>/chatroom/<str:pk_user>/', views.teamChatRoom, name="teamChatRoom"),
    # removeMember : pk_user=team.owner , pk_team=team.name , pk_member=member.user_name
    path('<str:pk_user>/<str:pk_team>/remove/<str:pk_member>', views.removeMember, name="removeMember"),

    # profileMember : pk_user=user.username , pk_member=member.name
    path('<str:pk_user>/profile/<str:pk_member>', views.profileMember, name="profileMember"),
    
    # search : pk_user=user.username
    path('<str:pk_user>/search/',views.search, name="search"),
]
