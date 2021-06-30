import random
import string

from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.db.models import Q
import datetime

from django.contrib import messages
from .import form
from .form import fooditemForm
from .models import dProfile, admin, user, Fooditem, UserCaloryDetail
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage

from ..settings import EMAIL_HOST_USER


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


def login(request):
    utype = request.POST.get('utype')
    uname1 = request.POST.get('uname')
    pwd = request.POST.get('pwd')
    if utype == 'Admin':
        try:
            if admin.objects.get(uname=uname1) is not None:  #check whether uname exist in table
                ad = admin.objects.get(uname=uname1)     #get row from table with column uname= uname
                if pwd == ad.pwd:                       #if pwd== pwd in table row
                    request.session['sid'] = ad.uname   #set session
                    return render(request, 'admin/adminHome.html', {'uname': uname1})
                else:
                    return HttpResponse(" Incorrect Password")
        except:
            return HttpResponse("Username Doesn't Exist")


    elif utype == 'Dietitian':

        if dProfile.objects.get(uname=uname1) is not None:
            print("not nont")
            doc = dProfile.objects.get(uname=uname1)
            if pwd == doc.pwd:
                request.session['sid'] = doc.uname
                st = doc.status
                print("status=", st)

                return render(request, 'doctor/docHome.html', {'doc': doc,'status':st})
            else:
                return HttpResponse(" Incorrect Password")
        else:
            return HttpResponse("Username doesn't exist")
    else:
        if user.objects.get(uname=uname1) is not None:
            print("not nont")
            user1 = user.objects.get(uname=uname1)
            if pwd == user1.pwd:
                print("corct pwd")
                request.session['sid'] = user1.uname
                print("session set")
                return userHome(request)
            else:
                return HttpResponse(" Incorrect Password")
        else:
            return HttpResponse("Username doesn't exist")

def logout(request):
    try:
        #Session.objects.all().delete()
        request.session['sid'].delete()
        return render(request, 'index.html')
    except:
        print('exception')
        return render(request, 'index.html')

def forgot(request):
    if request.method=="POST":
        mail=request.POST.get('email')
        uname1=request.POST.get('uname')

        try:
            if request.POST.get('utype') == "Admin":

                obj=admin.objects.get(uname=uname1,email=mail)
                ustype="Admin"
            elif request.POST.get('utype') == "Dietitian":
                obj =dProfile.objects.get(uname=uname1, email=mail)
                ustype = "Dietitian"
            else:
                obj = user.objects.get(uname=uname1, email=mail)
                ustype = "User"
        except:
            return render(request, 'index.html', {'msg1': 2})


        if 'otpsend' in  request.POST:
            try:
                n = 4
                res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=n))
                obj.otp=res
                obj.save()
                subject = 'OTP to change Password'
                message = 'Your OTP is'+res
                recepient = str(mail)
                print("RECEPIENT",recepient)
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
                print("Successfull")
                return render(request,'forgot.html',{'otp':res,'uname':uname1,'mail':mail,'utype':ustype,'form':2})
            except:
                return render(request,'forgot.html',{'utype':ustype,'uname':uname1,'mail':mail,'form':3,'msg':"OTP sending Unsuccessfull"})


        elif 'confirmOTP' in request.POST:
            if request.POST.get('uotp') == request.POST.get('otp'):
                return render(request,'forgot.html',{'utype':ustype,'uname':uname1,'mail':mail,'form':3})
            else:
                return render(request,'forgot.html',{'utype':ustype,'uname':uname1,'mail':mail,'form':3,'msg':"OTP Not MAtched"})



        elif 'updatePWD' in request.POST:
                obj.pwd=request.POST.get('newpwd')
                obj.save()
                return render(request,'index.html',{'msg1':1})

    return render(request,'forgot.html',{'form':1})















def adHome(request):
    return render(request, 'admin/adminHome.html', {'uname': request.session['sid']})


def ad_viewNewdoctor(request):

    if dProfile.objects.filter(Q(status='pending') | Q(status='rejected')) is not None:
        new=dProfile.objects.filter(Q(status='pending') | Q(status='rejected'))     #select rows where status='pending' or status='rejected'

        return render(request,'admin/ad_viewDoctor.html',{'doc':new,'status':"new"})


