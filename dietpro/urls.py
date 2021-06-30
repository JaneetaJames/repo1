"""dietpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from dietpro import settings
from dietpro.dietapp import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',views.index),
    path('home/',views.index),
    path('login/',views.login),
    path('logout/',views.logout),
    path('contact/',views.contact),
    path('forgot/', views.forgot),

    ##ADMIN
    path('adHome/',views.adHome),
    path('ad_viewNewdoctor/', views.ad_viewNewdoctor),
    path('docManage/', views.manageDoc),
    path('viewDoctorlist/', views.viewDoctorlist),
    path('viewBlockedDoctors/',views.blockedDoctors),

    path('viewUserlist/', views.viewUserlist),
    path('viewBlockedUsers/',views.blockedUsers),
    path('adViewFood/',views.adminViewFood),



    # USER
    path('userHome/', views.userHome),
    path('userregpage/', views.userregpage),
    path('uregisterdb/', views.uregisterdb),
    path('calorieCalc/', views.calorieCalc),
    path('viewUserCal/', views.viewUserCal),

    path('uProfileView/', views.myProfile),
    path('userPwdUpdate/', views.uPwd),
    path('userMailUpdate/', views.uMail),
    path('userPhoneUpdate/', views.uPhone),


    # Doctor
    path('docHome/', views.docHome),

    path('Doctor_registration/', views.doctorregpage),
    path('doctorregdb/', views.doc_regdb),

    path('doc_viewprofile/', views.doc_viewprofile),
    path('im/', views.imupload),

    path('mailUpdate/', views.dMail),
    path('phoneUpdate/', views.dPhone),
    path('qualUpdate/', views.qualUpdate),
    path('dPwdUpdate/', views.dPwd),



    path("addfood/",views.docAddfood),
    path("updatefood/",views.docUpdatefood),

]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)