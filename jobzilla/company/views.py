from cmath import e
from django.db.models.fields import EmailField
from django.http import request
from django.shortcuts import render
from company.models import *
from random import *
import random
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

#<a href="https://www.w3schools.com">Visit W3Schools.com!</a>
#Id Password jzilla 123456
# Create your views here.
# "Render" use karte hai "HTML" ki request ku response karne.
# Without "Render" "Html" display nahi huga.
# User.objects.get() == Use only jab lena hu "Single Value"
# User.objects.filter() == Use jab lena hu "Multi Value"
# "Redirect" use huta hai jab 1Page ku 2Page k Function use karna hu render nahi.
    # Eg -- Logout

# Settings may Send Email shortform "THupp"

# Means uid "Model" may Password "Variable" equal == hai newpassword k                      
# uid.password = newpassword 
# Save karo uid may
                         #uid.save() 




#-------------------> Home
def iindex(request):
    return render(request,"company/index.html")
#--------------------> End





#----------------------> Profile Account Setting

def pasetting(request):
    if 'email' in request.session:
        return render(request,'company/profile-account-setting.html')

#----------------------> End 



#-----------------------> Companies
def companies(request):
    try:
        if 'email' in request.session:
            uid = User.objects.get(email = request.session['email'])
            cid = Company.objects.get(user_id = uid)
            # Jo Company login hai uske shivaye other Company All dekhni chahiye.
            # "Exclude" means Isko Shuud k

            call = Company.objects.exclude(user_id = uid)
            context={
                'uid':uid,
                'cid':cid,
                'call':call,

            }
            return render(request,"company/companies.html",context)
        else: 
            return render(request,"company/companies.html")
    except Exception as e:
        print("------------------>",e)
        return render(request,"company/companies.html")







#-----------------------> End





# -----------------------> Only EmailPage jab Signin/Login Page pay ForgotButton click kare


def forgot(request):
    return render(request,"company/Forgot.html")

#----------------------------> End 

#---------------------> Only EmailPage/Send Otp
def send_otp(request):
    try:
        if request.POST:
            # Verify Django email
            email = request.POST['email']
            # Verify Python email same hai Model email say
            uid = User.objects.get(email = email)
            otp = randint(1111,9999)
        #-------------- uid match huti hai -----------------------    
            if uid:
                # [uid.email]------> Send jis ku karna hai Receiver
                # Email may String may Otp jati hai "OTP String" may convert karne ki 
                send_mail("OTP","OTP for change password"+str(otp),"anjali.20.learn@gmail.com",[uid.email])
                uid.otp = otp
                uid.save()
                return render(request,"company/Reset.html",{'email':email})
        else:
            return render(request,"company/Forgot.html")
    except Exception as e:
        print("---------------->",e)
        e_msg="something went wrong - please check your email"
        return render(request,"company/Forgot.html",{'e_msg':e_msg})

#---------------------------> End



#-------> Start Reset
# Function reset --  Page k Email and password ki value get karne
def reset(request):
# 1 Function Variable 2 Function may use karna hutu Global use huta hai.
# Email error thi kyuki use kar raha tha email per hai rtemail.
    try:
        if request.POST:
            email = request.POST['email']
            newpassword = request.POST['newpassword']
            repassword = request.POST['repassword']
            otp = request.POST['otp']
            uid = User.objects.get(email = email)
            print("newpassword---->",newpassword)
            print("repassword---->",repassword)
            print("email---->",email)
        # ----------------------> Agar uid match
            if uid:
                print("uid ---->",uid)
                if newpassword == repassword:
                    # update new password password 
                    print("---> password change ")
                    print("----> inside the msg ")
                    if str(uid.otp) == otp:
                        uid.password = newpassword 
                        uid.save() 
                    
                        return render(request,"company/Reset.html")
                    else:
                        e_msg="Otp wrong"
                        return render(request,"company/Reset.html",{'e_msg':e_msg,'email':email})
                else:
                    e_msg = "password does not match !!!"
                    print("-----> error msg ",e_msg)
                    return render(request,"company/Reset.html",{'e_msg':e_msg,'email':email})
        else:
            return render(request,"company/Forgot.html")
    except Exception as e:
        print("error Newpassword -------------> ",e)
        e_msg="something went wrong - please check your email"
        return render(request,"company/Reset.html",{'e_msg':e_msg})

