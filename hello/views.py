import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView

# Create your views here.


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


def about(request):
    return render(request, 'hello/about.html')


def contact(request):
    return render(request, 'hello/contact.html')


def hello_there(request, name):
    # Filter the name arguement to letters only using regular expressions. URL arguements
    # can contain arbitrary text, so we restrict to safe characters only
    match_object = re.match('[a-zA-Z]+', name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = 'Friend'

    return render(request, 'hello/hello_there.html', {
        'name': clean_name,
        'date': datetime.now()
    })


def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect('home')
    else:
        return render(request, 'hello/log_message.html', {'form': form})