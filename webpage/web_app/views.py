from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from web_app.forms import SignUpForm,Register,Hobbies,CourseForm,Degree_detailForm,Branch_detailForm,Exam_detailForm,subcourseform,streamform,collegeForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from web_app.models import Student_profile,Hobby_details,Degree_detail,Course_page,Branch_detail,subcoursepage,Streams,College_detail
from django.views.generic import View,ListView,CreateView,UpdateView
from django.contrib.auth.models import User
from . import models
from django.db import transaction
import simplejson as json
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



def check(request):

    username = request.GET.get('username', None)

    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

def insert(request):
    
    print(request.POST.get('val'))
    return HttpResponse("you are login successfully")
    # return "successfully"

def index(request):
    return render(request,"homepage.html")

@login_required
def special(request):
    return HttpResponse("you are login successfully")

@login_required
def user_logout(requets):
    logout(requets)
    return HttpResponseRedirect(reverse('index'))

@csrf_protect

def registration_page(request):
    registered = False
    #print(request.POST)
    if request.method == "POST":

        signup_detail = SignUpForm(data=request.POST)
        student_detail = Register(data=request.POST)
        hobby = Hobbies(data = request.POST)

        print(request.POST.get('password'), signup_detail,signup_detail.errors)

        if signup_detail.is_valid() and student_detail.is_valid() and hobby.is_valid():

            print("welcome")
            user = signup_detail.save()
            user.set_password(user.password)
            user.save()

            student = student_detail.save(commit=False)
            student.user = user

            if 'profile_pic' in request.FILES:
                student.profile_pic = request.FILES['profile_pic']

            student.save()

            # hob = hobby.save(commit=False)
            hobby.student_id = 1
            hobby.save()

            try:
                for i in range(2,10):
                    i=str(i)
                    n="field"+i
                    hb2 = request.POST[n]
                    if hb2=="":
                        break
                    else:
                        Hobby_details.objects.create(hobby = hb2)
            except:
                print("something")

            registered = True

            return HttpResponseRedirect(reverse('Login_page'))
        else:
            
            print("not coming")
            
            print(SignUpForm.errors,Register.errors)
    else:
        
        signup_detail = SignUpForm()
        
        student_detail = Register()
        
        hobby = Hobbies()
    
    return render(request,"registration.html",{'signup_detail':signup_detail,'student_detail':student_detail,"registerd":registered,'hobbies':hobby,'h':True})

def user_login(request):

    if request.method=='POST':
       
        username = request.POST.get('username')
       
        password = request.POST.get('password')
       
        user = authenticate(username=username,password=password)
       
        if user:
       
            if user.is_active:
       
                login(request,user)
       
                print(request.user)
       
                return HttpResponseRedirect(reverse('index'))
       
            else:
       
                return HttpResponse("Account not activated")
        else:

            print("someone tried to login but login failure")

            print("Username: {} Password: {} ".format(username,password))

            return HttpResponse("Invalid Login details")
    else:
        
        return render(request,"login.html",{})


def profile_page(request):
    user_id = request.user
    u_id = request.user.id
    print("this is id ",u_id)
    
    try:
        user_details = Student_profile.objects.filter(user=user_id)
        #hobbies = Hobby_details.objects.filter(pk = u_id)
        hobbies = Hobby_details.objects.filter(student__user__username__contains=user_id)
        print("this is user",user_details)
        print("this is hobbies",hobbies)
    except:
        raise Http404("you are logged out you need to login")
    return render(request, "profile_details.html" , {'user_details':user_details,'hobbies':hobbies})

def edit_student_form(request):
    try:
        user_name = request.user
        n = request.user.id
        k = User.objects.get(pk = n)
        h = Student_profile.objects.get(pk = n)
        i = Hobby_details.objects.get(pk = n)
        print (i)
        u = Hobby_details.objects.filter(student__user__username__contains=user_name)
        print ("this is me ",u)
        signup_detail = SignUpForm(request.POST or None, instance = k)
        student_detail = Register(request.POST or None, instance = h)
        hob = Hobbies(request.POST or None, instance = i)
        print(hob)
        if student_detail.is_valid() and hob.is_valid():
            student_detail.save()
            hob.save()
            return HttpResponseRedirect(reverse('profile_page'))
    except:
        raise Http404("you are logged out you need to login")
    return render(request,'registration.html',{'signup_detail':signup_detail,'student_detail':student_detail,'hobbies':hob,'h':False})