#---------------> End

















#----------------------> Start CompanySignUp/Registration
def sign(request):
    #  ------------------------------- DjangoVarible save in PythonVariable---------

    # "Request.POST" means SaveButton click huta function condition check hu
    # Ye nahi huga tu refresh krege tu condition check karne lagega
    try:
        if request.POST:
            # Default role Django may hide kiya hai
            if request.POST['role'] == 'company':
            # Getting Django data shortform "F(request)M(POST)V(DjangoVariable)"
                cname = request.POST['companyname']
                email = request.POST['companyemail']
                ccontact = request.POST['companycontact'] 
                ccity = request.POST['companycity']
                caddress = request.POST['companyaddress']
                ccategory = request.POST['companycategory']

                plist = ['ab123','cd456','ef789','gh1011','ij1213']

                password = random.choice(plist)+ccontact[-3:]
        #   ------------------------------- PythonVariable save in ModelVariable-------------

                uid = User.objects.create(email = email,
                                        password = password,
                                        role = request.POST['role'])
            # ShortForm COCVV    
                cid = Company.objects.create(user_id = uid,
                                            company_name = cname,
                                            company_type = ccategory,
                                            company_address = caddress,
                                            company_contact = ccontact,
                                            company_city = ccity
                                            )
                if cid:
                    s_msg = "Successfully Register"
                    send_mail("Jobzilla","Check your email for otp and password"+password,"anjali.20.learn@gmail.com",['companyemail'])
                    return render(request,"company/sign-in.html",{'s_msg':s_msg})
            else:
                e_msg = "Something Wrong"
                return render(request,"company/sign-in.html",{'e_msg':e_msg})       
        else:
            return render(request,"company/sign-in.html")
    except Exception as e:
        print("------------->",e)
        return render(request,"company/sign-in.html")
    
#----------------------------> End


#--------------> Signin/Login Start
@csrf_exempt
def signin(request):
    # Ye "Login Rhene deta hai" 1 bar login kare tu
    # Nahi tu bar bar logout huga
    try:

        if 'email' in request.session:
        
        # Esmay "Django Variable" ka "Email" compare "Model User Email" say.
        #                      Ye 'email' compare kiya 'Session' may store email say
            uid = User.objects.get(email = request.session['email'])
        # Esmay "Model Company Class" ke "Id" liye compare kiya upper walay "uid" say.
            cid = Company.objects.get(user_id = uid)
            calljob = jobpost.objects.filter(company_id = cid)
            context={
                        'uid':uid,
                        'cid':cid,
                        'calljob':calljob,
                    }
            return render(request,'company/company-profile.html',context)
        else:
            if request.POST:
                email = request.POST['email']
                password = request.POST['password']

                #uid = User.objects.get(email = email)
            # Multiple data lena hu tu filter use karne ka.
                uid = User.objects.filter(email = email)
                
                if uid:
                # "Filter" use kare tu position dena uid[0] ese.
                    if uid[0].password == password:
                        
                        if uid[0].role == 'company':
                    
                            uid = User.objects.get(email = email)
                    # Esmay "Model User Class" ke "All Variable" liye compare kiya upper walay "uid" say.
                            cid = Company.objects.get(user_id = uid)
                    
                            s_msg="Welcome"
        #------------ Session used for temporary store karne data 
                            # Store what "email" kaha say = uid k email say.
                            request.session['email'] = uid.email 
                            # Company JobPost ka data
                            jall = jobpost.objects.filter(company_id = cid).order_by('-create_at')
        #------------ Context use for company name display karne company-profile.html page per 
                            # Python ka data Django may dictionary say lejate hai.
                            context ={
                                'uid':uid,
                                'cid':cid,
                                's_msg':s_msg,
                                'jall':jall,
                             
                                }
                            return redirect('companyprofile')
                        else:
                             # Esmay "Django Variable" ka "Email" compare "Model User Email" say.
                            uid = User.objects.get(email = email)
        # Esmay "Model Company Class" ke "All Variable" liye compare kiya upper walay "uid" say.
                            id = Ruser.objects.get(user_id = uid)
                            # Store session what "email" kaha say = uid k email say.
                            request.session['email'] = uid.email
                            
                            # Python ka data Django may Dictionary se jata hai.
                            #jall = jobpost.objects.filter(company_id = cid).order_by('-create_at')
                            context ={
                                'uid':uid,
                                'id':id,
                                #'jall':jall,
                           
                                }
                            return redirect('userprofilep')
                            #e_msg = "Invalid Password"
                            #return render(request,"company/sign-in.html")
                    else:
                        e_msg = "Email does not exist"
                        return render(request,"company/sign-in.html",{'e_msg':e_msg})
                else:
                    e_msg = "Email does not exist"
                    return render(request,"company/sign-in.html",{'e_msg':e_msg})
            else:
                return render(request,"company/sign-in.html")
    except Exception as e:
        print("------------>",e)
        return render(request,"company/sign-in.html")

