#python manage.py runserver

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import All_Reviews, Negative_Reviews
import os
from pathlib import Path
#from transformers import AutoTokenizer, AutoModelForSequenceClassification
#import torch
from .send_mail import send_mail_func
import requests
from dotenv import load_dotenv


load_dotenv()
BERT_INFERENCE_API = os.getenv("BERT_INFERENCE_API")


BASE_DIR = Path(__file__).resolve().parent.parent

API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
headers = {"Authorization": f"Bearer {BERT_INFERENCE_API}"}

#==================================================================================

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

#==================================================================================

def home(request):
    return render(request, "home.html")

#==================================================================================

def client_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:  # Check if username and password are provided
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                # Login the authenticated user
                login(request, user)
            
                request.session['user_id'] = user.id
                request.session['user_username'] = user.username
            
                # Redirect to a success page after successful login
                return redirect('product_view')
            else:
                error_message = '*Invalid Username or Password!'
        else:
            error_message = ''
    else:
        error_message = ''  # No error message to display on initial load

    return render(request, "client_login.html", {'error_message': error_message})


#==================================================================================

def client_signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')

        # Check if the email is already registered
        if User.objects.filter(username=email).exists():
            return render(request, 'client_signup.html', {'error_message': '*Email already exists'})

        # Check if the password and confirm password match
        if password != confirm_password:
            return render(request, 'client_signup.html', {'error_message': '*Passwords do not match'})

        # Encrypt the password
        encrypted_password = make_password(password)
        
        # Create the user with email as the username
        user = User(username=email, email=email, first_name=full_name, password=encrypted_password)
        user.save()

        # Log in the user
        login(request, user)

        messages.success(request, 'Signup Successful! Login to continue.')
        return redirect('client_login_view')

    return render(request, "client_signup.html")

#==================================================================================

@login_required
def product_view(request):
    if request.method == "POST":
        
        username = request.session['user_username']
        if username:
            user = User.objects.get(username=username)
            
        fullname = user.first_name
        username = user.username
        product = request.POST.get('product_name')
        review = request.POST.get('review')
        
        #-----------------------------------------------------------------------------------------
        
        # tokenizer = AutoTokenizer.from_pretrained(os.path.join(BASE_DIR,"myapp/sentiment_analysis_tokenizer"))

        # bert_model = AutoModelForSequenceClassification.from_pretrained(os.path.join(BASE_DIR,"myapp/sentiment_analysis_bert_model"))
        
        # review_token = tokenizer.encode(review, return_tensors='pt')
        # rating = bert_model(review_token)
        # rating = int(torch.argmax(rating.logits))+1
        
        #-----------------------------------------------------------------------------------------
        
        output = query({
            "inputs": review,
        })

        rating = int(output[0][0]['label'][0])
        
        label = ""
        if rating == 3:
            label = "NEUTRAL"
        elif rating < 3:
            label = "NEGATIVE"
        else:
            label = "POSITIVE"
           
        #--------------------All Reviews Table--------------- 
        all_reviews = All_Reviews(username=username, fullname=fullname, product=product, review=review, rating=rating, label=label)
        all_reviews.save()
        #----------------------------------------------------
        
        #--------------------Negative Reviews Table--------------------
        if rating <= 3:
            negative_reviews = Negative_Reviews(username=username, fullname=fullname, product=product, review=review, rating=rating, label=label)
            negative_reviews.save()
        #--------------------------------------------------------------
        
        send_mail_func(fullname, username, product, label)
        
        return render(request, "product.html", {'success_message': 'Thanks for your review. Our team will get back to you soon through E-mail!'})       
    
    return render(request, "product.html")

#==================================================================================
