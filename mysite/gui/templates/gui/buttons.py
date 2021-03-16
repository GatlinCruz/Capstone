import plotly.graph_objects as go
import networkx as nx
import numpy as np
from pathlib import Path
import os
import time
import subprocess
import importlib.util

"""
This file handles the logic when a button is pressed on our GUI
__author__ Cade Tipton
__author__ Gatlin Cruz
__version__ 9/15/20
"""
BASE_DIR = Path(__file__).resolve().parent.parent
PATH = os.path.join(BASE_DIR, "gui/")

###### For Windows
"""This is the path we use when running on a windows machine"""
# spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "\\gui\\templates\\gui\\buttons.py")

###### For Mac
"""This is the path we use when running on a mac/linux machine"""
spec = importlib.util.spec_from_file_location("db_testing", str(BASE_DIR) + "/db_testing.py")

db_testing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_testing)

np.random.seed(1)
filename = ''


def make_graph(hosts, switches, controllers, links):
    """
    This setups up the graph based on the parameters from the user and makes an HTML file of the graph
    args:
     hosts: The number of hosts in the graph
     switches: The number of switches in the graph
     controllers: The number of controllers in the graph
     links: The links in the graph
    """
    # The graph object used to build the network throughout the function
    G = nx.Graph()

    G.add_edges_from(links)

    # Adds a node for each number of host, switch and controller
    for switch in range(0, switches):
        s_name = "s" + str(switch + 1)
        G.add_node(s_name, type='Switch', color='green', name=s_name)
        print("Added switch " + "s" + str(switch + 1))
    for controller in range(0, controllers):
        c_name = "c" + str(controller + 1)
        G.add_node(c_name, type='Controller', color='blue', name=c_name)
        print("Added controller " + "c" + str(controller + 1))
    for host in range(0, hosts):
        h_name = "h" + str(host + 1)
        G.add_node(h_name, type='Host', color='black', name=h_name)
        print("Added host " + "h" + str(host + 1))

    node_x = []
    node_y = []
    start_x = 1
    host_y = 1
    last_switch_x = -1
    switch_y = 5
    cont_y = 8
    for node in G.nodes():
        # x = np.random.uniform(low=1, high=5)
        # y = np.random.uniform(low=1, high=5)

        if G.nodes[node]['type'] == 'Switch':
            y = switch_y
            start_x += 1
            x = start_x
            last_switch_x = x

        elif G.nodes[node]['type'] == 'Controller':
            y = cont_y
            x = last_switch_x
            last_switch_x += 3
        else:
            start_x += 1
            y = host_y
            x = start_x

        G.nodes[node]['pos'] = x, y
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='none',
        marker=dict(
            size=50,
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
        line=dict(width=5, color='black'),
        hoverinfo='none',
        mode='lines')

    node_text = []
    node_color = []
    for node in G.nodes():
        node_text.append(G.nodes[node]['name'])  # type
        node_color.append(G.nodes[node]['color'])
    node_trace.marker.color = node_color
    node_trace.text = node_text
    node_trace.textfont = dict(
        family="monospace",
        size=32,
        color="white"
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,  # hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # if os.path.exists(PATH + 'figure.html'):
    #    fig.write_html(PATH + ('figure_{}.html'.format(int(time.time()))))
    # else:
    fig.write_html(PATH + 'figure.html')


def reset_graph(graph):
    """
    Resets the values of the graph to 0
    args:
      graph: The graph list being used
    """
    graph['num_hosts'] = 0
    graph['num_switches'] = 0
    graph['num_controllers'] = 0
    graph['links'] = []


def make_file(graph):
    """
    Creates a Python file that represents a network using Mininet
    args:
       graph: The graph list with the values for the network
    """
    #other_path = "/home/mininet/Desktop/"
    other_path = "/home/gatlin/Desktop/"
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
        if str(graph.get('links')[link][0][0]) != "c" and str(graph.get('links')[link][1][0]) != "c":
            link_text += "l" + str(link + 1) + " = net.addLink( '" + str(graph.get('links')[link][0]) \
                         + "', '" + str(graph.get('links')[link][1]) + "' )\n"

    print(host_text)
    print(switch_text)
    print(controller_text)
    print(link_text)

    # Writing the formatted text to the file
    new_file.write("#Add hosts\n" + host_text + "\n")
    new_file.write("#Add switches\n" + switch_text + "\n")
    new_file.write("#Add controllers\n" + controller_text + "\n")
    new_file.write("#Add links\n" + link_text + "\n")

    new_file.write("\nnet.start()\n")
    new_file.write("net.pingAll()\n")
    new_file.write("net.stop()\n")


def run_mininet(extra):
    """
    Method to run Mininet in the background so the user can run commands through it
    args:
       extra: The holder for the results to be stored to
    """
    path = "/home/gatlin/Desktop/"
    #sudo_pw = "mininet"
    sudo_pw = "Davis123!"
    #path = "/home/mininet/Desktop/"

    command = "python2 " + path + "new_file.py"
    command = command.split()

    cmd1 = subprocess.Popen(['echo', sudo_pw], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    outs, errors = cmd2.communicate()
    print("outs" + outs + "\nerrors: " + errors + "end")

    errors = errors.replace("[sudo] password for mininet: ", "")

    extra['ping'] = errors


def add_to_database(hosts, switches, controllers, links, graph_name):
    bolt_url = "neo4j://localhost:7687"  # %%BOLT_URL_PLACEHOLDER%%
    # The default username for Neo4j
    user = "neo4j"
    # The password we use to gain access to the database
    password = "mininet"
    # Creating an app object from the db_testing file
    app = db_testing.App(bolt_url, user, password)
    for i in range(hosts):
        app.create_node("h" + str(i + 1), graph_name)
    for i in range(switches):
        app.create_node("s" + str(i + 1), graph_name)
    for i in range(controllers):
        app.create_node("c" + str(i + 1), graph_name)

    for item in links:
        app.create_links_db(item[0], item[1], graph_name)

    app.create_csv(graph_name)

    app.close()


def main():
    """
    The main method that creates a path
    """
    # custom_path = "/home/mininet/mininet/custom/"

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
