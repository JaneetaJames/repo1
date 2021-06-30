from django.db import models

# Create your models here.
class admin(models.Model):
    uname = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)



class user(models.Model):
    uid = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    gender=models.CharField(max_length=15)
    dob = models.DateField()
    email = models.EmailField(max_length=100)
    ph = models.CharField(max_length=100)
    uname = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)


class dProfile(models.Model):
    did = models.IntegerField()
    lno = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(max_length=100)
    ph = models.CharField(max_length=100)
    qual = models.CharField(max_length=100)
    spec = models.CharField(max_length=150)
    exp = models.DateField()
    uname = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    dp= models.ImageField(upload_to="profilepic/",default=0)
    file = models.CharField(max_length=100)
    status = models.CharField(max_length=40)


class Category(models.Model):
    options = (
        ('breakfast', 'breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
        ('snacks', 'snacks'),
    )
    name = models.CharField(max_length=50, choices=options)


class Fooditem(models.Model):
    name = models.CharField(max_length=200,unique=True)
    category = models.CharField(choices=Category.options,max_length=50)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calorie = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class UserCaloryDetail(models.Model):
    customer = models.ForeignKey(user,on_delete=models.CASCADE)
    cat=models.CharField(max_length=30)
    date=models.DateField()
    food1=models.CharField(max_length=60,default=None)
    food2=models.CharField(max_length=60,default=None)
    food3=models.CharField(max_length=60,default=None)
    food4=models.CharField(max_length=60,default=None)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calorie = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
