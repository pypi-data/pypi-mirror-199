# snap_pslg

Refine a [planar straight-line graph](https://en.wikipedia.org/wiki/Planar_straight-line_graph) with [iterated snap rounding](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.23.220). No numpy dependency.

* floor all points to integer coordinates
* eliminate edge intersections and t-junctions
* if allowed to converge, no point will be within .5 units of an edge. You can remove this constraint entirely, maintaing more of the input shape at the cost of near t-junctions, by setting max_iterations to 0.

This will slightly distort the pslg, but the result will be ready for triangulation and other algorithms.

## install
~~~
pip install snap_pslg
~~~

## signature
~~~python
Vec2 = Annotated[Iterable[float], "2D vector"]

def snap_round_pslg(
    points: Iterable[Vec2], edges: Iterable[tuple[int, int]], max_iterations: int = 100
) -> tuple[list[IntPoint], list[tuple[int, int]]]:
    """Perform one iteration of snap rounding.

    :param points: A list of 2D points
    :param edges: A list of edges, each a pair of indices into points
    :param max_iterations: optionally limit number of iterations to perform. By
        default, will try 100 iterations to reach convergence.
    :return: A list of 2D points, a list of edges, each a pair of indices into points

    Some of the points may not have indices. That is fine.
    """
~~~

## usage

~~~python
from snap_pslg import snap_round_pslg

points = [(0, 0), (3, 0), (3, 3), (0, 3), (5, 5)]
edges = [(0, 2), (1, 3)]

# You might have noticed that point (5, 5) was never used. This is fine. It
# will be retained as a point and any line segments that pass very close to it
# will be routed through it.

new_points, new_segments = snap_round_pslg(points, edges)

new_points  # [(0, 0), (5, 5), (3, 3), (2, 2), (0, 3), (3, 0)]
new_edges  # [(0, 3), (4, 3), (3, 2), (3, 5)]

# a new point, (3, 3) has been added at the segment intersection
# each segment is broken into two pieces
~~~
