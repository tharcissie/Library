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

    path('admin-click', views.adminclick_view, name='adminclick'),
    path('student-click', views.studentclick_view, name="studentclick"),


    path('admins-ignup', views.adminsignup_view, name="adminsignup"),
    path('student-signup', views.studentsignup_view, name="studentsignup"),
    path('admin-login', LoginView.as_view(template_name='admin/adminlogin.html')),
    path('student-login', LoginView.as_view(template_name='library/studentlogin.html')),

    path('login', LoginView.as_view(template_name='super/login.html'), name='admin-login'),

    path('logout', LogoutView.as_view(), name="logout"),
    path('afterlogin', views.afterlogin_view, name='after_login'),

    path('add-book', views.addbook_view, name='addbook'),
    path('add-librarian', views.adminsignup_view, name='addlibrarian'),

    path('<int:id>', views.update_view, name='updatebook'),
    path('<int:id>/delete', views.delete_view, name='deletebook'),

    path('super_viewbook', views.viewbook, name='view'),

    path('super-view-issued-book', views.viewissuedbook, name='issued'),

   
    path('super-view-student', views.viewstudent, name='students'),
    path('view-book', views.viewbook_view, name='viewbook'),
    path('issue-book', views.issuebook_view , name='issuebook'),
    path('view-issued-book', views.viewissuedbook_view, name="viewissuedbook"),
    path('return-issued-book/<int:id>', views.return_issued_book_view, name='return_book'),
    path('view-student', views.viewstudent_view, name="viewstudent"),
    path('view-issued-book-by-student', views.viewissuedbookbystudent, name="viewissuedbookbystudent"),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
