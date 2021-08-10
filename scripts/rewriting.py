import argparse
import math
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt


DEFAULT_SIDES = 3
DEFAULT_SIDE_LENGTH = 1
DEFAULT_DEPTH = 3


def initiator(
    sides: int, length: float
) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    internal_angle = 2.0 * math.pi / float(sides)
    offset = internal_angle / 2.0 if (sides % 2 == 0) else 0.0
    center_to_vertex_length = (length / 2.0) / math.sin(internal_angle / 2.0)

    edges = list()
    for i in range(sides):
        theta = internal_angle * i + offset
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
    init_edges: List[Tuple[Tuple[float, float], Tuple[float, float]]]
) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    pass


def main(sides: int, length: float, depth: int) -> None:
    # Generate initial edges
    edges = initiator(sides, length)

    # Plot initial edges
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.axis("off")
    for (x0, y0), (x1, y1) in edges:
        ax.plot([x0, x1], [y0, y1], color="k", linewidth=1.0)

    plt.show()

    # Rewrite edges
    for _ in range(depth):
        edges = rewriter(edges)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--s", type=int)
    parser.add_argument("--l", type=float)
    parser.add_argument("--d", "--depth", type=int)
    args = parser.parse_args()

    sides = DEFAULT_SIDES
    if args.s:
        sides = args.s

    if sides < 3:
        print("Sides must be >= 3")
        exit(1)

    side_length = DEFAULT_SIDE_LENGTH
    if args.l:
        side_length = args.l

    if side_length <= 0.0:
        print("Side length must be > 0")
        exit(1)

    depth = DEFAULT_DEPTH
    if args.d:
        depth = args.d

    main(sides, side_length, depth)
