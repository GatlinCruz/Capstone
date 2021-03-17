import importlib.util

from django.shortcuts import render
from pathlib import Path
from . import nodes
import csv
# from lxml import html
# import requests
# from bs4 import BeautifulSoup

"""
This files is a generated file from Django that we use
to receive feedback from the GUI
__author__: Gatlin Cruz
__author__: Cade Tipton
__version__: 9/15/20
"""

BASE_DIR = Path(__file__).resolve().parent.parent

# For Windows
"""This is the path we use when running on a windows machine"""
# spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "\\gui\\templates\\gui\\buttons.py")

# For Mac
"""This is the path we use when running on a mac/linux machine"""
spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "/gui/templates/gui/buttons.py")

buttons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(buttons)

"""This graph info is linked to the HTML doc for our GUI. The values are stored in this dict"""
graph_info = {
    'num_hosts': 0,
    'num_switches': 0,
    'num_controllers': 0,
    'links': []
}

"""This graph nodes is linked to the HTML doc for our GUI. The values are stored in this dict"""
graph_nodes = {
    'hosts': [],
    'switches': [],
    'controllers': [],
    'links': []
}

"""This is the extra text used to display the ping results from Mininet"""
extra_text = {
    'ping': ""
}

"""This is how Django connects the lists to the HTML"""
context = {
    'graph': graph_nodes,
    'output': extra_text,
}


def home(request):
    """
    This is the main method for our GUI. It checks if any of the buttons have been pressed
    and does the appropriate method call. It also sets the parameters for the graph when the 
    user hits the set button
    return: The GUI html to display to the user
    """
    # This is the logic for when the set button is clicked
    if request.GET.get('setbtn'):
        print(graph_nodes)
        buttons.make_file(graph_nodes)

    # This is the logic for when the add host button is clicked
    elif request.GET.get('add_host_btn'):
        name = request.GET.get('add_host_name')
        ip = request.GET.get('add_host_ip')
        host = nodes.Host(name, ip)
        graph_nodes['hosts'].append(host)

    # This is the logic for when the add switch button is clicked
    elif request.GET.get('add_switch_btn'):
        name = request.GET.get('add_switch_name')
        switch = nodes.Switch(name)
        graph_nodes['switches'].append(switch)

    # This is the logic for when the add controller button is clicked
    elif request.GET.get('add_controller_btn'):
        name = request.GET.get('add_controller_name')
        controller = nodes.Controller(name)
        graph_nodes['controllers'].append(controller)

    # This is the logic for when the add link button is clicked
    elif request.GET.get('add_link_btn'):
        first = request.GET.get('add_first_link')
        second = request.GET.get('add_second_link')
        link = nodes.Link(first, second)
        graph_nodes['links'].append(link)

    # This is the logic for when the graph button is clicked
    elif request.GET.get('graphbtn'):
        buttons.make_graph(graph_nodes)
        return render(request, 'gui/figure.html', context)

    # This is the logic for when the reset button is clicked
    elif request.GET.get('resetbtn'):
        buttons.reset_graph(graph_nodes)

    # This is the logic for when the ping button is clicked
    elif request.GET.get('pingbtn'):
        buttons.run_mininet(extra_text)

    # This is the logic for when the add_data button is clicked
    elif request.GET.get('add_databtn'):
        filename = request.GET.get('save_file_name')
        buttons.add_to_database(graph_nodes, filename)

    # This is the logic for when the load_data button is clicked
    elif request.GET.get('load_databtn'):
        file = request.GET.get('load_databtn')
        path = str(Path.home()) + "/Desktop/" + file
        host_list = []
        switch_list = []
        controller_list = []
        links_list = []
        full_list = []
        with open(path, newline='') as csv_file:
            csv_r = csv.DictReader(csv_file)
            for row in csv_r:
                full_list.append(row)
                if row['type'] == 'host':
                    host_list.append(row)
                elif row['type'] == 'switch':
                    switch_list.append(row)
                elif row['type'] == 'controller':
                    controller_list.append(row)
                else:
                    links_list.append(row)
        for item in host_list:
            graph_nodes['hosts'].append(nodes.Host(item.get('name'), item.get('ip')))
        print("\n")
        for item in switch_list:
            graph_nodes['switches'].append(nodes.Switch(item.get('name')))
        print("\n")
        for item in controller_list:
            graph_nodes['controllers'].append(nodes.Controller(item.get('name')))
        # Gets the start and end id and finds them in 'full_list to create a link
        f, s = "", ""
        for item in links_list:
            first_id = item['_start']
            second_id = item['_end']
            for row in full_list:
                if row.get('_id') == first_id:
                    f = row.get('name')
                    break
            for row in full_list:
                if row.get('_id') == second_id:
                    s = row.get('name')
                    break
            graph_nodes['links'].append(nodes.Link(f, s))


    return render(request, 'gui/gui.html', context)


def graph(request):
    """
    This method creates the graph HTML and displays to the user
    return: The rendered HTML of the graph
    """
    return render(request, 'gui/figure.html')
