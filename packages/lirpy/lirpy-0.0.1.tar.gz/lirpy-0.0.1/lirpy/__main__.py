import argparse
from typing import List, Tuple

from lirpy.mask import Mask
from lirpy.point import Point, dist_points
from lirpy.rect import Rect
from lirpy.rectangulator import Rectangulator

dirchoices = []
for axis in "XYZ":
    for plusmin in "+-":
        dirchoices.append(f"{plusmin}{axis}")


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument("x", type=int)
    argp.add_argument("y", type=int)
    argp.add_argument("z", type=int)
    argp.add_argument("--radius", "-r", type=int)
    argp.add_argument("--depth", "-d", type=int, default=1)
    argp.add_argument("--axis", choices=dirchoices, default="-Y")
    argp.add_argument("--dump-steps", action='store_true', default=False)
    args = argp.parse_args()
    x: int = args.x
    y: int = args.y
    z: int = args.z
    r: int = args.radius
    d: int = args.depth - 1
    dump_steps: bool = args.dump_steps
    assert d >= 0
    c = Point(x=r, y=r)
    print(f'Center: {x} {y} {z}')
    print(f'Radius: {r}')
    print(f'Depth: {d}')
    print(f'Along axis: {args.axis}')
    m = Mask(height=r * 2 + 1, width=r * 2 + 1)
    m.setif(lambda x, y, v: dist_points(Point(x, y), c) <= r)
    rt = Rectangulator(m)
    rect: Rect
    written = set()
    cuboids: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = []
    for rect in rt.findAll(verbose=dump_steps):
        minx = rect.min.x
        miny = rect.min.y
        maxx = rect.max.x
        maxy = rect.max.y
        k = (minx, miny, maxx, maxy)
        if k in written:
            continue
        written.add(k)
        p1 = (0, 0, 0)
        p2 = (0, 0, 0)
        match args.axis:
            case "+X":
                p1 = (x, minx + r + y, miny + r + z)
                p2 = (x + d, maxx + r + y, maxy + r + z)
            case "-X":
                p1 = (x, minx + r + y, miny + r + z)
                p2 = (x - d, maxx + r + y, maxy + r + z)
            case "+Y":
                p1 = (minx + r + x, y, miny + r + z)
                p2 = (maxx + r + x, y + d, maxy + r + z)
            case "-Y":
                p1 = (minx + r + x, y, miny + r + z)
                p2 = (maxx + r + x, y - d, maxy + r + z)
            case "+Z":
                p1 = (minx + r + x, miny + r + y, z)
                p2 = (maxx + r + x, maxy + r + y, z + d)
            case "-Z":
                p1 = (minx + r + x, miny + r + y, z)
                p2 = (maxx + r + x, maxy + r + y, z - d)
        cuboids.append((p1, p2))
    print("#sel clear")
    for p1, p2 in cuboids:
        p1 = " ".join(list(map(str, p1)))
        p2 = " ".join(list(map(str, p2)))
        print(f"#sel 1 {p1}")
        print(f"#sel 2 {p2}")


if __name__ == "__main__":
    main()
