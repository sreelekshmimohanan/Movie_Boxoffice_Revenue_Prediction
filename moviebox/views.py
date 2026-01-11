from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect,get_object_or_404 
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings
from .models import *
from django.contrib import messages
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer

def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')


def reg(request):
    return render(request,'register.html')


def addreg(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('passsword')
        ins=register(name=name,email=email,phone=phone,password=password)
        ins.save()
    return render(request,'register.html',{'message':"Successfully Registerd"})    

def login(request):
     return render(request,'login.html')
    

def addlogin(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    if email=='admin@gmail.com' and password =='admin':
        request.session['logint']=email
        return render(request,'index.html')
    elif register.objects.filter(email=email,password=password).exists():
        user=register.objects.get(email=email,password=password)
        request.session['uid']=user.id
        return render(request,'index.html')
    else:
        return render(request,'login.html')
    



def logout(request):
    session_keys=list(request.session.keys())
    for key in session_keys:
          del request.session[key]
    return redirect(first)

def view_revenue_prediction(request):
    if request.session.get('logint'):
        # Admin view all
        predictions = Prediction.objects.all().select_related('user').order_by('-created_at')
    elif request.session.get('uid'):
        # User view own
        user = register.objects.get(id=request.session['uid'])
        predictions = Prediction.objects.filter(user=user).order_by('-created_at')
    else:
        return redirect('login')
    
    return render(request, 'view_revenue_prediction.html', {'predictions': predictions})

def viewuser(request):
    data=register.objects.all()
    return render(request,'viewuser.html',{'data':data})

def movie_revenue_prediction(request):
    if request.method == 'POST':
        # Get form data
        features = {
            'release_year': int(request.POST.get('release_year')),
            'release_day': int(request.POST.get('release_day')),
            'release_month': int(request.POST.get('release_month')),
            'status': request.POST.get('status'),
            'original_language': request.POST.get('original_language'),
            'budget': float(request.POST.get('budget')),
            'popularity': float(request.POST.get('popularity')),
            'genres_count': int(request.POST.get('genres_count')),
            'production_companies': request.POST.get('production_companies'),
            'production_countries': request.POST.get('production_countries'),
            'spoken_languages_count': int(request.POST.get('spoken_languages_count')),
            'cast_count': int(request.POST.get('cast_count')),
            'crew_count': int(request.POST.get('crew_count')),
            'runtime': float(request.POST.get('runtime'))
        }
        
        # Import and use the prediction function
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ML'))
        from inference import predict_revenue_processed
        
        prediction = predict_revenue_processed(features)
        
        # Save to database
        user = register.objects.get(id=request.session['uid'])
        pred_obj = Prediction.objects.create(
            user=user,
            predicted_revenue=prediction,
            **features
        )
        
        return render(request, 'movie_revenue_prediction.html', {
            'prediction': f"${prediction:,.2f}",
            **features
        })
    return render(request, 'movie_revenue_prediction.html')