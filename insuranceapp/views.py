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
                return redirect('add_agency_page')
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
        elif len(an) != 12:
            messages.error(request,'Please enter the valid aathaar number')
            return redirect('admin_home')
        elif not any(i.isupper() for i in pan):
            messages.error(request,'Invalid pan number')
            return redirect('admin_home')
        elif len(pan) != 10:
            messages.error(request,'Invalid pan number')
            return redirect('admin_home')
        elif len(num) != 10:
            messages.error(request,'Invalid phone number')
            return redirect('admin_home')
        elif not any(i.isupper() for i in passw):
            messages.error(request,'Password must be atleast one Capital letter')
            return redirect('admin_home')
        elif not any(i.islower() for i in passw):
            messages.error(request,'Password must be atleast one Small letter')
            return redirect('admin_home')
        elif not any(i.isdigit() for i in passw):
            messages.error(request,'Password must be atleast one number')
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
    da = customer.objects.filter(agentno=dd)
    s=0
    for i in da:
        s=s+1
    s=s
    return render(request,'admin/viewagent.html',{'view':data,'tot':s})

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
        an = request.POST.get('a_number')
        data.pan_number = request.POST.get('pan')
        pan = request.POST.get('pan')
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
                        elif len(an) != 12:
                            messages.error(request,'invalid Aadhar number!')
                            return redirect('edit_agent',dd=dd)
                        elif not any(i.isupper() for i in pan):
                            messages.error(request,'invalid Pan number!')
                            return redirect('edit_agent',dd=dd)
                        elif len(pan) != 10:
                            messages.error(request,'Invalid pan number')
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
                    elif len(an) != 12:
                        messages.error(request,'invalid Aadhar number!')
                        return redirect('edit_agent',dd=dd)
                    elif not any(i.isupper() for i in pan):
                        messages.error(request,'invalid Pan number!')
                        return redirect('edit_agent',dd=dd)
                    elif len(pan) != 10:
                        messages.error(request,'Invalid pan number')
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
                    elif len(an) != 12:
                        messages.error(request,'invalid Aadhar number!')
                        return redirect('edit_agent',dd=dd)
                    elif not any(i.isupper() for i in pan):
                        messages.error(request,'invalid Pan number!')
                        return redirect('edit_agent',dd=dd)
                    elif len(pan) != 10:
                        messages.error(request,'Invalid pan number')
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
                elif len(an) != 12:
                    messages.error(request,'invalid Aadhar number!')
                    return redirect('edit_agent',dd=dd)
                elif not any(i.isupper() for i in pan):
                    messages.error(request,'invalid Pan number!')
                    return redirect('edit_agent',dd=dd)
                elif len(pan) != 10:
                    messages.error(request,'Invalid pan number')
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

def editprofile(request,dd):
    data = agent.objects.get(id=dd)
    return render(request,'agent/editprofile.html',{'profile':data})

