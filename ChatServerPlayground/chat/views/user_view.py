from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# first creating the login view
def loginPage(request):
    # first checking user is authenticated
    if request.user.is_authenticated:
        # if user logged in then redirect the user to the homepage
        return redirect("home")
    error_message = ""
    email_or_pass = ""
    # checking the method
    if request.method == "POST":
        # get the user name and password from the user
        email_or_pass = request.POST.get("email_or_username")
        pass1 = request.POST.get('pass')
        try:
            curr_user = User.objects.get(
                Q(email=email_or_pass) | Q(username=email_or_pass)
            )
        except User.DoesNotExist:
            error_message = 'user does not exist check your email or username'
            return render(
                request,
                'login.html',
                {
                    'error_message' : error_message,
                    'email' : email_or_pass
                }
            )
        # next step will be authenticate the user
        user = authenticate(request,username=curr_user.username,password=pass1)
        # next check the user is not empty
        if user is not None:
            # then login the user
            login(request,user)
            # after that redirect the user to the home page
            return redirect("home")
        else:
            # else user is empty
            if User.objects.filter(username=curr_user.username).exists():
                # if the user exist probably the password is incorrect
                error_message = 'incorrect password for the user'
            else:
                # probably user  does not exist
                error_message = 'user does not exist'
        
    return render(request,
                  'login.html',
                  {
                      'error_message':error_message,
                      'email' : email_or_pass
                  })
    
# sign up view for the user
def signup(request):
    # check for authentication
    if request.user.is_authenticated:
        # redirect the user to the home
        return redirect("home")
    # initial error message
    error_message = ""
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        
        data = {
            'username' : uname,
            'useremail' : email
        }
        
        # check for the user is already exist on the db
        if User.objects.filter(username=uname).exists():
            # user exist
            error_message = 'username already taken'
            return render(request,
                          'signup.html',
                          {
                              'error_message' : error_message,
                              'userdata' : data
                          })
        
        # check the email already in use
        elif User.objects.filter(email=email).exists():
            error_message = f'mail of {email} in use'
            return render(request,
                          'signup.html',
                          {
                              'error_message': error_message,
                              'userdata' : data
                          })
            
        # checking the password for conformation
        elif pass1!=pass2:
            error_message = 'password does not match'
            return render(request,
                          'signup.html',
                          {
                              'error_message': error_message,
                              'userdata': data
                          })
        else:
            # now after check everything have to signup the new user
            user = User.objects.create_user(username=uname,
                                            email=email,
                                            password=pass1)
            # saving the  instance of the user
            user.save()
            # after sign up use must login
            login(request, user)
            return redirect("home")
        
    return render(
        request,
        'signup.html',
        {
            'error_message' : error_message
        }
    )
    
    
# user edit activity of the profile
@login_required(login_url='login')
def editProfile(request):
    success_message = ""
    error_message = ""
    if request.method == "POST":
        new_email = request.POST.get('email')
        new_username = request.POST.get('username')
        
        # check for the new user name  equal to the previous username or the new user name already exists
        if(new_username == request.user.username and User.objects.filter(username=new_username).exists):
            error_message = 'username already exists'
        # check for the new email equal to the previous email or the new email already exists
        elif(new_email == request.user.email and User.objects.filter(email=new_email).exists()):
            error_message = 'email already on use , please use a different a different one!'
        else:
            # update the username and password
            request.user.username = new_username
            request.user.email = new_email
            request.user.save()
            success_message = "profile updated successfully"
            
    return render(
        request,
        'edit.html',
        {
            
        }
    )


# logout view for the user
@login_required
def logout(request):
    logout(request)
    return redirect('login')