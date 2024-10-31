from django import forms
from .models import User, Student, Teacher, Registrar

class StudentCreationForm(forms.ModelForm):
    registration_number = forms.CharField(max_length=20)
    
    class Meta:
        model = User
        fields = ('username', 'password','registration_number')

class TeacherCreationForm(forms.ModelForm):
    teacher_id = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'teacher_id')

class RegistrarCreationForm(forms.ModelForm):
    registrar_id = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'registrar_id')
#class AssessmentCreation(forms.ModelForm):
 #   class Meta:
  #      model = Assessment
  #      fields = ['course', 'numberofass', 'name', 'max_mark']