def editpro(request,dd):
    data = agent.objects.get(id=dd)
    if request.method == "POST":
        data.user.first_name = request.POST.get('f_name')
        data.user.last_name = request.POST.get('l_name')
        data.aadaar_number = request.POST.get('a_number')
        an = request.POST.get('a_number')
        data.pan_number = request.POST.get('pan')
        pan = request.POST.get('pan')
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
                            return redirect('edit_profile',dd=dd)
                        elif len(an) != 12:
                            messages.error(request,'invalid Aadhar number!')
                            return redirect('edit_profile',dd=dd)
                        elif not any(i.isupper() for i in pan):
                            messages.error(request,'invalid Pan number!')
                            return redirect('edit_profile',dd=dd)
                        elif len(pan) != 10:
                            messages.error(request,'Invalid pan number')
                            return redirect('edit_profile',dd=dd)
                        elif len(ph) != 10:
                            messages.error(request,'invalid Phone number!')
                            return redirect('edit_profile',dd=dd)
                        else:
                            data.user.username = newuser
                            data.user.email = newmail
                            data.user.save()
                            data.save()
                            messages.success(request,'Update successfully')
                            return redirect('edit_profile',dd=dd)
                    else:
                        messages.error(request,'This email is already exists')
                        return redirect('edit_profile',dd=dd)
                else:
                    if not newmail.endswith('@gmail.com'):
                        messages.error(request,'invalid email!')
                        return redirect('edit_profile',dd=dd)
                    elif len(an) != 12:
                        messages.error(request,'invalid Aadhar number!')
                        return redirect('edit_profile',dd=dd)
                    elif not any(i.isupper() for i in pan):
                        messages.error(request,'invalid Pan number!')
                        return redirect('edit_profile',dd=dd)
                    elif len(pan) != 10:
                        messages.error(request,'Invalid pan number')
                        return redirect('edit_profile',dd=dd)
                    elif len(ph) != 10:
                        messages.error(request,'invalid Phone number!')
                        return redirect('edit_profile',dd=dd)
                    else:
                        data.user.username = newuser
                        data.user.email = newmail
                        data.user.save()
                        data.save()
                        messages.success(request,'Update successfully')
                        return redirect('edit_profile',dd=dd)
            else:
                messages.error(request,'This Username is already exists')
                return redirect('edit_profile',dd=dd)
        else:
            if User.objects.filter(email = newmail).exists():
                if newmail == oldmail:
                    if not newmail.endswith('@gmail.com'):
                        messages.error(request,'invalid email!')
                        return redirect('edit_profile',dd=dd)
                    elif len(an) != 12:
                        messages.error(request,'invalid Aadhar number!')
                        return redirect('edit_profile',dd=dd)
                    elif not any(i.isupper() for i in pan):
                        messages.error(request,'invalid Pan number!')
                        return redirect('edit_profile',dd=dd)
                    elif len(pan) != 10:
                        messages.error(request,'Invalid pan number')
                        return redirect('edit_profile',dd=dd)
                    elif len(ph) != 10:
                        messages.error(request,'invalid Phone number!')
                        return redirect('edit_profile',dd=dd)
                    else:
                        data.user.username = newuser
                        data.user.email = newmail
                        data.user.save()
                        data.save()
                        messages.success(request,'Update successfully')
                        return redirect('edit_profile',dd=dd)
                else:
                        messages.error(request,'This email is already exists')
                        return redirect('edit_profile',dd=dd)
            else:
                if not newmail.endswith('@gmail.com'):
                    messages.error(request,'invalid email!')
                    return redirect('edit_profile',dd=dd)
                elif len(an) != 12:
                    messages.error(request,'invalid Aadhar number!')
                    return redirect('edit_profile',dd=dd)
                elif not any(i.isupper() for i in pan):
                    messages.error(request,'invalid Pan number!')
                    return redirect('edit_profile',dd=dd)
                elif len(pan) != 10:
                    messages.error(request,'Invalid pan number')
                    return redirect('edit_profile',dd=dd)
                elif len(ph) != 10:
                    messages.error(request,'invalid Phone number!')
                    return redirect('edit_profile',dd=dd)
                else:
                    data.user.username = newuser
                    data.user.email = newmail
                    data.user.save()
                    data.save()
                    messages.success(request,'Update successfully')
                    return redirect('edit_profile',dd=dd)
    return redirect('edit_profile',dd=dd)

def deleteprofile(request,dd):
    data = agent.objects.get(id=dd)
    use = User.objects.get(id=data.user.id)
    data.delete()
    use.delete()
    return redirect('home')

def addcustomer(request):
    return render(request,'agent/addcustomer.html')