#----------------> End   



#----------------> Start Company Profile
def companyprofile(request):
    try:

        if "email" in request.session:
            uid = User.objects.get(email = request.session['email'])
            cid = Company.objects.get(user_id = uid)
            calljob = jobpost.objects.filter(company_id = cid)
            context={
                        'uid':uid,
                        'cid':cid,
                        'calljob':calljob,
                    }
            return render(request,'company/company-profile.html',context)
        # Elif condition hai User Profile jane ki Ya per. User folder walay may dena.
        else:
            return redirect('signin')
    except Exception as e:
        print("-------------->",e)
        return render(request,"company/sign-in.html")
#-----------------> End


#------------------> Start Profile Logout
def profilelogout(request):
    if "email" in request.session:
    # Delete karu 'email' store hai session may
        del request.session['email']
        return render(request,"company/sign-in.html")
    else:
        return render(request,"company/sign-in.html")


#---------------------------> Company Logo
def company_logo(request):
    try:
        if "email" in request.session:
            uid = User.objects.get(email = request.session['email'])
            cid = Company.objects.get(user_id = uid)
        
            if 'company-logo' in request.FILES:    
            
                companylogo = request.FILES['company-logo']

                # cid "Model" hai or company_logo "Model" wala
                # cid k company_logo may save huga companylogo
                # COCVV jesa per Single item insert karna hai esliye
                cid.company_logo = companylogo
                cid.save()
                #Update
            if 'company-coverp' in request.FILES:
                c_cover = request.FILES['company-coverp']
                cid.company_cover = c_cover
                cid.save()


            context ={
                    'uid':uid,
                    'cid':cid,
                }
            return render(request,"company/company-profile.html",context)
        else:
            return redirect('signin')
    except Exception as e:
        print("----------->",e)
        return render(request,"company/sign-in.html")


# --------------------------------------> Profile Password Changes 
@csrf_exempt
def cprofile_password(request):
    try:

        if 'email' in request.session:
        # Esmay Django Variable ki "Email" compare kari "Model Email" say.
            uid = User.objects.get(email = request.session['email'])
        # Esmay "Model User Class" ke "All Variable" liye compare kiya upper walay "uid" say.
            cid = Company.objects.get(user_id = uid)

            old_password = request.POST['oldpassword']
            new_password = request.POST['newpassword']
            re_password = request.POST['repeatpassword']

            if uid.password == old_password:
                if new_password == re_password:
                    uid.password = new_password
                    uid.save()
                # Python data Django may save karne
                # Dictionary
                    context ={
                        'uid':uid,
                        'cid':cid,
                        's_msg':'Succesfully update'
                    }
                    return render(request,"company/company-profile.html",context)
                else:
                    context ={
                            'uid':uid,
                            'cid':cid,
                            }
                    return render(request,"company/company-profile.html",context)
            else:
                context ={
                        'uid':uid,
                        'cid':cid,
                        'e_msg':'Invalid Password'
                        }
                return render(request,"company/company-profile.html",context)
        else:
            #return redirect('signin')
            return render(request,"company/company-profile.html")
    except Exception as e:
        print("------------>",e)
        return render(request,"company/sign-in.html")



