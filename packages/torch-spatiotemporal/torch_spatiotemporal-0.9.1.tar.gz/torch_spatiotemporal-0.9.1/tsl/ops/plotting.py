import numpy as np
from pandas import DataFrame

# from ..imports import _PLOTLY_AVAILABLE
_PLOTLY_AVAILABLE = True

if _PLOTLY_AVAILABLE:
    import plotly.graph_objects as go
    import plotly.io as pio

    pio.renderers.default = "browser"
else:
    go = None


def _make_edges_component(df, edge_index, name):
    x = df.iloc[edge_index.T.ravel()].loc[:, name].values.reshape(-1, 2)
    x = np.concatenate([x, np.full((x.shape[0], 1), None)], 1).reshape(-1)
    return x


def plot_adj(node_latlon: DataFrame, edge_index: np.ndarray,
             title: str = None,
             mapbox_kwargs: dict = None,
             filename: str = None,
             **kwargs):
    if not _PLOTLY_AVAILABLE:
        raise RuntimeError("Install optional dependency 'plotly' to use this "
                           "function.")
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        name='Edges',
        lat=_make_edges_component(node_latlon, edge_index, 'lat'),
        lon=_make_edges_component(node_latlon, edge_index, 'lon'),
        line=dict(width=0.8, color='#888'),
        hoverinfo='none',
        mode='lines',
        opacity=0.4,
    ))
    # plot nodes
    fig.add_trace(go.Scattermapbox(
        name='Nodes',
        lat=node_latlon.loc[:, 'lat'],
        lon=node_latlon.loc[:, 'lon'],
        text=node_latlon.index.astype(str),
        mode='markers',
        marker=go.scattermapbox.Marker(size=7)
    ))

    # update mapbox settings
    mean_lat, mean_lon = node_latlon[['lat', 'lon']].mean()
    mapbox_kwargs_default = {
        'center': dict(lat=mean_lat, lon=mean_lon)
    }
    if mapbox_kwargs is not None:
        mapbox_kwargs_default.update(mapbox_kwargs)
    else:
        mapbox_kwargs = mapbox_kwargs_default

    if 'accesstoken' not in mapbox_kwargs:
        mapbox_kwargs['style'] = 'open-street-map'

    fig.update_layout(mapbox=mapbox_kwargs)

    # update layout
    layout_kwargs = dict(autosize=True,
                         hovermode='closest')
    layout_kwargs.update(title_text=title, **kwargs)
    fig.update_layout(mapbox=mapbox_kwargs)

    if filename is not None:
        fig.write_html(filename)
    fig.show()
