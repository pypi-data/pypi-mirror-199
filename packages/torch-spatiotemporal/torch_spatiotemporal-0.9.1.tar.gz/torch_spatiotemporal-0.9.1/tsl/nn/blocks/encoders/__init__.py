from .conditional import ConditionalBlock, ConditionalTCNBlock
from .dcrnn import DCRNNCell, DCRNN
from .dense_dcrnn import DenseDCRNNCell, DenseDCRNN
from .gcgru import GraphConvGRUCell, GraphConvGRU
from .gclstm import GraphConvLSTMCell, GraphConvLSTM
from .mlp import MLP, ResidualMLP, MultiMLP
from .rnn import RNN, MultiRNN
from .stcn import SpatioTemporalConvNet
from .tcn import TemporalConvNet
from .transformer import (TransformerLayer,
                          SpatioTemporalTransformerLayer,
                          Transformer)

from .evolvegcn import EvolveGCNOCell, EvolveGCNHCell, EvolveGCN
from .agcrn import AGCRNCell, AGCRN

general_classes = [
    'ConditionalBlock',
    'ConditionalTCNBlock',
    'MLP',
    'ResidualMLP',
    'MultiMLP',
    'RNN',
    'MultiRNN'
]

cell_classes = [
    'DCRNNCell',
    'DenseDCRNNCell',
    'GraphConvGRUCell',
    'GraphConvLSTMCell',
    'AGCRNCell',
    'EvolveGCNOCell',
    'EvolveGCNHCell'
]

grnn_classes = [
    'DCRNN',
    'DenseDCRNN',
    'GraphConvGRU',
    'GraphConvLSTM',
    'EvolveGCN',
    'AGCRN'
]

conv_classes = [
    'TemporalConvNet',
    'SpatioTemporalConvNet'
]

transformer_classes = [
    'TransformerLayer',
    'SpatioTemporalTransformerLayer',
    'Transformer'
]

classes = [
    *general_classes,
    *cell_classes,
    *grnn_classes,
    *conv_classes,
    *transformer_classes
]

__all__ = classes
