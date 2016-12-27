# coding = utf-8

from .forms import *
from .models import *
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db import transaction

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html' , {})

# @csrf_protect
@transaction.atomic
def loginpage(request):
    if request.user.is_authenticated():
    	return HttpResponseRedirect('../home')
    elif request.method == 'POST':
        username = request.POST.get('username')
       	password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect('../home')
        else:
            return render(request, 'login.html', {})
    return render(request, 'login.html', {})

@csrf_protect
@transaction.atomic
def registerpage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            Touruser.objects.create(user = user,
            utag=form.cleaned_data['utag'], usign=form.cleaned_data['usign'],
            )
            print user.date_joined
            return HttpResponseRedirect('../home/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })

    return render_to_response(
    'register.html',
    variables,
    )

@login_required(login_url='../login/')
def logoutfunction(request):
    auth.logout(request)
    return HttpResponseRedirect('../login/')

@login_required(login_url='../login/')
def searchresult(request):
    return render(request, '' , {})


@login_required(login_url='../login/')
def community(request):
    return render(request, '' , {})

@login_required(login_url='../login/')
def triplist(request):
    return render(request, '' , {})

@login_required(login_url='../login/')
def editjournal(request):
    return render(request, 'main-yet.html' , {})

@login_required(login_url='../login/')
def addjournal(request):
    # getinfo = Tourjournal.objects.all()

    # getuser = Touruser.objects.all()
    # print(getuser[0].uid)

    if request.is_ajax():
        if request.method == 'POST':
            print ('come to ajax...')
            print (request.user.id)
            #  print ("come into ajax! " + request.body)
            # newrecord = Tourjournal.objects.create(jname='Test', jcontent=request.body, juser_id=request.user.id)

            # we use this way to solve the problem of foreign key instead of Tourjournal.objects.create()
            d1 = Touruser.objects.get(user=request.user.id)
            u1 = Tourjournal(jname='Test', jcontent=request.body, juser=d1)
            # save in database
            u1.save()

    return HttpResponseRedirect('../personal')
    # return HttpResponse("OK")

@login_required(login_url='../login/')
def personal(request):
    return render(request, 'user.html', {})

@login_required(login_url='../login/')
def profile(request):
    return render(request, '', {})

@login_required(login_url='../login/')
def editprofile(request):
    return render(request, '', {})
