from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
import datetime
from django.template.defaultfilters import slugify
from django.urls import reverse
from froala_editor.fields import FroalaField


#-----------------------------------Student Detail------------------------------------------------------------------


streams = ( ('Engineering','Engineering'),('Medical','Medical'),('Law','Law'),('Arts','Arts'))
exams = ( ('JEE Main','JEE Main'),('JEE Advance','JEE Advance'),('VITEEE','VITEEE'),('GATE','GATE'))

class Student_profile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)

    PhoneNumber = models.CharField(max_length=250,default="")

    qualification = models.CharField(max_length=250,default="")

    subjects = models.CharField(max_length=250,default="")

    percentage = models.CharField(max_length=250,default="")

    Description = models.CharField(max_length=250,default="")

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)


    def __str__(self):
        return self.user.username
    #def get_absolute_url(self):
    #    return reverse('profile-update', kwargs={'pk': self.pk})

#--------------------------------------Hobby Detail---------------------------------------------------------------

class Hobby_details(models.Model):

    types = (('None','Please Select'), ('Music','Music'), ('Sports','Sports'))

    student = models.ForeignKey('Student_profile', on_delete=models.CASCADE,null=True,blank=True,related_name = "hob")

    hobby = models.CharField(max_length=256)

    hobby_choices = models.CharField(max_length=25,choices = types, default='None')

    hobby_name = models.CharField(max_length=245)


#-------------------------------------------Degree_detail--------------------------------------------------------

class Degree_detail(models.Model):

    global streams

    name = models.CharField(max_length=250)

    stream = models.CharField(max_length=258,choices = streams ,default='Engineering')

    publish = models.BooleanField(default = True)

    def __str__(self):

        return self.name

#------------------------------------------Branch_detail-----------------------------------------------------------

class Branch_detail(models.Model):

    global streams

    name = models.CharField(max_length=250)

    stream = models.CharField(max_length=258,choices = streams ,default='Engineering')

    publish = models.BooleanField(default = True)

    def __str__(self):

        return self.name

#--------------------------------------Exam_detail---------------------------------------------------------------


class Exam_detail(models.Model):

    global exams

    name = models.CharField(max_length=250)

    Exam = models.CharField(max_length=258,choices = exams,default='GATE')

    publish = models.BooleanField(default = True)

    def __str__(self):

        return self.Exam


#----------------------------------------Course_page-------------------------------------------------------------

class Course_page(models.Model):

    college = models.ForeignKey('College_detail',on_delete=models.CASCADE,null=True,blank=True)
    
    global exams

    course_name = models.CharField(max_length=256)

    degree = models.CharField(max_length=50)

    branch = models.CharField(max_length=50)

    exam = models.ManyToManyField(Exam_detail,blank=True,default=None)

    course_duration = models.IntegerField()

    eligibility = models.CharField(max_length=223)

    course_detail = models.CharField(max_length=256)

    publish = models.BooleanField(default = True)

    created_date =  models.DateField(("Date"), default=datetime.date.today)

    updated_date = models.DateField(("Date"), default=datetime.date.today)

    slug = models.SlugField(blank=True)


    def save(self, *args, **kwargs):

        l = ['of','is','an','the','was'] 

        k = self.course_name.split(' ')

        mk = k.copy()

        for i in k:

            if i in l:

                mk.remove(i)

        new = "-".join(str(x) for x in mk)
       
        new_source = new+ "-careers360"
        
        self.slug = slugify(new_source)

        super(Course_page, self).save(*args, **kwargs)

    def get_absolute_url(self):

        #return (f'/{self.slug}/')
        return "hello"

#------------------------------------------course_page foreignkey -------------------------------------------------

class subcoursepage(models.Model):

    subcourse = models.ForeignKey('Course_page', on_delete=models.CASCADE,null=True,blank=True,related_name = "hob")

    category = models.CharField(max_length=254)

    Total_fees = models.IntegerField()

#----------------------------------------streams--------------------------------------------------------------------------

class Streams(models.Model):

    streambranch = models.CharField(max_length = 222)

    streamdegree =  models.CharField(max_length = 122)

    Stream = models.CharField(max_length = 122)



#-----------------------------------College Detail---------------------------------------------------

class College_detail(models.Model):

    college_name = models.CharField(max_length=122)

    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):

        l = ['of','is','an','the','was'] 

        k = self.college_name.split(' ')

        mk = k.copy()

        for i in k:

            if i in l:

                mk.remove(i)

        new = "-".join(str(x) for x in mk)
        
        self.slug = slugify(new)

        super(College_detail, self).save(*args, **kwargs)

    def get_absolute_url(self):

        # return (f'/{self.slug}/')
        return "hello"
