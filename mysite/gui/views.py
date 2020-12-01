import importlib.util

from django.shortcuts import render
from pathlib import Path
"""
This files is a generated file from Django that we use
to recieve feedback from the GUI
Currently this is not being used
__author__: Gatlin Cruz
__author__: Cade Tipton
__version__: 9/15/20
"""

BASE_DIR = Path(__file__).resolve().parent.parent

###### For Windows
"""This is the path we use when running on a windows machine"""
# spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "\\gui\\templates\\gui\\buttons.py")

###### For Mac
"""This is the path we use when running on a mac/linux machine"""
spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "/gui/templates/gui/buttons.py")

buttons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(buttons)

"""This graph info is linked to the HTML doc for our GUI. The values are stored in this list"""
graph_info = {
        'num_hosts': 0,
        'num_switches': 0,
        'num_controllers': 0,
        'links': []
        }

"""This is the extra text used to display the ping results from Mininet"""
extra_text = {
    'ping': ""
}

"""This is how Django conects the lists to the HTML"""
context = {
        'graph': graph_info,
        'output': extra_text
    }


def home(request):
    """
    This is the main method for our GUI. It checks if any of the buttons have been pressed
    and does the appropriate method call. It also sets the parameters for the graph when the 
    user hits the set button
    return: The GUI html to display to the user
    """
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

        buttons.make_file(graph_info)

    elif request.GET.get('graphbtn'):
        buttons.make_graph(graph_info['num_hosts'], graph_info['num_switches'],
                           graph_info['num_controllers'], graph_info['links'])
        return render(request, 'gui/figure.html', context)

    elif request.GET.get('resetbtn'):
        buttons.reset_graph(graph_info)

    elif request.GET.get('pingbtn'):
        buttons.run_mininet(extra_text)

    return render(request, 'gui/gui.html', context)


def graph(request):
        """
        This method creates the graph HTML and displays to the user
        return: The rendered HTML of the graph
        """
    return render(request, 'gui/figure.html')