def manageDoc(request):
    id=request.POST.get('did')
    doc=dProfile.objects.get(did=id)
        #manage new doctor registration(approve/reject button)
    if 'approve' in request.POST:
        doc.status='active'     #update status from 'pending' to 'active'
        doc.save()              #save to db
        return viewDoctorlist(request)
    elif 'reject' in request.POST:
        doc.status='rejected'
        doc.save()
        return ad_viewNewdoctor(request)

    elif 'deactivate' in request.POST and doc.status=="active":
        doc.status = 'deactivated'
        doc.save()
        return blockedDoctors(request)



def viewDoctorlist(request):
    if dProfile.objects.filter(status='active') is not None:
        doclist = dProfile.objects.filter(status='active')

        return render(request, 'admin/ad_viewDoctor.html', {'doc': doclist,'status':"active"})
    else:
        return HttpResponse("no active users")

def blockedDoctors(request):
    if dProfile.objects.filter(status='deactivated') is not None:
        doclist = dProfile.objects.filter(status='deactivated')

        return render(request, 'admin/ad_viewDoctor.html', {'doc': doclist,'status':'blocked'})
    else:
        return HttpResponse("no deactivated users")



def viewUserlist(request):
    ulist = user.objects.all()
    return render(request, 'admin/ad_viewUsers.html', {'udata': ulist,'status':"active"})


def blockedUsers(request):
    if user.objects.filter(status='deactivated') is not None:
        ulist = user.objects.filter(status='deactivated')
        return render(request, 'admin/ad_viewUsers.html', {'udata': ulist,'status':"deactive"})
    else:
        return HttpResponse("no active users")


def adminViewFood(request):
    food1=Fooditem.objects.all()
    return render(request, 'admin/viewFood.html', {'food':food1})


#USER



def userHome(request):
    obj=user.objects.get(uname=request.session['sid'])
    cat = Fooditem.objects.values('category').distinct()
    food = Fooditem.objects.all()
    list = []
    for x in cat:
        list.append(x['category'])
    print(list)

    return render(request, 'user/userHome.html', {"udata": obj,'cat':list,'food':food})


def getUid(request):
    obj=user.objects.get(uname=request.session['sid'])
    uid=obj.uid
    return uid


def userregpage(request):

    if not user.objects.all():
        return render(request, 'user/userregistration.html',{'uid':4000})
    else:
        uid = user.objects.order_by('-uid').first().uid + 1
        return render(request, 'user/userregistration.html', {'uid': uid})


def uregisterdb(request):
    user1 = user.objects.all()
    for x in user1:
            if x.uname == request.POST.get('uname'):
                return HttpResponse("Username allready registered")
            elif x.email == request.POST.get('email'):
                return HttpResponse("Mail Id allready registered")
            elif x.ph == request.POST.get('phone'):
                return HttpResponse("Licence number allready registered")
            else:
                pass

    db = user(uid=request.POST.get('uid'), fname=request.POST.get('fname'), lname=request.POST.get('lname'),
            dob=request.POST.get('dob'), gender=request.POST.get('gender'), email=request.POST.get('email'),ph=request.POST.get('phone'),
            uname=request.POST.get('uname'),pwd=request.POST.get('pwd'))

            #save html form data to db

    db.save()
    return index(request)

