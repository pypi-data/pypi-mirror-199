# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snap_pslg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snap-pslg',
    'version': '0.3.0',
    'description': 'simplify a pslg with iterated snap rounding',
    'long_description': '# snap_pslg\n\nRefine a [planar straight-line graph](https://en.wikipedia.org/wiki/Planar_straight-line_graph) with [iterated snap rounding](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.23.220). No numpy dependency.\n\n* floor all points to integer coordinates\n* eliminate edge intersections and t-junctions\n* if allowed to converge, no point will be within .5 units of an edge. You can remove this constraint entirely, maintaing more of the input shape at the cost of near t-junctions, by setting max_iterations to 0.\n\nThis will slightly distort the pslg, but the result will be ready for triangulation and other algorithms.\n\n## install\n~~~\npip install snap_pslg\n~~~\n\n## signature\n~~~python\nVec2 = Annotated[Iterable[float], "2D vector"]\n\ndef snap_round_pslg(\n    points: Iterable[Vec2], edges: Iterable[tuple[int, int]], max_iterations: int = 100\n) -> tuple[list[IntPoint], list[tuple[int, int]]]:\n    """Perform one iteration of snap rounding.\n\n    :param points: A list of 2D points\n    :param edges: A list of edges, each a pair of indices into points\n    :param max_iterations: optionally limit number of iterations to perform. By\n        default, will try 100 iterations to reach convergence.\n    :return: A list of 2D points, a list of edges, each a pair of indices into points\n\n    Some of the points may not have indices. That is fine.\n    """\n~~~\n\n## usage\n\n~~~python\nfrom snap_pslg import snap_round_pslg\n\npoints = [(0, 0), (3, 0), (3, 3), (0, 3), (5, 5)]\nedges = [(0, 2), (1, 3)]\n\n# You might have noticed that point (5, 5) was never used. This is fine. It\n# will be retained as a point and any line segments that pass very close to it\n# will be routed through it.\n\nnew_points, new_segments = snap_round_pslg(points, edges)\n\nnew_points  # [(0, 0), (5, 5), (3, 3), (2, 2), (0, 3), (3, 0)]\nnew_edges  # [(0, 3), (4, 3), (3, 2), (3, 5)]\n\n# a new point, (3, 3) has been added at the segment intersection\n# each segment is broken into two pieces\n~~~\n',
    'author': 'Shay Hill',
    'author_email': 'shay_public@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
