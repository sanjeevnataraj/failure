from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from web_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from web_app.sitemaps import StaticViewSitemap,SnippetSitemap,CollegeSitemap
from web_app import middleware
sitemaps = {
    # 'static': StaticViewSitemap,
    'snippet':SnippetSitemap,
    'college':CollegeSitemap,

}


urlpatterns = [

    url(r'^django-session-idle-timeout/',middleware.SessionIdleTimeout,name="s"),

    url(r'^insert$', views.insert, name="insert"),
    
    path('main_course/<slug>',views.course_detail,name="course_detail"),

    path('course/<slug>',views.course_slug,name='course_slug'),
    
    path('admin/', admin.site.urls),
    
    url(r'^$',views.index,name="index"),
    
    path('register/',views.registration_page,name="registartion_page"),
    
    path('login/',views.user_login,name="Login_page"),
    
    path('logout/',views.user_logout,name="logout"),
    
    path('profile/',views.profile_page,name="profile_page"),
    
    path("update_profile/", views.edit_student_form, name ="student_edit_form"),
    
    path('Degree/',views.degree_details,name="degree_detail"),
    
    path('Branch/',views.branch_detail,name="branch"),
    
    path('Exam/',views.Exam_details,name="exam"),

    path('ajax/validate/',views.check,name="check"),
    
    url(r'^ajax_calls/search/',views.autocompleteModel,name="auto_degree"),
    
    url(r'^ajax_calls/searchs/',views.autocomplte_branch,name="auto_branch"),
    
    url(r'^ajax_calls/search-course/',views.autocomplte_course,name="auto_course"),
    
    url(r'^course_profile/',views.List_view.as_view(),name="listview"),
    
    url(r'^manage_course/',views.managecourse,name="manage_course"),
    
    path("manage/college/courses/<pk>",views.managecourse,name="manage_course"),
    
    path('college/coures/<name>/<pk>/add',views.dynamicfield,name="dynamic-arg"),
    
    path("courses/<int:pk>", views.edit_course_form, name ="course_edit_form"),

    url(r'^course',views.dynamicfield,name="dynamic"),

    path('manage/',views.manage,name="manage"),

    path('manage-college/',views.manage_college,name="college"),

    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},name='d'),

    path('about',views.about,name="about"),

    path('add-college/',views.add_college,name="add-college"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
