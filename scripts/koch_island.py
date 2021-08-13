import argparse
import math

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


class Generator:
    def __init__(self, d: float, alpha: float):
        self.path = list()
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0

        self.d = d
        self.angle_increment = alpha * math.pi / 180.0

        self.path.append((self.x, self.y))

    def run_command(self, command: str) -> None:
        if command == "F" or command == "f":
            self.x += self.d * math.cos(self.angle)
            self.y += self.d * math.sin(self.angle)

            if command == "F":
                self.path.append((self.x, self.y))
        elif command == "-":
            self.angle -= self.angle_increment
        elif command == "+":
            self.angle += self.angle_increment

    def get_path(self) -> np.array:
        return np.array(self.path)


def main(w: str, p: str, n: int, step_length: float, angle_increment: float) -> None:
    # Generate command string
    for _ in range(n):
        w = w.replace("F", p)

    generator = Generator(step_length, angle_increment)

    for command in tqdm(w):
        generator.run_command(command)

    coords = generator.get_path()
    _, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.axis("off")
    ax.plot(coords[:, 0], coords[:, 1], color="k", linewidth=1.0)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--w", type=str, default="F-F-F-F")
    parser.add_argument("--p", type=str, default="F-F+F+FF-F-F+F")
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--d", type=float, default=1.0)
    parser.add_argument("--a", type=float, default=90.0)
    args = parser.parse_args()

    main(args.w, args.p, args.n, args.d, args.a)
