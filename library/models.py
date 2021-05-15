from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta



class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    department = models.CharField(max_length=40, blank=True, null=True)
   
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'

    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biographie'),
        ('history', 'History'),
        ]
    name = models.CharField(max_length=30)
    book_cover_image = models.ImageField(upload_to='cover')
    isbn = models.PositiveIntegerField()
    author = models.CharField(max_length=40)
    category = models.CharField(max_length=30, choices=catchoice, default='education')
    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssuedBook(models.Model):
    BOOK_STATUS = (('YES', 'YES'),('NO', 'NO'))

    enrollment=models.CharField(max_length=30)
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    is_returned = models.CharField(max_length=10, choices = BOOK_STATUS, default = 'NO')
    
    def __str__(self):
        return self.enrollment
