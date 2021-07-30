from django.db import models

# Create your models here.
class Skill(models.Model):
	name = models.CharField(max_length=100,default='Skill')

	def save(self, force_insert=False, force_update=False):
		self.name = self.name.upper()
		super(Skill, self).save(force_insert, force_update)

	def __str__(self):
		return self.name

class Team(models.Model):
	name = models.CharField(max_length=50)
	owner = models.CharField(max_length=50,default='Owner')
	skill = models.ManyToManyField(Skill)

	def __str__(self):
		return self.name

class TeamChatRoom(models.Model):
	team_chat_name = models.OneToOneField(
		Team,
		on_delete=models.CASCADE,
		primary_key=True,
	)

	def __str__(self):
		return "%s : ChatRoom" % self.team_chat_name.name

class ChatMessage(models.Model):
	team_name = models.ForeignKey(TeamChatRoom,models.CASCADE)
	member_username = models.CharField(max_length=200)
	member_message = models.CharField(max_length=200,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "%s : %s : %s : %s" % (self.team_name, self.date_created, self.member_username, self.member_message)

class Member(models.Model):
	user_name = models.CharField(max_length=200)
	first_name = models.CharField(max_length=200,null=True,blank=True)
	middle_name = models.CharField(max_length=200,null=True,blank=True)
	last_name = models.CharField(max_length=200,null=True,blank=True)
	email = models.CharField(max_length=200,default='Email')
	skills = models.ManyToManyField(Skill,blank=True)
	teams = models.ManyToManyField(Team,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	profile_image = models.ImageField(null=True,blank=True)

	def __str__(self):
		return self.user_name