from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Headline, Source, Category, Follow, User

def index(request):
    template = 'codex/home.html'
    message = 'Welcome: Home Page!'
    context = {'message': message}
    return render(request, template, context)

@login_required(login_url='login')
def sidebar(request):
    template = 'codex/layout.html'
    message = 'Welcome: Home Page!'
    sources = Follow.objects.get(user=request.user)
    context = {'sources': sources, 'message': message}
    return render(request, template, context)

@login_required(login_url='login')
def def_headline(request):
    template = 'codex/headline.html'
    sources = Follow.objects.get(user=request.user)
    sed = sources.source.first()
    headlines = Headline.objects.filter(source=sources.source.first())[:30]
    context = {'sources': sources, 'sed': sed,'headlines': headlines}
    return render(request, template, context)

@login_required(login_url='login')
def headline(request, id):
    template = 'codex/headline.html'
    sources = Follow.objects.get(user=request.user)
    sed = sources.source.get(pk=id)
    headlines = Headline.objects.filter(source=sed)[:30]
    context = {'sources': sources, 'sed': sed, 'headlines': headlines}
    return render(request, template, context)

@login_required(login_url='login')
def delete(request, id):
    selected = Follow.objects.get(user=request.user)
    source = Source.objects.get(pk=id)
    selected.source.remove(source)
    return redirect('def_headline')

@login_required(login_url='login')
def sources(request):
    sources = Follow.objects.get(user=request.user)
    sourced = Source.objects.all()
    template = 'codex/sources.html'
    context = {'sources': sources, 'sourced': sourced}
    return render(request, template, context)

@login_required(login_url='login')
def follow(request, id):
    source = Source.objects.get(pk=id)
    follow, created = Follow.objects.get_or_create(user=request.user)
    follow.source.add(source)
    return redirect('sources')
    
    



















def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("def_headline"))
        else:
            return render(request, "codex/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "codex/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "codex/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("sources"))
    else:
        return render(request, "codex/register.html")