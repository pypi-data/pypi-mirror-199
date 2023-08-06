from einops import rearrange, repeat
from torch_geometric.data.collate import collate
from torch_geometric.transforms import BaseTransform
from torch_geometric.utils.num_nodes import maybe_num_nodes

from tsl.data import Data, StaticBatch

# def cartesian_product_graph(edge_index, num_steps, num_nodes=None):
#     num_nodes = maybe_num_nodes(num_nodes)


def cart_prod(data, t):
    for key, value in data.items():
        pattern = data.pattern.get(key)
        if pattern is not None and 'n' in pattern:
            if 't' in pattern:  # '... t n ...' -> '... (t n) ...'
                new_pattern = pattern.replace('t ', '')
                change_pattern = new_pattern.replace('n', '(t n)')
                value = rearrange(value, f'{pattern} -> {change_pattern}')
            else:
                new_pattern = pattern
                change_pattern = pattern.replace('n', '(t n)')
                repeat(value, f'{pattern} -> {change_pattern}', t=t)
            data[key] = value
            data.pattern[key] = new_pattern
    # edge_index ?


def unpack_data(data, t):
    data_list = []
    for _ in range(t):
        d = Data()
        data_list.append(d.stores_as(data))

    for key, value in data.items():
        if key == 'transform':
            continue
        pattern = data.pattern.get(key)
        if 't' in pattern:
            pattern_tokens = pattern.replace(' ', '')
            t_dim = pattern_tokens.index('t')
            new_pattern = ' '.join(pattern_tokens.replace('t', ''))
            for i in range(value.size(t_dim)):
                data_list[i][key] = value.select(t_dim, i)
                data_list[i].pattern[key] = new_pattern
        else:
            data_list[i][key] = value

    return data_list


class CartesianProduct(BaseTransform):

    def __call__(self, data: Data) -> Data:
        data_list = unpack_data(data)
        out_data, slice_dict, inc_dict = collate(
            Data,
            data_list=data_list,
            increment=True,
            add_batch=not isinstance(data_list[0], Batch),
            follow_batch=follow_batch,
            exclude_keys=exclude_keys,
        )
        return out_data