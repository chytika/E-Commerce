from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

USer = settings.AUTH_USER_MODEL

# Create your views here.


def Register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"hey {username}, your account is created successfully")
            new_user = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password1"])
            login(request, new_user)
            return  redirect("core:index")


    else:
      form = UserRegisterForm()

      context ={
            'form': form,
        }

    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f"User is already logged in")
        # return  redirect("core:index")

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = user.objects.all(email=email)
        except:
            messages.warning(request,f"User with this {email} doesnot exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,'you r logged in')
            return  redirect("core:index")
        else:
            messages.warning(request,"user is not exist. Create and account")

    # context ={
         
    #  }

    return render(request, "userauths/sign-in.html")



def logout_view(request):
    logout(request)
    messages.success(request, "u r logged out")
    return redirect("userauths:sign-in")