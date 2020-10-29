import importlib.util

from django.shortcuts import render
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

###### For Windows
# spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "\\gui\\templates\\gui\\buttons.py")

###### For Mac
spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "/gui/templates/gui/buttons.py")

buttons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(buttons)

graph_info = {
        'num_hosts': 0,
        'num_switches': 0,
        'num_controllers': 0,
        'links': []
        }

context = {
        'graph': graph_info
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
        buttons.make_graph(graph_info['num_hosts'], graph_info['num_switches'],
                           graph_info['num_controllers'], graph_info['links'])
        return render(request, 'gui/figure.html', context)

    elif request.GET.get('resetbtn'):
        buttons.reset_graph(graph_info)

    elif request.GET.get('runbtn'):
        buttons.make_file(graph_info)

    return render(request, 'gui/base.html', context)


def graph(request):
    return render(request, 'gui/figure.html')
