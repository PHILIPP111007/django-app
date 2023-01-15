from django import forms


class UserForm(forms.Form):
	name = forms.CharField(max_length=20, help_text='Write name')
	surname = forms.CharField(max_length=20, help_text='Write surname')
	age = forms.IntegerField(min_value=0, max_value=120, help_text='Write age')


class EditForm(forms.Form):
	name = forms.CharField(required=False, max_length=20)
	surname = forms.CharField(required=False, max_length=20)
	age = forms.CharField(required=False, max_length=3)



class AdminForm(forms.Form):
	login = forms.CharField(max_length=20)
	password = forms.CharField(max_length=30)


class UploadForm(forms.Form):
    csv_file = forms.FileField()


class FindForm(forms.Form):
	id = forms.CharField(required=False)
	name = forms.CharField(required=False, max_length=20)
	surname = forms.CharField(required=False, max_length=20)
	age = forms.CharField(required=False, max_length=3)