import json
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('chatbot')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')

# def welcome_message(request):
#     return HttpResponse(
#         "Welcome to the Chatbot! Please <a href='/chatbot/'>navigate to /chatbot/</a> to start chatting."
#     )
# Load the intents file
with open('intents.json', 'r') as file:
    intents = json.load(file)['intents']

# Prepare dataset
patterns = []
tags = []
responses = {}

for intent in intents:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])
    responses[intent['tag']] = intent['responses']

# Vectorize and train the model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)
y = np.array(tags)

model = make_pipeline(TfidfVectorizer(), LinearSVC())
model.fit(patterns, y)
# @login_required(login_url='login')
def chatbot_response(text):
    tag = model.predict([text])[0]
    return random.choice(responses[tag])

@login_required(login_url='login')
@csrf_exempt  # This is for demonstration purposes. In production, handle CSRF properly.
def chatbot(request):
    if request.method == "POST":
        user_input = json.loads(request.body).get('message')
        response = chatbot_response(user_input)
        return JsonResponse({"response": response})

    return render(request, "chatbot.html")


