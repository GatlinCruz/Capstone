import plotly.graph_objects as go
import networkx as nx
import numpy as np
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
PATH = os.path.join(BASE_DIR, "gui/")

np.random.seed(1)


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

    fig.write_html(PATH + 'figure.html')

    # pio.write_html(fig, file=PATH + 'figure.html', auto_open=False)


def reset_graph(graph):
    graph['num_hosts'] = 0
    graph['num_switches'] = 0
    graph['num_controllers'] = 0
    graph['links'] = []
