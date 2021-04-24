from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static



urlpatterns = [
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view, name="home_view"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('afterlogin', views.afterlogin_view, name='after_login'),

    # Admin URLS
    path('admin/', admin.site.urls),
    path('admin-login', LoginView.as_view(template_name='admin/login.html'), name='admin-login'),
    path('admin-signup', views.adminsignup_view, name="adminsignup"),
    path('add-librarian', views.adminsignup_view, name='addlibrarian'),
    path('admin-view-books', views.viewbook, name='view'),
    path('admin-view-issued-books', views.viewissuedbook, name='issued'),
    path('admin-view-students', views.viewstudent, name='students'),

    # Librarian URLS
    path('librarian-click', views.Librarian_click_view, name='librarian_click'),
    path('librarian-login', LoginView.as_view(template_name='librarian/librarian_login.html')),
    path('add-book', views.addbook_view, name='addbook'),
    path('view-books', views.viewbook_view, name='viewbook'),
    path('issue-book', views.issuebook_view , name='issuebook'),
    path('view-issued-books', views.viewissuedbook_view, name="viewissuedbook"),
    path('view-students', views.viewstudent_view, name="viewstudent"),
    path('update/<int:id>', views.update_view, name='updatebook'),
    path('delete/<int:id>', views.delete_view, name='deletebook'),
    path('return-issued-book/<int:id>', views.return_issued_book_view, name='return_book'),

    # Student URLS
    path('student-signup', views.studentsignup_view, name="studentsignup"),
    path('student-login', LoginView.as_view(template_name='student/studentlogin.html')),
    path('student-click', views.studentclick_view, name="studentclick"),
    path('view-issued-book-student', views.viewissuedbookbystudent, name="viewissuedbookbystudent"),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
