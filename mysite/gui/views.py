from django.shortcuts import render
import plotly.graph_objects as go
import networkx as nx

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
    if request.GET.get('graphbtn'):
        hosts = int(request.GET.get('host'))
        switches = int(request.GET.get('switch'))
        controllers = int(request.GET.get('controller'))
        link = request.GET.get('link').replace(" ", "").split(';')
        links = []
        for pair in link:
            links.append(tuple(map(str, pair.split(','))))
        make_graph(hosts, switches, controllers, links)

    elif request.GET.get('resetbtn'):
        reset_graph()

    return render(request, 'gui/gui.html', context)


def make_graph(hosts, switches, controllers, links):
    graph_info['num_hosts'] = hosts
    graph_info['num_switches'] = switches
    graph_info['num_controllers'] = controllers
    graph_info['links'] = links

    G = nx.Graph()

    for host in range(hosts):
        G.add_node("h" + str(host))
    for switch in range(switches):
        G.add_node("s" + str(switch))
    for controller in range(controllers):
        G.add_node("c" + str(controller))

    G.add_edges_from(links)

    # TODO: Make Plotly graph from networkx graph


def reset_graph():
    graph_info['num_hosts'] = 0
    graph_info['num_switches'] = 0
    graph_info['num_controllers'] = 0
    graph_info['links'] = []
