from django.shortcuts import render
from django.http import HttpResponse

graph_info = [
    {
        'num_hosts': 5,
        'num_clients': 1,
        'num_controllers': 2
    },
    {
        'num_hosts': 3,
        'num_clients': 4,
        'num_controllers': 1
    }

]

def home(request):
    context = {
        'graphs': graph_info
    }
    return render(request, 'gui/gui.html', context)

    # response = HttpResponse()
    # response.write('./gui.html')
    # return response



# Create your views here.
