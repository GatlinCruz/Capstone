import plotly.graph_objects as go
import networkx as nx
import numpy as np
from pathlib import Path
import os
import time
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent
PATH = os.path.join(BASE_DIR, "gui/")

np.random.seed(1)
filename = ''


def make_graph(hosts, switches, controllers, links):
    G = nx.Graph()

    G.add_edges_from(links)

    for host in range(0, hosts):
        G.add_node("h" + str(host + 1), type='Host', color='black')
        print("Added host " + "h" + str(host + 1))
    for switch in range(0, switches):
        G.add_node("s" + str(switch + 1), type='Switch', color='green')
        print("Added switch " + "s" + str(switch + 1))
    for controller in range(0, controllers):
        G.add_node("c" + str(controller + 1), type='Controller', color='blue')
        print("Added controller " + "c" + str(controller + 1))

    node_x = []
    node_y = []
    for node in G.nodes():
        x = np.random.uniform(low=1, high=20)
        y = np.random.uniform(low=1, high=20)
        G.nodes[node]['pos'] = x, y
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=40,
            color=[]))

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='black'),
        hoverinfo='none',
        mode='lines')

    node_text = []
    node_color = []
    for node in G.nodes():
        node_text.append(" " + G.nodes[node]['type'] + " ")
        node_color.append(G.nodes[node]['color'])
    node_trace.marker.color = node_color
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # if os.path.exists(PATH + 'figure.html'):
    #    fig.write_html(PATH + ('figure_{}.html'.format(int(time.time()))))
    # else:
    fig.write_html(PATH + 'figure.html')

    # pio.write_html(fig, file=PATH + 'figure.html', auto_open=False)


def reset_graph(graph):
    graph['num_hosts'] = 0
    graph['num_switches'] = 0
    graph['num_controllers'] = 0
    graph['links'] = []


def make_file(graph):
    other_path = "/home/mininet/Desktop/"
    new_file = open(other_path + "new_file.py", "w+")
    new_file.write("from mininet.net import Mininet\n")
    new_file.write("from mininet.cli import CLI\n")
    new_file.write("net = Mininet()\n")

    host_text = ""
    switch_text = ""
    controller_text = ""
    link_text = ""

    for host in range(graph.get('num_hosts')):
        host_text += "h" + str(host + 1) + " = net.addHost( 'h" + str(host + 1) + "' )\n"
    for switch in range(graph.get('num_switches')):
        switch_text += "s" + str(switch + 1) + " = net.addSwitch( 's" + str(switch + 1) + "' )\n"
    for controller in range(graph.get('num_controllers')):
        controller_text += "c" + str(controller + 1) + " = net.addController( 'c" + str(controller + 1) + "' )\n"
    for link in range(len(graph.get('links'))):
        link_text += "l" + str(link + 1) + " = net.addLink( '" + str(graph.get('links')[link][0]) \
                     + "', '" + str(graph.get('links')[link][1]) + "' )\n"

    print(host_text)
    print(switch_text)
    print(controller_text)
    print(link_text)

    new_file.write("#Add hosts\n" + host_text + "\n")
    new_file.write("#Add switches\n" + switch_text + "\n")
    new_file.write("#Add controllers\n" + controller_text + "\n")
    new_file.write("#Add links\n" + link_text + "\n")

    new_file.write("\nnet.start()\n")
    new_file.write("net.pingAll()\n")
    new_file.write("net.stop()\n")


def run_mininet(extra):
    sudo_pw = "mininet"
    path = "/home/mininet/Desktop/"
    # command = "gnome-terminal -- mn --custom " + path + "base_file.py --topo mytopo"
    # command = "gnome-terminal -- python2 " + path + "new_file.py"
    # command = "python2 " + path + "new_file.py"
    # p = os.popen('echo %s|sudo -S %s' % (sudo_pw, command))
    # print(p.read())

    command = "python2 " + path + "new_file.py"
    command = command.split()

    cmd1 = subprocess.Popen(['echo', sudo_pw], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    outs, errors = cmd2.communicate()
    print("outs" + outs + "\nerrors: " + errors + "end")

    errors = errors.replace("[sudo] password for mininet: ", "")

    extra['ping'] = errors


def main():
    custom_path = "/home/mininet/mininet/custom/"

    # base_file = open(custom_path + "base_file.py", "a")
    #
    # host_text = ""
    # switch_text = ""
    # for host in range(4):  # graph.get('num_hosts')
    #     host_text += "\th" + str(host + 1) + " = self.addHost( 'h" + str(host + 1) + "' )\n"
    # for switch in range(2):  # graph.get('num_switches')
    #     switch_text += "\ts" + str(switch + 1) + " = self.addSwitch( 's" + str(switch + 1) + "' )\n"
    #
    # print(host_text)
    # print(switch_text)
    #
    # base_file.write("\t#Add hosts\n" + host_text + "\n")
    # base_file.write("\t#Add switches\n" + switch_text)
    # other_path = "/home/mininet/Desktop/"
    # make_file()

    # run_mininet(other_path)


if __name__ == '__main__':
    main()
