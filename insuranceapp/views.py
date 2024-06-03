from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from . models import *

# Create your views here.

def home(request):
    return render(request,'home.html')

def loginpage(request):
    return render(request,'login.html')

def adminhome(request):
    return render(request,'admin/adminhome.html')

def login(request):
    if request.method == "POST":
        un = request.POST.get('u_name')
        ps = request.POST.get('pass')
        user = auth.authenticate(username = un,password = ps)

        if user is not None:
            auth.login(request,user)

            if request.user.is_superuser == 1:
                return redirect('admin_home')
            else:
                return redirect('agent_home')
        else:
            messages.error(request,'User not found')
            return redirect('login_page')
    else:
        return redirect('login_page')
    
def addagencypage(request):
    data = agent.objects.all()
    return render(request,'admin/addagency.html',{'agen':data})

def addagent(request):
    if request.method == "POST":
        fn = request.POST.get('f_name')
        ln = request.POST.get('l_name')
        un = request.POST.get('u_name')
        an = request.POST.get('a_number')
        pan = request.POST.get('pan')
        db = request.POST.get('dob')
        qua = request.POST.get('quali')
        gen = request.POST.get('gent')
        add = request.POST.get('address')
        num = request.POST.get('num')
        em = request.POST.get('e_mail')
        passw = request.POST.get('pass')
        cpassw = request.POST.get('c_pass')
        img = request.FILES.get('img')

        if User.objects.filter(username=un).exists():
            messages.error(request,'This username is already exist')
            return redirect('admin_home')
        elif User.objects.filter(email=em).exists():
            messages.error(request,'This email is already exist')
            return redirect('admin_home')
        elif len(passw) != 6:
            messages.error(request,'Password must be 6 characters')
            return redirect('admin_home')
        elif passw != cpassw:
            messages.error(request,'Password and conform password are incorrect')
            return redirect('admin_home')
        else:
            user = User.objects.create_user(first_name = fn,last_name = ln,email = em,username = un,password = passw)
            uid = User.objects.get(id=user.id)
            agent.objects.create(aadaar_number = an,pan_number = pan,dob = db,qualification = qua,gender = gen,address = add,phone_number = num,user = uid,profile = img)
            messages.success(request,'Register successfully')
            return redirect('admin_home')
    return redirect('admin_home')

def logout(request):
    auth.logout(request)
    return redirect('home')

def viewagent(request,dd):
    data = agent.objects.get(id=dd)
    return render(request,'admin/viewagent.html',{'view':data})

def deleteagent(request,dd):
    data = agent.objects.get(id=dd)
    use = User.objects.get(id=data.user.id)
    data.delete()
    use.delete()
    return redirect('add_agency_page')

def editagent(request,dd):
    data = agent.objects.get(id=dd)
    return render(request,'admin/editagent.html',{'editage':data})

def edit(request,dd):
    data = agent.objects.get(id=dd)
    if request.method == "POST":
        data.user.first_name = request.POST.get('f_name')
        data.user.last_name = request.POST.get('l_name')
        data.aadaar_number = request.POST.get('a_number')
        data.pan_number = request.POST.get('pan')
        data.qualification = request.POST.get('quali')
        data.gender = request.POST.get('gent')
        data.address = request.POST.get('address')
        data.phone_number = request.POST.get('num')
        ph = request.POST.get('num')

        old = data.profile
        new = request.FILES.get('img')

        if old != None and new == None:
            data.profile = old
        else:
            data.profile = new

        olduser = data.user.username
        newuser = request.POST.get('u_name')

        oldmail = data.user.email
        newmail = request.POST.get('e_mail')

        if User.objects.filter(username = newuser).exists():
            if newuser == olduser:
                if User.objects.filter(email = newmail).exists():
                    if newmail == oldmail:
                        if not newmail.endswith('@gmail.com'):
                            messages.error(request,'invalid email!')
                            return redirect('edit_agent',dd=dd)
                        elif len(ph) != 10:
                            messages.error(request,'invalid Phone number!')
                            return redirect('edit_agent',dd=dd)
                        else:
                            data.user.username = newuser
                            data.user.email = newmail
                            data.user.save()
                            data.save()
                            messages.success(request,'Update successfully')
                            return redirect('edit_agent',dd=dd)
                    else:
                        messages.error(request,'This email is already exists')
                        return redirect('edit_agent',dd=dd)
                else:
                    if not newmail.endswith('@gmail.com'):
                        messages.error(request,'invalid email!')
                        return redirect('edit_agent',dd=dd)
                    elif len(ph) != 10:
                        messages.error(request,'invalid Phone number!')
                        return redirect('edit_agent',dd=dd)
                    else:
                        data.user.username = newuser
                        data.user.email = newmail
                        data.user.save()
                        data.save()
                        messages.success(request,'Update successfully')
                        return redirect('edit_agent',dd=dd)
            else:
                messages.error(request,'This Username is already exists')
                return redirect('edit_agent',dd=dd)
        else:
            if User.objects.filter(email = newmail).exists():
                if newmail == oldmail:
                    if not newmail.endswith('@gmail.com'):
                        messages.error(request,'invalid email!')
                        return redirect('edit_agent',dd=dd)
                    elif len(ph) != 10:
                        messages.error(request,'invalid Phone number!')
                        return redirect('edit_agent',dd=dd)
                    else:
                        data.user.username = newuser
                        data.user.email = newmail
                        data.user.save()
                        data.save()
                        messages.success(request,'Update successfully')
                        return redirect('edit_agent',dd=dd)
                else:
                        messages.error(request,'This email is already exists')
                        return redirect('edit_agent',dd=dd)
            else:
                if not newmail.endswith('@gmail.com'):
                    messages.error(request,'invalid email!')
                    return redirect('edit_agent',dd=dd)
                elif len(ph) != 10:
                    messages.error(request,'invalid Phone number!')
                    return redirect('edit_agent',dd=dd)
                else:
                    data.user.username = newuser
                    data.user.email = newmail
                    data.user.save()
                    data.save()
                    messages.success(request,'Update successfully')
                    return redirect('edit_agent',dd=dd)
    return redirect('edit_agent',dd=dd)

def agenthome(request):
    data = request.user
    da = agent.objects.get(user=data.id)
    return render(request,'agent/agenthome.html',{'agent':da})