#------------------------------------course_detail------------------------------------------------------------------------------------------------------------------------------------

def course_detail(request,slug):

    if request.method == "POST":

        print("It came here ")

        course = CourseForm(data=request.POST)
        
        if course.is_valid():

            print("hello")
            
            course_model = course.save(commit=False)
            
            course_model.college_id = 2
            
            #   course_model.exam = s
            
            course_model.save()
            

    else:
        course = CourseForm()

    return render(request,"course_detail.html",{"course":course})


def course_slug(request,slug):

    course = Course_page.objects.filter(slug=slug)

    print(course)

    return render(request,'courseslug.html',{'course':course})


#------------------Degree Details ---------------------------------------------------------------------

def degree_details(request):

    if request.method == "POST":
        degree = Degree_detailForm(data=request.POST)
        if degree.is_valid():
            degree.save()
            return HttpResponseRedirect(reverse('branch'))
    else:
        degree = Degree_detailForm()
    return render(request,"degree_detail.html",{"degree":degree})

#------------------------branch Detail ----------------------------------------------------------------

def branch_detail(request):
    if request.method == "POST":
        branch = Branch_detailForm(data=request.POST)
        if branch.is_valid():
            branch.save()
            return HttpResponseRedirect(reverse('exam'))
    else:
        branch = Branch_detailForm()
    return render(request,"branch-detail.html",{"branch":branch})

#------------------------------------ Exam-form ---------------------------------------------------------------------------

def Exam_details(request):
    if request.method == "POST":

        exam = Exam_detailForm(data=request.POST)
        if exam.is_valid():
            exam.save()
            return HttpResponseRedirect(reverse('course_detail'))
    else:
        exam = Exam_detailForm()
    return render(request,"exam_details.html",{"exam":exam})

#--------------------------------Auto complete Model----------------------------------------------------------------------------------------------

def autocompleteModel(request,degree_stream=None):
    
    if request.is_ajax():
        
        results =[]
        
        q = request.GET.get('term', '')
        
        search= Degree_detail.objects.filter(name__icontains=q).values('id','name','stream')
        
        for data in search:
        
            result = dict()
            result['label'] = data['name']
            result['value'] = data['name']
            result['id'] = data['id']
            result['stream'] = data['stream']
            results.append(result)
        
        data = json.dumps(results)

    else:
        
        data = 'fail'

    mimetype = 'application/json'

    return HttpResponse(data, mimetype)

def autocomplte_branch(request):

    if request.is_ajax():
        
        results =[]
        
        q = request.GET.get('term', '')
        
        search= Branch_detail.objects.filter(name__icontains=q).values('id','name','stream')
        
        for data in search:
            result = dict()
            result['label'] = data['name']
            result['value'] = data['name']
            result['id'] = data['id']
            result['stream'] = data['stream']
            results.append(result)
        
        print(results)        

        #branch_name = data['name']

        #branch_stream =Branch_detail.objects.get(name=branch_name)

        #stream = streamform(initial = {'streambranch':  branch_stream.stream})
  
        data = json.dumps(results)
  
    else:
  
        data = 'fail'
  
    mimetype = 'application/json'
  
    return HttpResponse(data, mimetype)

def autocomplte_course(request):
    
    if request.is_ajax():
        results =[]
        q = request.GET.get('term', '')
        search= Course_page.objects.filter(course_name__icontains=q).values('id','course_name')
        for data in search:   
            result = dict()
            result['label'] = data['course_name']
            result['value'] = data['course_name']
            result['id'] = data['id']
            results.append(result)

        data = json.dumps(results)
    
    else:
       
        data = 'fail'

    mimetype = 'application/json'

    return HttpResponse(data, mimetype)

