from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register_page(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'registration/register.html', context)
