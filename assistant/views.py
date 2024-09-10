from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventRegisterForm, EventFilterForm, EventForm

def index(request):

    params = {

        'title' : 'Assistant/Index',
        'msg' : 'This page is under construction.Please, check me later.'
    }

    return render(request, 'assistant/index.html', params)

@login_required(login_url="/admin/login/")
def open(request):

    data = Event.objects.all()
    params = {

        'title' : 'Assistant/open',
        'msg' : 'festival info',
        'data' : data,
    }

    return render(request, 'assistant/open.html', params)


#@staff_member_required(login_url="admin/login/")
@login_required(login_url="/admin/login/")
def registerEvent(request):

    params = {

        'title' : 'Assistant/EventRegister',
        'message' : 'Fill in bellow blanks to register events',
        'form' : EventRegisterForm(),
        'search_form' : EventFilterForm(),
    }
    if(request.method == "POST"):
        
        obj = Event()
        event = EventForm(request.POST, instance=obj)
        event.save()

        params['message'] = 'Registration completed successfully<br>' + request.POST['name'] + '( ' + request.POST['location'] + ' : ' + request.POST['date'] + ')' + request.POST['summary']

        #return redirect(to="open/")
    
    return render(request, 'assistant/eventRegister.html', params)


@login_required(login_url="/admin/login/")
def editEvent(request, id):

    obj = Event.objects.get(id=id)
    if(request.method == 'POST'):
        event = EventForm(request.POST, instance=obj)
        event.save()
        return redirect(to="/assistant/open/")

    params = {

        'title' : 'assistant/eventEdit',
        'id' : id,
        'form' : EventForm(instance=obj),
    }

    return render(request, 'assistant/eventEdit.html', params)

@login_required(login_url="/admin/login/")
def deleteEvent(request, id):

    event = Event.objects.get(id=id)
    if(request.method == 'POST'):
        event.delete()
        return redirect(to="/assistant/open/")
    
    params = {

        'title' : 'assistant/eventDelete',
        'id' : id,
        'obj' : event,
    }

    return render(request, 'assistant/eventDelete.html', params)