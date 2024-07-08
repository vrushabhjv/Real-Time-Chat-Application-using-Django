from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm


# Create your views here.
def frontpage(request):
    return render(request, 'core/frontpage.html')

def signUp(request):
    if request.method=="POST":
        form=SignUpForm(request.POST) #This populates the form instance with the submitted data, binding it to the form's fields.
        
        if form.is_valid():
            user=form.save()
            
            login(request, user)
            
            return redirect('frontpage') 
    else:
        form=SignUpForm()
        
    return render(request, 'core/signup.html', {'form':form} )
