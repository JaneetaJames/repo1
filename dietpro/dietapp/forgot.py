import random
import string


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



