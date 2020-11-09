import importlib.util

from django.shortcuts import render
from pathlib import Path
from django.template import Context, loader
import webview

BASE_DIR = Path(__file__).resolve().parent.parent

###### For Windows
# spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "\\gui\\templates\\gui\\buttons.py")

###### For Mac
spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "/gui/templates/gui/buttons.py")

buttons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(buttons)


page = open("/Users/gatlincruz/PycharmProjects/Capstone/mysite/gui/templates/gui/figure.html", "r").read()


num_links = {
        'num_hosts': 0,
        'num_switches': 0,
        'num_controllers': 0,
        'links': []
        }

graph_info = {
        'num_hosts': 0,
        'num_switches': 0,
        'num_controllers': 0,
        'links': []
        }

context = {
        'graph': graph_info,
        'first_name': page,
        'num_hosts': num_links['num_hosts'],
        'num_switches': num_links['num_switches'],
        'num_controllers': num_links['num_controllers']
    }

def home(request):
    if request.GET.get('setbtn'):
        hosts = int(request.GET.get('host'))
        switches = int(request.GET.get('switch'))
        controllers = int(request.GET.get('controller'))
        link = request.GET.get('link').replace(" ", "").split(';')
        links = []
        for pair in link:
            links.append(tuple(map(str, pair.split(','))))

        graph_info['num_hosts'] = hosts
        graph_info['num_switches'] = switches
        graph_info['num_controllers'] = controllers
        graph_info['links'] = links

    elif request.GET.get('graphbtn'):
        #buttons.make_graph(graph_info['num_hosts'], graph_info['num_switches'],
        #                   graph_info['num_controllers'], graph_info['links'])
        #return render(request, 'gui/figure.html', context)
        buttons.make_graph(num_links['num_hosts'], num_links['num_switches'],
                            num_links['num_controllers'], num_links['links'])

        #webview.create_window('Capstone 1', 'gui/figure.html', resizable=True, background_color='#000')
        #webview.start(http_server=True)
        reload()

        return render(request, 'gui/figure.html', context)

    elif request.GET.get('resetbtn'):
        buttons.reset_graph(graph_info)

    elif request.GET.get('runbtn'):
        buttons.make_file(graph_info)

    elif request.POST.get('applybtn'):

        numHosts = request.POST.get('num_hosts')
        numSwitches = request.POST.get('num_switches')
        numControllers = request.POST.get('num_controllers')
        num_links['num_hosts'] = numHosts
        num_links['num_switches'] = numSwitches
        num_links['num_controllers'] = numControllers


    elif request.POST.get('addbtn'):

        link1 = request.POST.get('link1')
        link2 = request.POST.get('link2')
        num_links['links'].append((link1, link2))

    elif request.POST.get('printbtn'):
        print(num_links['num_hosts'])
        print(num_links['num_switches'])
        print(num_links['num_controllers'])
        print(num_links['links'])

    return render(request, 'gui/base1.html', context)


def graph(request):
    return render(request, 'gui/figure.html')

def reload():
    page = open("/Users/gatlincruz/PycharmProjects/Capstone/mysite/gui/templates/gui/figure.html", "r").read()