class List_view(ListView):
   
    context_object_name = "course_detail"
    
    model = models.Course_page
    
    template_name = "listview.html"
    
    paginate_by = 1
    
    queryset = Course_page.objects.all()


#-----------------------------------------Managecourse----------------------------------------------------------

def managecourse(request,pk=None):
    
    course_model = Course_page.objects.all()

    course = CourseForm()

    l = Course_page.objects.filter(college_id = pk)

    print(l)

    if request.method == "POST":
        
        course = CourseForm(data=request.POST)
        
        course_name = request.POST.get('course_name')

        m = Course_page.objects.all().values_list('course_name', flat=True)

        l = []

        for i in m:

            l.append(i)

        if course_name in l:

            print("not valid")

            return render(request, "course.html", {'course': course,'course_model':course_model})

        else:

            name = {'course_name':course_name}

            return HttpResponseRedirect(reverse('dynamic-arg',args=(course_name,pk)))

    else:

        d={}

        for key,value in request.GET.items():
            
            if value !='':  

                d[key]=value

        print(d)
        
        if d:

            l = Course_page.objects.filter(college_id=pk,**d)

        else:

            course_model = l   

            course = CourseForm()

    return render(request,"course.html",{'course':course,'course_model':l})

#---------------------------------------------------------------------------------------------------


def dynamicfield(request,name=None,pk=None):

    print(name)

    print(pk)

    course_name = request.GET.get('name')

    course = CourseForm(initial = {'course_name':name} )

    Course_formset = modelformset_factory(subcoursepage,form = subcourseform ,extra = 1,can_delete = True)

    stream = streamform()

    if request.method == "GET":
    
        formset = Course_formset(queryset=subcoursepage.objects.none())

    elif request.method == "POST":

        formset = Course_formset(request.POST)

        course = CourseForm(data=request.POST)

        myDict = dict(request.POST)
        
       
        if course.is_valid():

            with transaction.atomic():

                temp_form = course.save()
                
                temp_form.college_id=pk
                
                if formset.is_valid():
                
                    for f in formset:
                
                        f.subcourse = temp_form
                
                    formset.save()
                
                else:
                
                    print("where it is coming")
            
            course.save()

            return HttpResponseRedirect(reverse('manage_course',args=(pk,)))

    else:

        course = CourseForm()

        stream = streamform()
        
    return render(request,"course_formset.html",{"formset":formset,'course':course,"stream":stream})


def edit_course_form(request,pk):
   
    n=pk

    h=Course_page.objects.get(pk=n)
    
    print(h.exam,type(h.exam))

    form = CourseForm(request.POST or None, instance=h)

    dstream= Degree_detail.objects.get(name=h.degree)

    degree_stream = dstream.stream

    bstream = Branch_detail.objects.get(name=h.branch)

    branch_stream =  bstream.stream

    print(branch_stream)

    if form.is_valid():

        print("hello")

        form.save()

        return HttpResponseRedirect(reverse('manage_course'))

    return render(request,'course_update.html',{'form':form,'branch_stream':branch_stream,'degree_stream':degree_stream})

def manage(request):
    
    course = CourseForm()

    return render(request,'course.html',{'course_model':filter_course,'course':course})

#---------------------------------------------------------------------------------------------------

def manage_college(request):

    if request.method=='POST':

        collegename = request.POST.get('college_name')

        college = College_detail.objects.filter(college_name=collegename)

        print(college)

        for i in college:

            print(i.pk)

            ids = i.pk
            
        return HttpResponseRedirect(reverse('manage_course',args=(ids,)))
    
    else:

        college = collegeForm()

    return render(request,'college.html',{'college':college})

def about(request):

    return HttpResponse('s')

def add_college(request):

    college_add = collegeForm(request.POST or None)

    if request.method =="POST":

        print(college_add)

        if college_add.is_valid():

            print('hello')

            college_add.save()

            return HttpResponseRedirect(reverse('college'))

    return render(request,'add_college.html',{'college_add':college_add})