# -------------------------------> Other Company Profile 
# Request k sath Primary Key display hugi.
# Company Increase hugi tu "Primary Key" Increase hugi.

def othercompanyprofile(request,pk):
    cid = Company.objects.get(id = pk)
    print("---->",pk)
    context = {
        'cid':cid,
        }
    return render(request,"company/company-profile.html",context)


# ----------------------> Company Details
@csrf_exempt
def companydetails(request):
    try:
        if 'email' in request.session:
        # Esmay Django Variable ki "Email" compare kari "Model Email" say.
            uid = User.objects.get(email = request.session['email'])
        # Esmay "Model User Class" ke "All Variable" liye compare kiya upper walay "uid" say.
            cid = Company.objects.get(user_id = uid)
            if request.POST:
                overview = request.POST['Overview']
                Establish = request.POST['Establish']
                temployee = request.POST['Temployee']

                cid.company_info = overview
                cid.company_established = Establish
                cid.company_employee = temployee
                cid.save()
                context = {
                    'uid':uid,
                    'cid':cid,
                }
                return redirect('companyprofile')
            else:
                return render(request,"company/company-profile.html")
        else:
        # "Redirect" use huta jab Response dena hu "Funtion" may.
            return render(request,"company/company-profile.html")
    except Exception as e:
        print("---------->",e)
        return render(request,"company/sign-in.html")
        
        
        
#----------------------> Start

# Companies Function hai per Jobpost use kliya.
# Similar Home
def jobpostcompanies(request):
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)
        calljob = jobpost.objects.filter(company_id = cid).order_by('-create_at')
        
        context={
            'uid':uid,
            'cid':cid,
            'calljob':calljob,
        }
        return render(request,"company/companies.html",context)
    elif 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Ruser.objects.get(user_id = uid)
        jall = jobpost.objects.all().order_by('-create_at')
        
        for job in jall:
        #                               post_title
            print("Job post_title",job.job_title)
        #                              Model ki jobpost_id = forloop ki jobki id say.
            all_likes = postlike.objects.filter(jobpost_id = job.id)
            print("------------>",all_likes)
            
            for item in all_likes:
            # Ye postlike model may "Likes" print karega.
                print("------->",item.likes)
       
        
        context={
            'uid':uid,
            'cid':cid,
            'jall':jall,
        }
        return render(request,"company/user-profile.html",context)
    else:
        return render(request,"company/user-profile.html")
        #return redirect('sigin')
    


#----------------------> End       
# Attribute error thi 
# "Modelname" "Same nahi" dene ka "View FunctionName say"      
def jobposts(request):
    try:

        if 'email' in request.session:
            uid = User.objects.get(email = request.session['email'])
            cid = Company.objects.get(user_id = uid)
            calljob = jobpost.objects.filter(company_id = cid)
            # Short way
            if request.POST:
                jid = jobpost.objects.create(
                                            company_id = cid,
                                            job_title = request.POST['job-title'],
                                            job_type =  request.POST['job-type'],
                                            job_description = request.POST['job-description'],
                                            job_salary = request.POST['job-salary'],
                                            job_requirement =  request.POST['job-requirement'],
                                            job_tags =  request.POST['job-tags'],
                                            )
                calljob = jobpost.objects.filter(company_id = cid)
                if jid:
                    context={
                            'uid':uid,
                            'cid':cid,
                            'jid':jid,
                            'calljob':calljob,

                        }
                    return render(request,'company/company-profile.html',context)
                    #return redirect(request,'jobpostcompanies',context)
                else:
                    context={
                            'uid':uid,
                            'cid':cid,
                            'jid':jid,
                            'calljob':calljob,

                        }
                    
                    return render(request,'company/company-profile.html',context)
            else:
                return render(request,'company/company-profile.html')
        else:
            return render(request,"company/sign-in.html")
    except Exception as e:
        print("----------->",e)
        return render(request,"company/sign-in.html")

            
