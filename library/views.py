from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date



def home_view(request):
    education = models.Book.objects.filter(category='education').order_by('-pk')[:4]
    entertainment = models.Book.objects.filter(category='entertainment').order_by('-pk')[:4]
    comics = models.Book.objects.filter(category='comics').order_by('-pk')[:4]
    biography = models.Book.objects.filter(category='biography').order_by('-pk')[:4]
    history = models.Book.objects.filter(category='history').order_by('-pk')[:4]
    student = models.StudentExtra.objects.all().count()
    book = models.Book.objects.all().count()
    isue = models.IssuedBook.objects.all().count()
    books = models.Book.objects.all()

    context = {
        'education':education,
        'entertainment':entertainment,
        'comics':comics,
        'biography':biography,
        'history':history,
        'student':student,
        'book':book,
        'isue':isue,
        'books':books
    }
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'core/index.html', context)

def is_admin(user):
    return user.groups.filter(name='LIBRARIAN').exists()

def afterlogin_view(request):
    education = models.Book.objects.filter(category='education').order_by('-pk')[:4]
    entertainment = models.Book.objects.filter(category='entertainment').order_by('-pk')[:4]
    comics = models.Book.objects.filter(category='comics').order_by('-pk')[:4]
    biography = models.Book.objects.filter(category='biography').order_by('-pk')[:4]
    history = models.Book.objects.filter(category='History').order_by('-pk')[:4]
    student = models.StudentExtra.objects.all().count()
    book = models.Book.objects.all().count()
    isue = models.IssuedBook.objects.filter(is_returned='NO').count()
    books = models.Book.objects.all()

    context = {
        'education':education,
        'entertainment':entertainment,
        'comics':comics,
        'biography':biography,
        'history':history,
        'student':student,
        'book':book,
        'isue':isue,
        'books':books
    }
    if is_admin(request.user):
        return render(request,'admin/adminafterlogin.html', context)
    elif request.user.is_superuser:
        return render(request,'admin/super.html', context)
    else:
        return render(request,'student/studentafterlogin.html', context)


## ADMIN Views ##

def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='LIBRARIAN')
            my_admin_group[0].user_set.add(user)
            return render(request,'admin/librarian_added.html')
    return render(request,'admin/addlibrarian.html',{'form':form})


@login_required(login_url='login')
def viewbook(request):
    books= models.Book.objects.all()
    return render(request,'admin/viewbook.html',{'books':books})


def viewissuedbook(request):
    issuedbooks=models.IssuedBook.objects.all().filter(is_returned='NO')
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*10

        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'admin/issuedbook.html',{'li':li})


def viewstudent(request):
    students=models.StudentExtra.objects.all()
    return render(request,'admin/students.html',{'students':students})




## LIBRARIAN Views ##

def Librarian_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'librarian/librarian_click.html')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def addbook_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST or None,files=request.FILES)
        if form.is_valid():
            isbn = form.cleaned_data.get('isbn')

            if len(str(isbn)) == 8:
                user = form.save()
                return redirect('bookadded')
            else:
                return render(request,'librarian/addbook.html',{'form':form, 'error':"ISBN must be 8 numbers"})
    return render(request,'librarian/addbook.html',{'form':form})


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def bookadded_view(request):
    return render(request,'librarian/bookadded.html')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def viewbook_view(request):
    books= models.Book.objects.all()
    return render(request,'librarian/viewbooks.html',{'books':books})


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method =='POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.enrollment = request.POST.get('enrollment2')
            obj.isbn = request.POST.get('isbn2')
            validation =  models.IssuedBook.objects.filter(enrollment=obj.enrollment ).filter(is_returned='NO').exists()
            if validation:
                return render(request,'librarian/issuebook.html',{'form':form, 'error':"The student has another issued book"})
            obj.save()
            return redirect('issued_books')
    return render(request,'librarian/issuebook.html',{'form':form})


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def issued_books_view(request):
    return render(request,'librarian/bookissued.html')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all().filter(is_returned='NO')
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*10

        books=list(models.Book.objects.filter(isbn=ib.isbn))
        issue=list(models.IssuedBook.objects.filter(id=ib.id))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine,issue[i].id,issue[i].id)
            i=i+1
            li.append(t)

    return render(request,'librarian/viewissuedbook.html',{'li':li})


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'librarian/viewstudent.html',{'students':students})


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_view(request, id):
    context ={}
    book = get_object_or_404(models.Book, id = id)
    form = forms.BookForm(request.POST or None, instance = book)
    if form.is_valid():
        form.save()
        return redirect('viewbook')
    context["form"] = form
    return render(request, "librarian/update_book.html", context)


def delete_view(request, id):
    book = get_object_or_404(models.Book, id = id)
    context ={'book':book}

    if request.method =="POST":
        book.delete()
        return redirect("viewbook")
    return render(request, "librarian/deletebook.html", context)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def return_issued_book_view(request, id):
    issued_book = models.IssuedBook.objects.get(id=id)
    form = forms.ReturnIssuedBookForm(request.POST or None, instance=issued_book)
    if form.is_valid():
        form.save()
        return redirect('viewissuedbook')
    return render(request, 'librarian/return_issued_book.html', {'form':form})




## STUDENT Views ##

def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1':form1,'form2':form2}
    if request.method =='POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2=f2.save()

            enrol = form2.cleaned_data.get('enrollment')
            if len(enrol) == 8:
                my_student_group = Group.objects.get_or_create(name='STUDENT')
                my_student_group[0].user_set.add(user)
                return HttpResponseRedirect('student-login')
            else:
                return render(request,'student/studentsignup.html', {'form1':form1,'form2':form2,'error':"Sorry!, Enrolment number must be 8 numbers"})
    return render(request,'student/studentsignup.html',context=mydict)


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')


@login_required(login_url='student-login')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment).filter(is_returned='NO')
    li1=[]
    li2=[]
    for ib in issuedbook:
        books= models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].department, book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'student/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})
