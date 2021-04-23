from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view, name="home_view"),

    path('adminclick', views.adminclick_view, name='adminclick'),
    path('studentclick', views.studentclick_view, name="studentclick"),


    path('adminsignup', views.adminsignup_view, name="adminsignup"),
    path('studentsignup', views.studentsignup_view, name="studentsignup"),
    path('adminlogin', LoginView.as_view(template_name='admin/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html')),

    path('login', LoginView.as_view(template_name='super/login.html'), name='admin-login'),

    path('logout', LogoutView.as_view(), name="logout"),
    path('afterlogin', views.afterlogin_view),

    path('addbook', views.addbook_view, name='addbook'),
    path('addlibrarian', views.adminsignup_view, name='addlibrarian'),

    path('<int:id>', views.update_view, name='updatebook'),
    path('<int:id>/delete', views.delete_view, name='deletebook'),

    path('super_viewbook', views.viewbook, name='view'),

    path('super_viewissuedbook', views.viewissuedbook, name='issued'),

   
    path('superviewstudent', views.viewstudent, name='students'),
    path('viewbook', views.viewbook_view, name='viewbook'),
    path('issuebook', views.issuebook_view , name='issuebook'),
    path('viewissuedbook', views.viewissuedbook_view, name="viewissuedbook"),
    path('returnissuedbook/<int:id>', views.return_issued_book_view, name='return_book'),
    path('viewstudent', views.viewstudent_view, name="viewstudent"),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent, name="viewissuedbookbystudent"),
    #path('return_book', views.return_book),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
