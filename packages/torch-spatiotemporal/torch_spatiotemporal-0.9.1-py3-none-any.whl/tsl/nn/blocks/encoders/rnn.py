import torch
from einops import rearrange
from torch import nn

from tsl.nn.base import MultiGRUCell, MultiLSTMCell
from tsl.nn.base.recurrent import RNNBase
from ...utils import maybe_cat_exog


class RNN(nn.Module):
    """Simple RNN encoder with optional linear readout.

        Args:
        input_size (int): Input size.
        hidden_size (int): Units in the hidden layers.
        exog_size (int, optional): Size of the optional exogenous variables.
        output_size (int, optional): Size of the optional readout.
        n_layers (int, optional): Number of hidden layers. (default: 1)
        cell (str, optional): Type of cell that should be use (options: [`gru`,
            `lstm`]). (default: `gru`)
        dropout (float, optional): Dropout probability.
    """

    def __init__(self, input_size: int, hidden_size: int,
                 exog_size: int = None, output_size: int = None,
                 n_layers: int = 1, return_only_last_state: bool = False,
                 cell: str = 'gru',
                 bias: bool = True,
                 dropout: float = 0.,
                 **kwargs):
        super(RNN, self).__init__()

        self.return_only_last_state = return_only_last_state

        if cell == 'gru':
            cell = nn.GRU
        elif cell == 'lstm':
            cell = nn.LSTM
        else:
            raise NotImplementedError(f'"{cell}" cell not implemented.')

        if exog_size is not None:
            input_size += exog_size

        self.rnn = cell(input_size=input_size,
                        hidden_size=hidden_size,
                        num_layers=n_layers,
                        bias=bias,
                        dropout=dropout)

        if output_size is not None:
            self.readout = nn.Linear(hidden_size, output_size)
        else:
            self.register_parameter('readout', None)

    def forward(self, x, u=None):
        """

        Args:
            x (torch.Tensor): Input tensor.
            return_last_state: Whether to return only the state corresponding to the last time step.
        """
        # x: [batches, steps, nodes, features]
        x = maybe_cat_exog(x, u)
        b, *_ = x.size()
        x = rearrange(x, 'b s n f -> s (b n) f')
        x, *_ = self.rnn(x)
        # [steps batches * nodes, features] -> [steps batches, nodes, features]
        x = rearrange(x, 's (b n) f -> b s n f', b=b)
        if self.return_only_last_state:
            x = x[:, -1]
        if self.readout is not None:
            return self.readout(x)
        return x


class MultiRNN(RNNBase):

    def __init__(self, input_size: int, hidden_size: int, n_instances: int,
                 n_layers: int = 1, cat_states_layers: bool = False,
                 return_only_last_state: bool = False,
                 cell: str = 'gru',
                 bias: bool = True,
                 **kwargs):

        if cell == 'gru':
            cell = MultiGRUCell
        elif cell == 'lstm':
            cell = MultiLSTMCell
        else:
            raise NotImplementedError(f'"{cell}" cell not implemented.')

        rnn_cells = [
            cell(input_size if i == 0 else hidden_size, hidden_size,
                 n_instances, bias=bias, **kwargs)
            for i in range(n_layers)
        ]
        super(MultiRNN, self).__init__(rnn_cells, cat_states_layers,
                                       return_only_last_state)
