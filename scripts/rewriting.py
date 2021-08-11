import argparse
import math
import time
from typing import List, Tuple
import sys

import matplotlib.pyplot as plt
import numpy as np

DEFAULT_SIDES = 3
DEFAULT_SIDE_LENGTH = 1.
DEFAULT_DEPTH = 3
DEFAULT_ROTATION_OFFSET = 0.


def initiator(
    sides: int, length: float, init_offset: float = 0.
) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    internal_angle = 2.0 * math.pi / float(sides)
    offset = internal_angle / 2.0 if (sides % 2 == 0) else 0.0
    center_to_vertex_length = (length / 2.0) / math.sin(internal_angle / 2.0)

    edges = list()
    for i in range(sides):
        theta = internal_angle * i + offset + init_offset
        starting_edge = (
            center_to_vertex_length * math.sin(theta),
            center_to_vertex_length * math.cos(theta),
        )
        ending_edge = (
            center_to_vertex_length * math.sin(theta + internal_angle),
            center_to_vertex_length * math.cos(theta + internal_angle),
        )
        edges.append((starting_edge, ending_edge))

    return edges


def rewriter(
    init_edges: List[Tuple[Tuple[float, float], Tuple[float, float]]],
    candidate: np.array,
) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Replace edges with candidate"""
    edges = list()
    for (x0, y0), (x1, y1) in init_edges:
        # Scale candidate
        init_edge_length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        scaled_candidate = init_edge_length * candidate

        # Rotate candidate
        theta = math.atan2(y1 - y0, x1 - x0)
        rotation_matrix = np.array(
            [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]]
        )
        rotated_candidate = (np.matmul(rotation_matrix, scaled_candidate.T)).T

        # Translate candidate
        translated_candidate = rotated_candidate + np.array([x0, y0])

        # Insert new edges
        for row_ind in range(translated_candidate.shape[0] - 1):
            edges.append(
                (
                    (
                        translated_candidate[row_ind, 0],
                        translated_candidate[row_ind, 1],
                    ),
                    (
                        translated_candidate[row_ind + 1, 0],
                        translated_candidate[row_ind + 1, 1],
                    ),
                )
            )

    return edges


def plot_edges(edges: List[Tuple[Tuple[float, float], Tuple[float, float]]]) -> None:
    start_time = time.time()
    _, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.axis("off")
    for (x0, y0), (x1, y1) in edges:
        ax.plot([x0, x1], [y0, y1], color="k", linewidth=1.0)
    print(f"Plotting {len(edges)} edges: {(time.time() - start_time) * 1000:.1f}ms")
    plt.show()


def main(sides: int, length: float, depth: int, shape_offset: float) -> None:
    # Generate initial edges
    edges = initiator(sides, length, shape_offset * math.pi / 180.)

    # Plot initial edges
    plot_edges(edges)

    # Rewrite edges
    candidate = np.array(
        [
            [0.0, 0.0],
            [1.0 / 3.0, 0.0],
            [0.5, 1.0 / 3.0 * math.sin(math.pi / 3.0)],
            [2.0 / 3.0, 0.0],
            [1.0, 0.0],
        ]
    )

    for i in range(depth):
        start_time = time.time()
        edges = rewriter(edges, candidate)
        print(f"Rewrite {i + 1}: {(time.time() - start_time) * 1000:.1f}ms")

    # Plot rewritten edges
    if depth > 0:
        plot_edges(edges)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--s", type=int, help="number of initial sides", default=DEFAULT_SIDES)
    parser.add_argument("--l", type=float, help="side length", default=DEFAULT_SIDE_LENGTH)
    parser.add_argument("--o", type=float, help="default shape offset (deg)", default=DEFAULT_ROTATION_OFFSET)
    parser.add_argument("--d", "--depth", type=int, help="number of rewrites", default=DEFAULT_DEPTH)

    args = parser.parse_args()

    if args.s < 3:
        print("Sides must be >= 3")
        sys.exit(1)

    if args.l <= 0.0:
        print("Side length must be > 0")
        sys.exit(1)

    main(args.s, args.l, args.d, args.o)
