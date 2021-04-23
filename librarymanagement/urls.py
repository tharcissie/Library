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

    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),


    path('admin-signup', views.adminsignup_view),
    path('student-signup', views.studentsignup_view),
    path('admin-login', LoginView.as_view(template_name='admin/adminlogin.html')),
    path('student-login', LoginView.as_view(template_name='library/studentlogin.html')),

    path('logout', LogoutView.as_view(), name="logout"),
    path('afterlogin', views.afterlogin_view),

    path('add-book', views.addbook_view, name='addbook'),

    path('<int:id>', views.update_view, name='updatebook'),
    path('<int:id>/delete', views.delete_view, name='deletebook'),

    path('view-book', views.viewbook_view, name='viewbook'),
    path('issue-book', views.issuebook_view),
    path('view-issued-books', views.viewissuedbook_view),
    path('return-issued-book/<int:pk>', views.return_issued_book_view, name='return_book'),
    path('view-student', views.viewstudent_view),
    path('view-issued-book-by-student', views.viewissuedbookbystudent),
    #path('return_book', views.return_book),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