def calorieCalc(request):
    ftype=request.POST.get('cat')
    f1=str(request.POST.get('sym2'))
    f2=str(request.POST.get('sym3'))
    f3=str(request.POST.get('sym4'))
    f4=str(request.POST.get('sym5'))
    if f2=="Select Here":
        f2="No item"
    if f3=="Select Here":
        f3="No item"

    if f4=="Select Here":
        f4="No item"


    print(f1,f2,f3,f4)
    total_cal = 0
    total_carb = 0
    total_pro = 0
    total_fat = 0
    if f1 is not None:
        obj1=Fooditem.objects.get(name=f1)
        total_cal+=obj1.calorie
        total_carb+=obj1.carbohydrate
        total_fat+=obj1.fats
        total_pro+=obj1.protein
    if f2 is not None:
        try:
            obj2=Fooditem.objects.get(name=f2)
            total_cal+=obj2.calorie
            total_carb+=obj2.carbohydrate
            total_fat+=obj2.fats
            total_pro+=obj2.protein
        except:
            obj2=None

    if f3 is not None:
        try:
            obj3=Fooditem.objects.get(name=f3)
            total_cal+=obj3.calorie
            total_carb+=obj3.carbohydrate
            total_fat+=obj3.fats
            total_pro+=obj3.protein
        except:
            obj3=None
    if f1 is not None:
        try:

            obj4=Fooditem.objects.get(name=f4)
            total_cal+=obj4.calorie
            total_carb+=obj4.carbohydrate
            total_fat+=obj4.fats
            total_pro+=obj4.protein
        except:
            pass

    obj = user.objects.get(uname=request.session['sid'])
    cat = Fooditem.objects.values('category').distinct()
    food = Fooditem.objects.all()
    list = []
    for x in cat:
        list.append(x['category'])
    print(list)
    us=user.objects.get(uname=request.session['sid'])

    obj_cal=UserCaloryDetail(
    customer=us,
    cat = ftype,
    food1 =f1,
    food2 =f2,
    food3 =f3,
    food4 =f4,
    carbohydrate = total_carb,
    fats = total_fat,
    protein =total_pro ,
    calorie =total_cal,
    date=datetime.datetime.now().date())
    obj_cal.save()

    return render(request, 'user/userHome.html', {"udata": obj,'cat': list, 'food': food,'cal':total_cal,'carb':total_carb,'pro':total_pro,'fat':total_fat})

def viewUserCal(request):
    user1=user.objects.get(uname=request.session['sid'])
    obj=UserCaloryDetail.objects.filter(customer=user1)
    return render(request,'user/calory details.html',{'res':obj})


#####DOCTOR



def getDid(request):
    obj=dProfile.objects.get(uname=request.session['sid'])
    did=obj.did
    return did

def docHome(request):

    doc = dProfile.objects.get(uname= request.session['sid'])
    st = doc.status
    return render(request, 'doctor/docHome.html', {'doc': doc, 'status': st})


def doctorregpage(request):

    if not dProfile.objects.all():
        return render(request, 'doctor/doc_registration.html',{'did':2000})
    else:
        did = dProfile.objects.order_by('-did').first().did + 1
        return render(request, 'doctor/doc_registration.html', {'did': did})

def doc_regdb(request):
    doc = dProfile.objects.all()
    if request.method == 'POST' and request.FILES['cert'] :
        print("yes")
        #certificate
        certificate = request.FILES['cert']
        fs = FileSystemStorage()
        fname = certificate.name
        fsize = certificate.size
        print(fname)
        print(fsize)
        filename = fs.save(fname, certificate)
        certificate_url = fs.url(filename)


        for x in doc:
            if x.uname == request.POST.get('uname'):
                return HttpResponse("Username allready registered")
            elif x.email == request.POST.get('email'):
                return HttpResponse("Mail Id allready registered")
            elif x.lno == request.POST.get('lno'):
                return HttpResponse("Licence number allready registered")
            else:
                pass

        db = dProfile(did=request.POST.get('did'), fname=request.POST.get('fname'), lname=request.POST.get('lname'),
                      dob=request.POST.get('dob'),gender=request.POST.get('gender'), email=request.POST.get('email'),
                      ph=request.POST.get('ph'),
                      lno=request.POST.get('lno'),qual=request.POST.get('qual'),spec = request.POST.get('spec'),
                      exp =request.POST.get('exp'),uname=request.POST.get('uname'), pwd=request.POST.get('pwd'),

                      file=certificate_url, status="pending")
        db.save()


        return index(request)

def imupload(request):

    doc = dProfile.objects.get(uname=request.session['sid'])
    dp=form.Abc(request.POST,request.FILES)
    if dp.is_valid():
        print("valid")
        doc.dp=dp.cleaned_data['profile_pic']
        doc.save()
        return doc_viewprofile(request)
    return doc_viewprofile(request)


