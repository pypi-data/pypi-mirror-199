"""
This module contains functionality which is specifically useful for the generation of color-based datasets.
"""
import typing as t

import visual_graph_datasets.typing as tc


# Global variables for RGB codes
WHITE = [1., 1., 1.]
GRAY = [0.8, 0.8, 0.8]
BLACK = [0., 0., 0.]
RED = [1., 0., 0.]
YELLOW = [1., 1., 0.]
GREEN = [0., 1., 0.]
CYAN = [0., 1., 1.]
BLUE = [0., 0., 1.]
MAGENTA = [1., 0., 1.]


def make_star_motif(inner_color: tc.ColorList,
                    outer_color: tc.ColorList,
                    k: int = 3,
                    edge_attributes: t.List[float] = [1.0],
                    ) -> tc.GraphDict:
    """
    Creates a color motif of a star, which consists of a center node and ``k`` outer nodes, which are all
    exclusively connected the center node. The center node has the color ``inner_color`` and all the outer
    nodes share the same color ``outer_color``.
    """
    graph = {
        'node_indices': [0],
        'node_attributes': [
            inner_color,
        ],
        'edge_indices': [],
        'edge_attributes': []
    }

    for i in range(1, k + 1):
        graph['node_indices'].append(i)
        graph['node_attributes'].append(outer_color)

        # Adding the edges from the just added outer "star" node to the inner node
        graph['edge_indices'] += [[0, i], [i, 0]]
        graph['edge_attributes'] += [edge_attributes, edge_attributes]

    return graph


def make_ring_motif(start_color: tc.ColorList,
                    ring_color: tc.ColorList,
                    k: int = 3,
                    edge_attributes: t.List[int] = [1]
                    ) -> tc.GraphDict:
    graph = {
        'node_indices': [0],
        'node_attributes': [
            start_color,
        ],
        'edge_indices': [],
        'edge_attributes': []
    }

    prev_index = 0
    for i in range(1, k + 1):
        graph['node_indices'].append(i)
        graph['node_attributes'].append(ring_color)

        # Adding an edge from the previous element in the ring to the current one
        graph['edge_indices'] += [[prev_index, i], [i, prev_index]]
        graph['edge_attributes'] += [edge_attributes, edge_attributes]
        prev_index = i

    # At the end we need to add an additional edge from the end of the ring to the starting node
    graph['edge_indices'] += [[prev_index, 0], [0, prev_index]]
    graph['edge_attributes'] += [edge_attributes, edge_attributes]

    return graph


def make_grid_motif(color_1: tc.ColorList,
                    color_2: tc.ColorList,
                    n: int = 2,
                    m: int = 2,
                    edge_attributes: t.List[float] = [1.]):
    graph = {
        'node_indices': [],
        'node_attributes': [],
        'edge_indices': [],
        'edge_attributes': []
    }

    colors = [color_1, color_2]

    prev_row = None
    prev_index = None
    index = 0
    for j in range(m):

        color_index = int(j % 2)
        row = []
        for i in range(n):
            graph['node_indices'].append(index)
            graph['node_attributes'].append(colors[color_index])

            if prev_index is not None:
                graph['edge_indices'] += [[prev_index, index], [index, prev_index]]
                graph['edge_attributes'] += [edge_attributes, edge_attributes]

            if prev_row is not None:
                graph['edge_indices'] += [[prev_row[i], index], [index, prev_row[i]]]
                graph['edge_attributes'] += [edge_attributes, edge_attributes]

            row.append(index)
            color_index = int(not color_index)
            prev_index = index
            index += 1

        prev_row = row
        prev_index = None

    return graph