def like_jobpost(request,pk):
    '''if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)
        # Company Self ka dekhe ga
        jall = jobpost.objects.filter(company_id = cid).order_by('-create_at')
        
        context={
            'uid':uid,
            'cid':cid,
            'jall':jall,
        }
        return render(request,"company/company-profile.html",context)'''
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Ruser.objects.get(user_id = uid)
        # User ku AllCompany ka dekhe ga
        jall = jobpost.objects.all().order_by('-create_at')
        
        jid = jobpost.objects.get(id = pk)# This way say pk dege direct nahi.
        print("-----> Postlike",pk)
        # Agar "jobpost_id ki Pk mili" tu like nahi tu no like
        like_job = postlike.objects.filter(jobpost_id = pk)
        
        if like_job:
        # All Post
            # Already Liked
            pall = postlike.objects.all()
            
        # All Ruser
            all_clients = []
            for i in pall:
                # all_clients may append kiya i k client_id ku.
                all_clients.append(i.client_id)
                

            # New user like kare tu like+1 hugi.
            if cid in all_clients:
                print("Already liked")
        else:
            like_id = postlike.objects.create(jobpost_id = jid,client_id = cid, likes=1)
                                                        # jid = pk hai.
            print("New like")
        
        # calljob    
        jall = jobpost.objects.all().order_by('-create_at')
        
        
        context={
            'uid':uid,
            'cid':cid,
            'jall':jall,
        }
        return redirect('userprofilep')
        #return render(request,"company/user-profile.html",context)
    

#------------> Postlike Page
def postlikes(request,pk):
     if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Company.objects.get(user_id = uid)
        jid = jobpost.objects.get(id=pk)
        calljob = jobpost.objects.filter(company_id = cid).order_by('-created_at')
        p_likes_by = postlike.objects.filter(jobpost_id = jid)
        context = {
                    'uid':uid,
                    'cid':cid,
                    'calljob':calljob,
                    'p_likes_by':p_likes_by,
                }
        return render(request,"company/post-like.html",context)
#------------> End





# ---------------------------------------------------------- User ----------------------------------------
#------------------------->
def userprofilepage(request): 
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        id = Ruser.objects.get(user_id = uid)
        #calljob = jobpost.objects.filter(company_id = cid)
        jall = jobpost.objects.all()
        jid = upost.objects.filter(ur_id = id)
        context ={
                'uid':uid,
                'id':id,
                'jall':jall,
                'jid':jid,
            }
        return render(request,"company/user-profile.html",context)
    # Elif condition hai User Profile jane ki Ya per. User folder walay may dena.
    else:
        return redirect('signin')                  
 

#-------------------------------------> User Registration/SignUp
def usignup(request):
    if request.POST:
        if request.POST['urole'] == 'user':
            uname = request.POST['username']

            uemail = request.POST['useremail']
            useraddress = request.POST['useraddress']
            usercontact = request.POST['usercontact']

            
            plist = ['ab123','cd456','ef789','gh1011','ij1213']
            password = random.choice(plist)
        # User Model email may save hai.
            uid = User.objects.create(email = uemail,
                                    password = password,
                                    role = request.POST['urole'])



            id = Ruser.objects.create(user_id = uid,
                                    user_name=uname,
                                    user_address = useraddress,
                                    user_contact = usercontact,
                                    )
            if id:
            #if request.POST:
                #email = request.POST['email']
                #password = request.POST['password']

                #uid = User.objects.get(email = email)
                #uid = User.objects.filter(email = email)
                
                #if uid:
                send_mail("Jobzilla","Check your email for otp and password"+password,"anjali.20.learn@gmail.com",['companyemail'])
                return render(request,"company/sign-in.html")
            else:
                return render(request,"company/sign-in.html")

    else:
        return render(request,"company/sign-in.html")


#---------------------------->End

