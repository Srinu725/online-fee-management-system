from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from FinalApp.models import AccountantProfile,StudentProfile

class AccountantRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
   
    employee_id = forms.CharField(max_length=20, label="Employee ID")
    phone = forms.CharField(max_length=15)
    department = forms.CharField(max_length=50)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    student_id = forms.CharField(max_length=20, label="Student ID")
    phone = forms.CharField(max_length=15)
    branch = forms.CharField(max_length=50)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 

    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            StudentProfile.objects.create(
                student_user=user,
                student_id=self.cleaned_data['student_id'],
                phone=self.cleaned_data['phone'],
                branch=self.cleaned_data['branch'],
                address=self.cleaned_data['address']
            )