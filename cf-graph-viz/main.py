import os
import pandas as pd
import holoviews as hv
import networkx as nx

from colorcet import fire

from holoviews.operation.datashader import datashade
from holoviews.operation import decimate

from bokeh.plotting import curdoc
from bokeh.layouts import layout

from dask.distributed import Client
client = Client()

renderer = hv.renderer('bokeh').instance(mode='server')

decimate.max_samples=20000
datashade.cmap=fire[40:]
sz = dict(width=1024,height=1024)

# stackoverflow https://stackoverflow.com/questions/12329853/how-to-rearrange-pandas-column-sequence
# reorder columns
def set_column_sequence(dataframe, seq, front=True):
    '''Takes a dataframe and a subsequence of its columns,
       returns dataframe with seq as first columns if "front" is True,
       and seq as last columns if "front" is False.
    '''
    cols = seq[:] # copy so we don't mutate seq
    for x in dataframe.columns:
        if x not in cols:
            if front: #we want "seq" to be in the front
                #so append current column to the end of the list
                cols.append(x)
            else:
                #we want "seq" to be last, so insert this
                #column in the front of the new column list
                #"cols" we are building:
                cols.insert(0, x)
    return dataframe[cols]

pd_nodes = pd.read_pickle('nodes.pkl')
pd_edges = pd.read_pickle('edges-bundled.pkl')

r_nodes = hv.Points(set_column_sequence(pd_nodes, ['x', 'y']) , label='Nodes')
r_edges = hv.Curve(pd_edges, label='Bundled')

hv_layout=datashade(r_edges, **sz) * \
          decimate(hv.Points(r_nodes),max_samples=1000)
# Opts
hv.opts('RGB [xaxis=None yaxis=None show_grid=False bgcolor="black" width={width} height={height}]'.format(**sz))
hv.opts('Points [tools=["hover"]] (color="cyan", size=3)')

hv_plot=renderer.get_plot(hv_layout, curdoc())

bk_layout = layout([
    [hv_plot.state]], sizing_mode='fixed')

curdoc().add_root(bk_layout)
