import os
import logging

import pandas as pd
import networkx as nx

from datashader.bundling import hammer_bundle
from datashader.layout import forceatlas2_layout

logger = logging.getLogger('cf-graph-viz')

def on_server_loaded(server_context):
    # Load the raw NX GRAPH, compute ForceLayout node position, and Hammer_bundle the edges
    r_graph_file = os.getenv('CF_GRAPH')
    logger.info('Loading CF_GRAPH={}'.format(r_graph_file))

    r_graph = nx.read_yaml(r_graph_file)
    pd_nodes = pd.DataFrame([(node, node) for node in r_graph.nodes], columns=['id', 'node'])
    pd_nodes.set_index('id', inplace=True)
    pd_edges = pd.DataFrame(list(r_graph.edges), columns=['source', 'target'])

    logger.info('Laying out {} nodes'.format(len(pd_nodes)))
    pd_nodes_layout = forceatlas2_layout(pd_nodes, pd_edges)
    pd_nodes_layout.to_pickle('nodes.pkl')

    logger.info('Bundling {} edges'.format(len(pd_edges)))
    h_bundle = hammer_bundle(pd_nodes_layout, pd_edges)
    h_bundle.to_pickle('edges-bundled.pkl')

    return

def on_server_unloaded(server_context):
    print('Server stopped')

def on_session_created(server_context):
    print('New session')

def on_server_destroyed(server_context):
    print('Session destroyed')
