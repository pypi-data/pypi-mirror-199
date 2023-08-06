from typing import Optional

from torch import Tensor

from tsl.nn.base.recurrent import GraphGRUCell, RNNBase
from tsl.nn.layers.graph_convs.dense_graph_conv import DenseGraphConvOrderK


class DenseDCRNNCell(GraphGRUCell):
    r"""The Diffusion Convolutional Recurrent cell from the paper
    `"Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic
    Forecasting" <https://arxiv.org/abs/1707.01926>`_ (Li et al., ICLR 2018).

    In this implementation, the adjacency matrix is dense and the convolution is
    performed with matrix multiplication.

    Args:
         input_size: Size of the input.
         hidden_size: Number of units in the hidden state.
         k: Size of the diffusion kernel.
         root_weight (bool): Whether to learn a separate transformation for the
            central node.
    """

    def __init__(self, input_size: int, hidden_size: int,
                 k: int = 2, root_weight: bool = False):
        # instantiate gates
        forget_gate = DenseGraphConvOrderK(input_size + hidden_size,
                                           hidden_size,
                                           support_len=2,
                                           order=k,
                                           include_self=root_weight,
                                           channel_last=True)
        update_gate = DenseGraphConvOrderK(input_size + hidden_size,
                                           hidden_size,
                                           support_len=2,
                                           order=k,
                                           include_self=root_weight,
                                           channel_last=True)
        candidate_gate = DenseGraphConvOrderK(input_size + hidden_size,
                                              hidden_size,
                                              support_len=2,
                                              order=k,
                                              include_self=root_weight,
                                              channel_last=True)

        super(DenseDCRNNCell, self).__init__(hidden_size=hidden_size,
                                             forget_gate=forget_gate,
                                             update_gate=update_gate,
                                             candidate_gate=candidate_gate)


class DenseDCRNN(RNNBase):
    """The Diffusion Convolutional Recurrent Neural Network from the paper
    `"Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic
    Forecasting" <https://arxiv.org/abs/1707.01926>`_ (Li et al., ICLR 2018).

    In this implementation, the adjacency matrix is dense and the convolution is
    performed with matrix multiplication.

    Args:
        input_size: Size of the input.
        hidden_size: Number of units in the hidden state.
        n_layers: Number of layers.
        k: Size of the diffusion kernel.
        root_weight: Whether to learn a separate transformation for the central
            node.
    """
    _n_states = 1

    def __init__(self, input_size: int, hidden_size: int,
                 n_layers: int = 1, cat_states_layers: bool = False,
                 return_only_last_state: bool = False,
                 k: int = 2, root_weight: bool = False):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.k = k
        rnn_cells = [
            DenseDCRNNCell(input_size if i == 0 else hidden_size, hidden_size,
                           k=k, root_weight=root_weight)
            for i in range(n_layers)
        ]
        super(DenseDCRNN, self).__init__(rnn_cells, cat_states_layers,
                                         return_only_last_state)

    def forward(self, x: Tensor, adj,
                h: Optional[Tensor] = None, **kwargs):
        support = DenseGraphConvOrderK.compute_support(adj)
        return super(DenseDCRNN, self).forward(x, h=h, support=support)
