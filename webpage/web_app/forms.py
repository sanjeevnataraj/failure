from django import forms
from django.contrib.auth.models import User
from web_app.models import Student_profile,Hobby_details,Course_page,Degree_detail,Branch_detail,Exam_detail,subcoursepage,Streams,College_detail
from dal import autocomplete
from django.forms.models import inlineformset_factory

class SignUpForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():

        model = User

        fields = ('username', 'email', 'password')

class Register(forms.ModelForm):

    class Meta():

        model = Student_profile

        fields = ('PhoneNumber','qualification','subjects','percentage','Description','profile_pic')

class Hobbies(forms.ModelForm):

    types = (('None','Please Select'), ('Music','Music'), ('Sports','Sports'))

    hobby_choices = forms.ChoiceField(choices=types)

    class Meta():

        model = Hobby_details

        fields = ('hobby_choices','hobby_name',)

    def clean_hobby_choices(self):

        name=self.cleaned_data.get('hobby_choices')

        if name == "None":

            raise forms.ValidationError("You must select the value")

        else:

            return name

#---------------------------------------------CourseForm-----------------------------------------------------
class CourseForm(forms.ModelForm):

    course = Course_page.objects.all()

    exam = forms.ModelMultipleChoiceField( required=True, queryset=Exam_detail.objects.all())

    course_detail = forms.CharField(widget=forms.Textarea)

    class Meta():

        model = Course_page

        fields = ('course_name','course_duration','degree','branch','exam','eligibility','course_detail','publish')

    def clean_course_name(self):

        name = self.cleaned_data.get('course_name')

        m = Course_page.objects.all().values_list('course_name', flat=True)

        l = []

        for i in m:

            l.append(i)

        if name in l:

            raise forms.ValidationError("This course already taken")

        else:

            return name

class Degree_detailForm(forms.ModelForm):

    class Meta():
        
        model = Degree_detail

        fields = ('name','stream','publish')

class Branch_detailForm(forms.ModelForm):


    class Meta():

        model = Branch_detail

        fields = ('name','stream','publish')

class Exam_detailForm(forms.ModelForm):

    class Meta():

        model = Exam_detail

        fields = ('name','Exam','publish')

class subcourseform(forms.ModelForm):

    class Meta():

        model = subcoursepage

        fields = ('category','Total_fees')

class streamform(forms.ModelForm):

    class Meta():

        model = Streams

        fields = ('streambranch','streamdegree','Stream')

class collegeForm(forms.ModelForm):

    class Meta():

        model = College_detail

        fields = ('college_name',)