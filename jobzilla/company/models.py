from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone
from django.db.models import Max
import math

# Create your models here.
# Inheritance
class User(models.Model):
    email = models.EmailField(unique= True,max_length=20)
    password = models.CharField(max_length=10)
    role = models.CharField(max_length=10)
    otp = models.IntegerField(default=459)
    #Account Active hai ya nahi
    is_active = models.BooleanField(default=True)
    # First Login per verify
    is_verify = models.BooleanField(default=False)
    # Account create ka Time
    create_at = DateTimeField(auto_now_add=True,blank=False)
    # Account update ka Time
    update_at = DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.email


# Models create kiya Model name ka.
class Company(models.Model):
    # User Class ka Sare Variable aayege 
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=20)
    company_address = models.CharField(max_length=20)
    company_contact = models.IntegerField(max_length=10)
    company_city = models.CharField(max_length=20)
    company_type = models.CharField(max_length=20)

    # Company may New field apply ki.
    # Cmd may default error aati hai ki.
    # Already company register hue hai osmay ya field ka kay karna hai.
    company_established = models.CharField(max_length=100,default="")
    company_info = models.TextField(null=True,blank=True)
    company_employee = models.IntegerField(default=0)

    company_logo = models.FileField(upload_to='media/images',default='media/default.jpg')
    company_cover = models.FileField(upload_to='media/images',default='media/defaults.jpg')

# Use kiya Superuser may data may "company_name" 123 nahi.
    def __str__(self):
        return self.company_name

# ------------------> User
class Ruser(models.Model):
    # "Foreignkey" important hai Comman Value rakhne.
    # "ForeignKey" 1position per rakhne ka always.
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

    user_name = models.CharField(max_length=20)
 
    user_address = models.CharField(max_length=10)
    user_contact = models.CharField(max_length=20)

    user_logo = models.FileField(upload_to='media/images',default='media/ulogo.jpg')
    user_cover = models.FileField(upload_to='media/images',default='media/ucover.jpg')
    
    
    def __str__(self):
       return self.user_name

class upost(models.Model):
    ur_id = models.ForeignKey(Ruser,on_delete=models.CASCADE)
    u_overview = models.TextField()
    u_role = models.CharField(max_length= 10)
    u_language = models.CharField(max_length=10)
    u_education = models.CharField(max_length=10)
    u_location = models.CharField(max_length=10)
    create_at = DateTimeField(auto_now_add=True,blank=False)
    # Account update ka Time
    update_at = DateTimeField(auto_now=True,blank=False)

    # Self Kjage kuch or bhi enter kar sakte hai.
    def __str__(self):
        return self.u_overview




# Class hai Job upload,like,comment kliya 
class jobpost(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=20)
    job_type = models.CharField(max_length= 10)
    job_description = models.TextField()
    job_salary = models.IntegerField(max_length=10)
    job_requirement = models.IntegerField()
    job_tags = models.CharField(max_length=50)
    create_at = DateTimeField(auto_now_add=True,blank=False)
    # Account update ka Time
    update_at = DateTimeField(auto_now=True,blank=False)

    # Self Kjage kuch or bhi enter kar sakte hai.
    def __str__(self):
        return self.job_title
        
# Function hai  

    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.create_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:  
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
    def mylikes(self):
        try:
            my_post_likes = postlike.objects.filter(jobpost_id = self.id).order_by('-likes')
        # Ye my_post_likes ki 0position means Jobpostki 0position
        # Or sath may "Likes"
            print("----------> mypost like",my_post_likes[0].likes)
            
            totallikes = my_post_likes[0].likes
            return totallikes
        except:
            return 0
            
    def mytags(self):
    # JobPost k tags "Split" kiye
        myall_tags = self.job_tags.split(",")
        print("---------->",myall_tags)
        return myall_tags
            
 
        




class postlike(models.Model):
    # k Smallletter may tha
    jobpost_id = models.ForeignKey(jobpost, on_delete=models.CASCADE)
    client_id = models.ForeignKey(Ruser,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    
    # Account create ka Time
    create_at = DateTimeField(auto_now_add=True,blank=False)
    # Account update ka Time
    update_at = DateTimeField(auto_now=True,blank=False)
    
    def __str__(self):
    # Print karegi "Jobpost.Job Title" "String" "Ruser.Username"
        return self.jobpost_id.job_title + "liked by"+ self.client_id.user_name






