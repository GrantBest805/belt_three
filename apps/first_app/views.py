from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import User, Appointment
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.db.models import Count
from django.core.urlresolvers import reverse


def index(request):
    return render(request, 'first_app/index.html')

def show(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect(reverse('index'))
    time = datetime.now()
    other = Appointment.objects.all().exclude(date=datetime.now())
    context = {
        'other': other,
        'time': datetime.now(),
        'appointments': Appointment.objects.filter(date=datetime.now())
    }
    return render(request, 'first_app/show.html', context)

def new_task(request):
    if request.method == 'POST':
        data = {
            'date': request.POST['date'],
            'time': request.POST['time'],
            'task': request.POST['task'],
            'user': request.session['user_id'],
        }
        the_appoint = Appointment.objects.appoint(data)
        if the_appoint['list_errors'] != None:
            for error in the_appoint['list_errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect(reverse('show'))
        else:
            return redirect(reverse('show'))
def update_page(request, id=None):
    app_edit = Appointment.objects.get(id=id)
    context ={
        'app_edit': app_edit,
    }

    return render(request, "first_app/edit.html", context)




#REGISTER FUNCTION
def register(request):
    if request.method == 'POST':
        context = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'confirm': request.POST['confirm']
        }

        req_results = User.objects.reg(context)
        if req_results['new'] != None:
            request.session['user_id'] = req_results['new'].id
            request.session['user_first_name'] = req_results['new'].first_name
            return redirect(reverse('show'))
        else:
            print req_results['error_list']
            for error_str in req_results['error_list']:
                messages.add_message(request, messages.ERROR, error_str)

            return redirect(reverse('index'))
#LOGIN FUNCTION
def login(request):
    if request.method == 'POST':
        p_data = {
            'email': request.POST['email'],
            'password': request.POST['password']
        }

        log_results = User.objects.login(p_data)
        if log_results['list_errors'] != None:
            for error in log_results['list_errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect(reverse('index'))
        else:
            request.session['user_id'] = log_results['log_user'].id
            request.session['user_first_name'] = log_results['log_user'].first_name
            return redirect(reverse('show'))

#LOG OUT FUNCTION
def logout(request):
    request.session.clear()
    return redirect(reverse('index'))

def delete(request, id=None):
   a = Appointment.objects.get(id=id).delete()
   return redirect(reverse('show'))

def edit(request, id=None):
    if request.method == 'POST':
        a = Appointment.objects.get(id=id)

        new = Appointment.objects.create(task=request.POST['task'], status=request.POST['status'], date=request.POST['date'], time=request.POST['time'])

        return redirect(reverse('show', kwargs={'id': id}))