def addcus(request):
    if request.method == "POST":
        fn = request.POST.get('f_name')
        ln = request.POST.get('l_name')
        un = request.POST.get('username')
        an = request.POST.get('a_number')
        pan = request.POST.get('pan')
        db = request.POST.get('dob')
        qua = request.POST.get('quali')
        gen = request.POST.get('gent')
        add = request.POST.get('address')
        num = request.POST.get('num')
        img = request.FILES.get('img')
        age = request.POST.get('ag')
        occup = request.POST.get('occupi')
        income  = request.POST.get('income')
        select = request.POST.get('yes')
        how = request.POST.get('known')
        c_service = request.POST.get('service')
        m_area = request.POST.get('markup')
        p_insurance = request.POST.get('willing')
        s_insurance = request.POST.get('share')
        comment = request.POST.get('comments')
        switch = request.POST.get('switch')
        c_name = request.POST.get('c_name')
        i_name = request.POST.get('i_name')

        data = request.user
        da = agent.objects.get(user=data.id)
        dat = agent.objects.get(id=da.id)


        if len(num) != 10:
            messages.error(request,'invalid Phone number!')
            return redirect('add_customer')
        elif len(an) != 12:
            messages.error(request,'invalid Aadhar number!')
            return redirect('add_customer')
        elif not any(i.isupper() for i in pan):
            messages.error(request,'invalid Pan number!')
            return redirect('add_customer')
        elif len(pan) != 10:
            messages.error(request,'Invalid pan number')
            return redirect('add_customer')
        elif User.objects.filter(username=un).exists():
            messages.error(request,'Use another username')
            return redirect('add_customer')
        else:
            user = User.objects.create_user(first_name = fn,last_name = ln,username = un)
            uid = User.objects.get(id=user.id)
            customer.objects.create(aadhar_number = an,pan_number = pan,dob = db,qualification = qua,gender = gen,address = add,phone_number = num,user = uid,profile = img,age = age,profession = occup,annual_income = income,kids = select,
                                    how_know = how,agentno = dat,feedback = c_service,markup_area = m_area,
                                    purchase_insurance = p_insurance,share_insurance = s_insurance,
                                    comments = comment,switch_insurance = switch,company_name = c_name,
                                    insurance_name = i_name)
            messages.success(request,'Register successfully')
            return redirect('add_customer')
    return redirect('add_customer')

def dashboard(request):
    da = request.user
    dat = agent.objects.get(user=da.id)
    data = customer.objects.filter(agentno=dat.id)
    return render(request,'agent/dashboard.html',{'view':data,'agent':dat})

def viewcustomer(request,dd):
    data = customer.objects.get(id=dd)
    return render(request,'agent/viewcustomer.html',{'view':data})

def editcustomer(request,dd):
    da = request.user
    dat = agent.objects.get(user=da.id)
    data = customer.objects.get(id=dd)
    return render(request,'agent/editcustomer.html',{'edit':data,'agent':dat})

def editcus(request,dd):
    data = customer.objects.get(id=dd)
    if request.method == "POST":
        data.user.first_name = request.POST.get('f_name')
        data.user.last_name = request.POST.get('l_name')
        data.phone_number = request.POST.get('num')
        ph = request.POST.get('num')
        data.gender = request.POST.get('gent')
        data.address = request.POST.get('address')
        data.age = request.POST.get('ag')
        data.profession = request.POST.get('occupi')
        data.qualification = request.POST.get('quali')
        data.annual_income  = request.POST.get('income')
        data.aadhar_number = request.POST.get('a_number')
        an = request.POST.get('a_number')
        data.pan_number = request.POST.get('pan')
        pan = request.POST.get('pan')

        old = data.profile
        new = request.FILES.get('img')

        if old != None and new == None:
            data.profile = old
        else:
            data.profile = new

        if len(ph) != 10:
            messages.error(request,'invalid Phone number!')
            return redirect('edit_customer',dd=dd)
        elif len(an) != 12:
            messages.error(request,'invalid Aadhar number!')
            return redirect('edit_customer')
        elif not any(i.isupper() for i in pan):
            messages.error(request,'invalid Pan number!')
            return redirect('edit_customer')
        elif len(pan) != 10:
            messages.error(request,'Invalid pan number')
            return redirect('edit_customer')
        else:
            data.user.save()
            data.save()
            messages.success(request,'Update successfully')
            return redirect('edit_customer',dd=dd)
    return redirect('edit_customer',dd=dd)

def deletecustomer(request,dd):
    data = customer.objects.get(id=dd)
    use = User.objects.get(id=data.user.id)
    data.delete()
    use.delete()
    return redirect('dash_board')

def nocustomer(request,dd):
    data = agent.objects.get(id=dd)
    return render(request,'admin/nocustomer.html',{'dat':data})

def agentviewcustomer(request,dd):
    da = agent.objects.get(id=dd)
    if customer.objects.filter(agentno=dd).exists():
        data = customer.objects.filter(agentno=dd)
        return render(request,'admin/agentcustomer.html',{'customer':data,'dat':da})
    else:
        return redirect('no_customer',dd=dd)

def viewcustomerdetail(request,dd):
    data = customer.objects.get(id=dd)
    return render(request,'admin/viewcustomerdetail.html',{'view':data})

