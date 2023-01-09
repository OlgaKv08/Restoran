from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from .forms import Image
from .models import LoadMultipleImages
from .db import *

# Create your views here.

def index(request):
    city = 'All'
    return render(request, 'main\index.html', {'restorans': restorans, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})

def login(request):
    if request.method == 'POST':
        luser = request.POST

        for _user in users:
            if _user['login'] == luser['login'] and _user['password'] == luser['password']:
                global isLogin, isAdmin, user
                isLogin = True
                isAdmin = bool(_user['isAdmin'])
                user = _user
                
                return render(request, 'main\index.html', {'restorans': restorans, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})
        return render(request, 'main/login.html', {'isFailed': True, 'cityes': cityes})
    else: return render(request, 'main/login.html', {'cityes': cityes})

def reg(request):
    if request.method == 'POST':
        ruser = request.POST
        form = Image(ruser, request.FILES)

        if form.is_valid():
            form.save()
            img_obj = form.instance

            global users, user, isLogin, isAdmin

            for _user in users:
                if _user['login'] == ruser['login']:
                    return render(request, 'main/reg.html', {'form': Image, 'cityes': cityes})

            users.append({
                'login': ruser['login'],
                'password': ruser['password'],
                'isAdmin': False,
                'img': img_obj.image.url
            })

            isLogin = True
            isAdmin = False
            user = users[len(users) - 1]
            

            return render(request, 'main\index.html', {'restorans': restorans,  'cityes': cityes, 'city': city,  'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})
    else: return render(request, 'main/reg.html', {'form': Image, 'cityes': cityes})

def Exit(request):
    global isAdmin, isLogin, user
    isAdmin = False
    isLogin = False
    user = None

    
    return render(request, 'main\index.html', {'restorans': restorans, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})

def Sort(request):
    global city
    city = request.POST['city']
    
    return render(request, 'main\index.html', {'restorans': restorans, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})
    
def Search(request):
    resul = []

    for item in restorans:
        if str(item['city']).lower() == request.POST['Search'].lower() or str(item['city']).lower().__contains__(request.POST['Search'].lower()) or str(item['name']).lower() == request.POST['Search'].lower() or str(item['name']).lower().__contains__(request.POST['Search'].lower()):
            if city != None and item['city'] == city:
                resul.append(item)
            else:
                resul.append(item)

    if len(resul) > 0:
        return render(request, 'main\index.html', {'restorans': resul, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})
    else:
        if city == None:
            return render(request, "main\Error.html", {'error': "По запросу '" + request.POST['Search'] + "' ничего не найдено!"})
        else:
            return render(request, "main\Error.html", {'error': "В категории '" + city + "' по запросу '" + request.POST['Search'] + "' ничего не найдено!"})

def Remove(request):
    name = request.POST['name']
    city = request.POST['city']

    _list = []

    for item in restorans:
        if item['name'] != name:
            _list.append(item)

    restorans.clear()
    for item in _list:
        restorans.append(item)

    CheckCityes()
    return render(request, 'main\index.html', {'restorans': restorans, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})

def About(request):
    if request.method == 'POST':
        pass
    else:
        restoran = GetRestoranByName(request.GET['name'])
        haveUserComment = False

        if user:
            for comment in restoran['comments']:
                if comment['user']['login'] == user['login']:
                    haveUserComment = True

        return render(request, 'main/about.html', {'user': user, 'isLogin': isLogin, 'haveUserComment': haveUserComment, 'cityes': cityes, 'restoran': restoran})

def Comment(request):
    if request.method == 'POST':
        for rest in restorans:
            if rest['name'] == request.POST['name']:
                rest['comments'].append({
                    'user': user,
                    'comment': request.POST['comment'],
                    'raiting': request.POST['raiting'],
                })
    
    restoran = GetRestoranByName(request.POST['name'])
    haveUserComment = False

    for comment in restoran['comments']:
        if comment['user']['login'] == user['login']:
            haveUserComment = True
    haveUserComment = False

    CheckRaiting()
    return render(request, 'main/about.html', {'user': user, 'isLogin': isLogin, 'haveUserComment': haveUserComment, 'cityes': cityes, 'restoran': restoran})


def Create(request):
    if request.method == 'POST':
        rest = request.POST

        if GetRestoranByName(rest['name']): 
            return render(request, 'main\index.html', {'restorans': restorans, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})

        form = Image(rest, request.FILES)

        if form.is_valid():
            form.save()
            img_obj = form.instance

            restorans.append({
                'name': rest['name'],
                'city': rest['city'],
                'img': img_obj.image.url,
                'about': rest['about'],
                'mapUrl': rest['mapUrl'],
                'comments': []
            })

        CheckCityes()
        return render(request, 'main\index.html', {'restorans': restorans, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})
    else:
        return render(request, 'main\create.html', {'cityes': cityes, 'form': Image, 'isLogin': isLogin, 'user': user})

def Change(request):
    if request.method == 'POST':
        rest = request.POST

        for restoran in restorans:
            if restoran['name'] == rest['oldName']:

                restoran['name'] = rest['name']
                restoran['city'] = rest['city']
                restoran['img'] = rest['img']
                restoran['about'] = rest['about']
                restoran['mapUrl'] = rest['mapUrl']

                break

        CheckCityes()
        return render(request, 'main\index.html', {'restorans': restorans, 'cityes': cityes, 'city': city, 'isAdmin': isAdmin, 'isLogin': isLogin, 'user': user})
    else:
        for restoran in restorans:
            if restoran['name'] == request.GET['name']:
                return render(request, 'main\change.html', {'cityes': cityes, 'restoran': restoran, 'user': user, 'isLogin': isLogin})