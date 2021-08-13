"""
Examples

--n 2 --F F+FF-FF-F-F+F+FF-F-F+F+FF+FF-F
--n 4 --w " -F" --F F+F-F-F+F
--n 2 --w F+F+F+F --F F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF --f ffffff
--n 4 --w F-F-F-F --F FF-F-F-F-F-F+F
--n 4 --w F-F-F-F --F FF-F-F-F-FF
--n 3 --w F-F-F-F --F FF-F+F-F-FF
--n 4 --w F-F-F-F --F FF-F--F-F
--n 5 --w F-F-F-F --F F-FF--F-F
--n 4 --w F-F-F-F --F F-F+F-F-F
"""

import argparse
import math

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


class Generator:
    def __init__(self, d: float, alpha: float):
        self.x = [0.0, 0.0]
        self.y = [0.0, 0.0]
        self.angle = 90.0 * math.pi / 180.0

        self.d = d
        self.angle_increment = alpha * math.pi / 180.0

        _, self.ax = plt.subplots()

    def run_command(self, command: str) -> None:
        if command == "F" or command == "f":
            self.x[0] = self.x[1]
            self.y[0] = self.y[1]
            self.x[1] = self.x[0] + self.d * math.cos(self.angle)
            self.y[1] = self.y[0] + self.d * math.sin(self.angle)

            if command == "F":
                self.ax.plot(self.x, self.y, color="k", linewidth=1.0)

        elif command == "-":
            self.angle -= self.angle_increment
        elif command == "+":
            self.angle += self.angle_increment

    def get_axes(self) -> plt.axes:
        return self.ax


def main(
    w: str, F: str, f: str, n: int, step_length: float, angle_increment: float
) -> None:
    w = w.strip()
    F = F.strip()
    f = f.strip()

    # Generate command string
    for _ in range(n):
        if len(f) == 0:
            w = w.replace("F", F)
        else:
            w = w.replace("F", "x")
            w = w.replace("f", f)
            w = w.replace("x", F)

    generator = Generator(step_length, angle_increment)

    print(w[:10])
    for command in tqdm(w):
        generator.run_command(command)

    ax = generator.get_axes()
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--w", type=str, default="F-F-F-F")
    parser.add_argument("--F", type=str, default="F-F+F+FF-F-F+F")
    parser.add_argument("--f", type=str, default="")
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--d", type=float, default=1.0)
    parser.add_argument("--a", type=float, default=90.0)
    args = parser.parse_args()

    main(args.w, args.F, args.f, args.n, args.d, args.a)
