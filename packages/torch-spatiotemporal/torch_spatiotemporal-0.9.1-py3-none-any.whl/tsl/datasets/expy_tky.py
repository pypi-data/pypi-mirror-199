import os
from typing import Union

import numpy as np
import pandas as pd

from .prototypes import DatetimeDataset
from ..ops.similarities import gaussian_kernel
from ..utils import download_url, extract_zip, precision_stoi


class ExpyTky(DatetimeDataset):
    r"""Traffic speed readings from 2841 expressway road links in Tokyo
    collected every 10 minutes for three months (Oct to Dec 2021).

    Introduced in the paper `"Spatio-Temporal Meta-Graph Learning for Traffic
    Forecasting" <https://arxiv.org/abs/2211.14701>`_ (Jiang et al., AAAI 2023),
    where only a subset of 1843 sensors is considered. To use this subset, set
    the argument :arg:`use_subset` to :obj:`True`.

    Dataset information:
        + Time steps: 13248
        + Nodes: 2841
        + Channels: 1
        + Sampling rate: 10 minutes
        + Missing values: 0.00%

    Static attributes:
        + :obj:`metadata`: storing for each node:
            + ``start_lat``: latitude of the road segment's starting point;
            + ``start_lon``: longitude of the road segment's starting point;
            + ``mask``: if ``True``, then the node is in the subset of 1843
                sensors considered in the paper.
        + :obj:`dist`: :math:`N \times N` matrix of node pairwise distances.
        + :obj:`adj`: binary adjacency matrix :math:`\mathbf{A} \in
          \{0,1\}^{N \times N}`
    """
    url = ""

    similarity_options = {'distance', 'binary'}

    def __init__(self,
                 root: str = None,
                 use_subset: bool = False,
                 freq: str = None,
                 precision: Union[int, str] = 32):
        # set root path
        self.root = root
        self.use_subset = use_subset
        # load dataset
        readings, metadata = self.load(use_subset=use_subset)
        covariates = {'metadata': (metadata, ['n f'])}
        super().__init__(target=readings, freq=freq,
                         covariates=covariates,
                         similarity_score="binary",
                         temporal_aggregation="mean",
                         name="ExpyTky",
                         precision=precision)

    @property
    def raw_file_names(self):
        return ['data.h5', 'adj.npz']

    @property
    def required_file_names(self):
        return self.raw_file_names

    def download(self) -> None:
        path = download_url(self.url, self.root_dir)
        extract_zip(path, self.root_dir)
        os.unlink(path)

    def build(self) -> None:
        self.maybe_download()
        # Remove raw data
        # self.clean_downloads()

    def load_raw(self):
        self.maybe_build()
        # load traffic data
        data_path = os.path.join(self.root_dir, 'data.h5')
        readings = pd.read_hdf(data_path, key='readings')
        metadata = pd.read_hdf(data_path, key='metadata')
        return readings, metadata

    def load(self, use_subset: bool = False):
        readings, metadata = self.load_raw()
        if use_subset:
            node_mask = metadata[['mask']].values
            readings = readings.loc[:, node_mask]
            metadata = metadata.loc[node_mask]
        return readings, metadata

    def compute_similarity(self, method: str, **kwargs):
        # load archive containing connectivity information
        adj_path = os.path.join(self.root_dir, 'adj.npz')
        adj_archive = np.load(adj_path)
        # possibly mask nodes
        if self.use_subset:
            node_mask = self.metadata[['mask']].values
        else:
            node_mask = None
        # convert to dataset's precision
        precision = f'float_{precision_stoi(self.precision)}'

        if method == "binary":
            # load binary adjacency matrix
            adj = adj_archive['binary']
            if node_mask is not None:
                adj = adj[node_mask][:, node_mask]
            return adj.astype(precision)
        if method == "distance":
            # load distance matrix
            dist = adj_archive['distance']
            if node_mask is not None:
                dist = dist[node_mask][:, node_mask]
            return gaussian_kernel(dist).astype(precision)
