from django import forms

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		# Checking if user exists by QuerySet

		# user_qs = User.objects.filter(username = username)
		# if user_qs.count() == 1:
		# 	user = user_qs.first()
		if username and password:
			user = authenticate(username = username, password= password)	# Check if user in database
			if not user:
				raise forms.ValidationError("This user is not in database!")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password, are you hacker?")

			if not user.is_active:
				raise forms.ValidationError("You are not log in!")

		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label = "Email address")
	email2 = forms.EmailField(label = "Confirm e-mail")
	password = forms.CharField(widget = forms.PasswordInput)

	class Meta:
		model = User
		# Declaring what are we going to use from User Model
		fields = {
			'username',
			'password',
			'email',
		}

	def clean_email2(self):	# Email match
		print (self.cleaned_data)
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		print (email, email2)
		if email != email2:
			raise forms.ValidationError("Emails are not same")

		email_qs = User.objects.filter(email = email)
		if email_qs.exists():
			raise forms.ValidationError("This email is already registered.")
		return email