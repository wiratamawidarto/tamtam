from django import forms
from . import models

class ProfileForm(forms.ModelForm):
	class Meta:
		model = models.employee
		fields = ['gongHao', 'name','company', 'lineid', 'email', 'contact_num']
		widgets ={
		    'gonghao': forms.TextInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'company': forms.Select(attrs={'class':'form-control'}),
            'lineid': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'contact_num': forms.TextInput(attrs={'class':'form-control'}),
            }


	def __init__(self, *args, **kwargs):
	    super(ProfileForm, self).__init__(*args, **kwargs)
	    self.fields['gongHao'].widget.attrs['readonly'] = True
	    self.fields['company'].widget.attrs['readonly'] = True
	    self.fields['lineid'].widget.attrs['readonly'] = True
	    self.fields['gongHao'].label = '工號(無法更改）'
	    self.fields['name'].label = '姓名'
	    self.fields['company'].label = '公司(無法更改）'
	    self.fields['lineid'].label = 'LINE(無法更改）'
	    self.fields['email'].label = '郵箱地址'
	    self.fields['contact_num'].label = '聯絡號碼'