def doc_viewprofile(request):

    dp = form.Abc(request.POST, request.FILES)
    doc=dProfile.objects.get(uname=request.session['sid'])
    st=doc.status
    print("doc.dp=",doc.dp)

    if doc.dp=='0':
        return render(request, 'doctor/dProfileView.html', {"x":'0','doc': doc,'form':dp,'status':st})

    else:
        return render(request, 'doctor/dProfileView.html', {'doc': doc,'status':st})

#Updates

def dMail(request):
    us = dProfile.objects.get(uname=request.session['sid'])
    return mailUpdate(request, us)
def dPhone(request):
    us = dProfile.objects.get(uname=request.session['sid'])
    return phoneUpdate(request, us)

def dPwd(request):
    doc=dProfile.objects.get(uname=request.session['sid'])
    return pwdUpdate(request, doc)



def qualUpdate(request):
    if request.method == 'POST' and request.FILES['cert']:
        print("yes")
        # certificate
        certificate = request.FILES['cert']
        fs = FileSystemStorage()
        fname = certificate.name
        fsize = certificate.size
        print(fname)
        print(fsize)
        filename = fs.save(fname, certificate)
        certificate_url = fs.url(filename)

    doc=dProfile.objects.get(uname=request.session['sid'])
    x=doc.qual
    doc.qual=request.POST.get('qual'),x
    doc.file=certificate_url
    doc.save()
    return doc_viewprofile(request)











def myProfile(request):
    user1=user.objects.get(uname=request.session['sid'])
    return render(request,'user/uProfile.html',{'user1':user1})








def pwdUpdate(request,obj):
    print("pwd", obj.pwd)
    print("pwd1", request.POST.get('pwd1'))
    if obj.pwd==request.POST.get('pwd1'):
        obj.pwd=request.POST.get('pwd2')
    else:
        return HttpResponse("Current password is incorrect")
    obj.save()
    try:
        if obj.did:
            return doc_viewprofile(request)
    except:
        return myProfile(request)


def mailUpdate(request, objt):
    try:
        if  objt.did:
            doc1 = dProfile.objects.all()
    except:
        doc1 = user.objects.all()

    for x in doc1:
        if x.email == request.POST.get('email') and x.uname!=request.session['sid']:
            return HttpResponse("Mail id allready exist")

    objt.email=request.POST.get('email')
    objt.save()
    try:
        if objt.did:
            return doc_viewprofile(request)
    except:
        return myProfile(request)


def phoneUpdate(request,obj):
    try:
        if  obj.did:
            doc1 = dProfile.objects.all()
    except:
        doc1 = user.objects.all()

    for x in doc1:
        if x.ph==request.POST.get('ph') and x.uname!=request.POST.get('uname'):
            return HttpResponse("Phone Number allready exist")

    obj.ph=request.POST.get('ph')
    obj.save()
    try:
        if obj.did:
            return doc_viewprofile(request)
    except:
        return myProfile(request)


def uPhone(request):
    us = user.objects.get(uname=request.session['sid'])
    return phoneUpdate(request, us)
def uMail(request):
    us = user.objects.get(uname=request.session['sid'])
    return mailUpdate(request, us)

def uPwd(request):
    us=user.objects.get(uname=request.session['sid'])
    return pwdUpdate(request,us)



def docAddfood(request):

    form = fooditemForm()
    if request.method == 'POST':
        form = fooditemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/addfood/')
    context={'form':form}
    return render(request,'doctor/addFood.html',context)

def docUpdatefood(request):
    food1=Fooditem.objects.all()

    if request.method=='POST':
        food = Fooditem.objects.get(id=request.POST.get('id'))
        food.carbohydrate=request.POST.get('carb')
        food.fats=request.POST.get('fats')
        food.protein=request.POST.get('protein')
        food.calorie=request.POST.get('calorie')
        food.quantity=request.POST.get('quantity')
        food.save()

    return render(request,'doctor/updateFood.html',{'food':food1})
