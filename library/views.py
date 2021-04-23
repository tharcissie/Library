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
    return render(request,'library/index.html', context)


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'admin/adminclick.html')


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
            return HttpResponseRedirect('afterlogin')
    return render(request,'super/addlibrarian.html',{'form':form})



def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)


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
        return render(request,'super/super.html', context)
    else:
        return render(request,'library/studentafterlogin.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form=forms.BookForm()
    if request.method=='POST':
        form=forms.BookForm(request.POST or None,files=request.FILES)
        if form.is_valid():
            user=form.save()
            return render(request,'admin/bookadded.html')
    return render(request,'admin/addbook.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_view(request, id):
    context ={}
    book = get_object_or_404(models.Book, id = id)
    form = forms.BookForm(request.POST or None, instance = book)
    if form.is_valid():
        form.save()
        return Redirect('viewbook')
    context["form"] = form
    return render(request, "admin/update_book.html", context)


def delete_view(request, id):
    context ={}
    book = get_object_or_404(models.Book, id = id)
    if request.method =="POST":
        book.delete()
        return redirect("viewbook")
    return render(request, "admin/deletebook.html", context)


#def return_book(request):
 #   request_id = request.GET.get('request_id')
  #  book = IssuedBook.objects.get(id=request_id)
   # book.status = 'returned'
    #book.save()

   # return render(request, 'admin/viewissuedbook.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books= models.Book.objects.all()
    return render(request,'admin/viewbook.html',{'books':books})

@login_required(login_url='login')
def viewbook(request):
    books= models.Book.objects.all()
    return render(request,'super/viewbook.html',{'books':books})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'admin/bookissued.html')
    return render(request,'admin/issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all().filter(is_returned='NO')
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        print(date.today())
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

    return render(request,'admin/viewissuedbook.html',{'li':li})


def viewissuedbook(request):
    issuedbooks=models.IssuedBook.objects.all().filter(is_returned='NO')
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        print(date.today())
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

    return render(request,'super/issuedbook.html',{'li':li})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def return_issued_book_view(request, id):
    issued_book = models.IssuedBook.objects.get(id=id)
    form = forms.ReturnIssuedBookForm(request.POST or None, instance=issued_book)
    if form.is_valid():
        form.save()
        return redirect('viewissuedbook')
    return render(request, 'admin/return_issued_book.html', {'form':form})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'admin/viewstudent.html',{'students':students})


def viewstudent(request):
    students=models.StudentExtra.objects.all()
    return render(request,'super/students.html',{'students':students})


@login_required(login_url='studentlogin')
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
        print(date.today())
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})


