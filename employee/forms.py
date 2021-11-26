from django import forms
from . import models

class ProfileForm(forms.ModelForm):
	class Meta:
		model = models.employee
		fields = ['name', 'email', 'contact_num']
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
			'contact_num': forms.TextInput(attrs={'class':'form-control'}),
			}

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = '姓名'
		self.fields['email'].label = '郵箱地址'
		self.fields['contact_num'].label = '聯絡號碼'


# class ProfileForm(forms.Form):
# 	name = forms.CharField(label='姓名', required=True)
# 	email = forms.CharField(label='郵箱地址', required=True)
# 	contact_num = forms.CharField(label='聯絡號碼', required=True)
