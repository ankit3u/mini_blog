
from django.shortcuts import HttpResponse, redirect, render,HttpResponseRedirect
from .forms import SignupForm,LoginForm,PostForm,blogform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post,Blog
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})


def about(request):
    return render(request,'blog/about.html')

@login_required(login_url="login")
def contact(request):
    return render(request,'blog/contact.html')

@login_required(login_url="login")
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        # user=request.user()
        # full_name=user.get_full_name()
        # gps=user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/login/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations ! You have become an Author')
            user=form.save()
            # group=Group.objects.get(name='Author')
            # user.groups.add(group)
    else:
        form=SignupForm()
    return render(request,'blog/signup.html',{'form':form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Loged in succcessfully !")
                    return HttpResponseRedirect('/')
        else:
            form=LoginForm()
        return render(request,'blog/login.html',{'form':form})

    else:
        return HttpResponseRedirect('/dashboard/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=PostForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form=PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

@login_required(login_url="login")
def addblog(request):
    if request.method == 'GET':
        form = blogform()
        return render(request,'blog/addblog.html',{'form':form})

    else:
        form = blogform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('addblog')
        else:
            messages.info(request,"Error")
            return redirect('addblog')

@login_required(login_url="login")
def blogs(request):
        image=Blog.objects.all()
        return render(request,'blog/show.html',{'image':image})
   
    