#------------> User Logo
def user_logo(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        id = Ruser.objects.get(user_id = uid)
    
        if 'ulogo' in request.FILES:    
        
            userlogo = request.FILES['ulogo']

            # cid "Model" hai or company_logo "Model" wala
            # cid k company_logo may save huga companylogo
            # COCVV jesa per Update  karna hai esliye
            id.user_logo = userlogo
            id.save()
            #Update
        if 'user-coverp' in request.FILES:
                c_cover = request.FILES['user-coverp']
                id.user_cover = c_cover
                id.save()
        context ={
                    'uid':uid,
                    'id':id,
                }
        return render(request,"company/user-profile.html",context)
    else:
        return render(request,"company/user-profile.html")

#------------> End

#----------------------> User Profile Account Setting
def upasetting(request):                   
    if 'email' in request.session:
        uid = User.objects.get(email = request.session['email'])
        id = Ruser.objects.get(user_id = uid)
        context={
            'uid':uid,
            'id':id,
        }
        return render(request,"company/Useraccount.html",context)
    else:
        return render(request,"company/Useraccount.html")


#----------------------> End




#----------------> ProfilePage Password Change
def profile_password(request):
    try:
        if 'email' in request.session:
        # Esmay Django Variable ki "Email" compare kari "Model Email" say.
            id = User.objects.get(email = request.session['email'])
        # Esmay "Model User Class" ke "All Variable" liye compare kiya upper walay "uid" say.
            cid = Ruser.objects.get(user_id = id)

            uold_password = request.POST['uold-password']
            unew_password = request.POST['unew-password']
            ure_password = request.POST['urepeat-password']

            if id.password == uold_password:
                if unew_password == ure_password:
                # Python ka data Django may dene use ki context
                    id.password = unew_password
                    id.save()   
                    context ={
                        'id':id,
                        'cid':cid,
                        's_msg':'Succesfully update'
                    }
                    return render(request,"company/Useraccount.html",context)
                else:
                    context ={
                            'uid':id,
                            'cid':cid,
                            }
                    return render(request,"company/user-profile.html",context)
            else:
                context ={
                        'uid':id,
                        'cid':cid,
                        'e_msg':'Invalid Password'
                        }
                return render(request,"company/user-profile.html",context)
        else:
            return render(request,"company/user-profile.html")
    except Exception as e:
        print("------------>",e)
        return render(request,"company/user-profile.html")

#----------------> End

# --------------------> User Profile pay header per home
def userprofile(request):
    try:
        if "email" in request.session:
            uid = User.objects.get(email = request.session['email'])
            id = Ruser.objects.get(user_id = uid)
            jall = jobpost.objects.all()
            jid = upost.objects.all()
            context ={
                    'uid':uid,
                    'id':id,
                    'jall':jall,
                    'jid':jid,
                }
            return render(request,"company/user-profile.html",context)
        else:
            return redirect('signin')
    except Exception as e:
        print("------->",e)
        return render(request,"company/sign-in.html")
# --------------------> End

# ---------------------> User see all companies
def allcompanies(request):
    if 'email' in request.session:
        # User ko all "Company" dekni chahiye
        uid = User.objects.get(email = request.session['email'])
        id = Ruser.objects.get(user_id = uid)
        call = Company.objects.all()
        context={
                    'uid':uid,
                    'id':id,
                    'call':call,
                }
        return render(request,"company/companies.html",context)
# ---------------------> End

# ----------------------> User Resume
def uposts(request):
    try:
        
        if 'email' in request.session:
            uid = User.objects.get(email = request.session['email'])
            id = Ruser.objects.get(user_id = uid)
            userd = upost.objects.filter(ur_id = id)
            # Short way
            if request.POST:
                jid = upost.objects.create(
                                            ur_id = id,
                                            u_overview = request.POST['overview'],
                                            u_role =  request.POST['roles'],
                                            u_language = request.POST['language'],
                                            u_education = request.POST['education'],
                                            u_location =  request.POST['location'],
                                            )
                userd = upost.objects.filter(ur_id = id)
                if jid:
                    context={
                            'uid':uid,
                            'id':id,
                            'jid':jid,
                            'userd':userd,

                        }
                    return redirect('userprofilep')
                    #return redirect(request,'jobpostcompanies',context)
                else:
                    return render(request,'company/user-profile.html')
            else:
                return render(request,'company/user-profile.html')
    except Exception as e:
        print("--------->",e)
        return render(request,"company/user-profile.html")


# ----------------------> End








    



