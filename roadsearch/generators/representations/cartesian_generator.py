from roadsearch.utils.catmull import ControlNodesGenerator
from roadsearch.generators.representations.road_generator import RoadGenerator

def points_to_deltas(control_points):
    x1,y1 = 0, 0
    res = []
    for x, y in control_points:
        res.append((x-x1, y-y1))
        x1 = x
        y1 = y
    return res


def deltas_to_points(deltas):
    res = []
    x0, y0 = 0, 0
    for x,y in deltas:
        x0+=x
        y0+=y
        res.append((x0, y0))
    return res


class CatmullRomGenerator(RoadGenerator):

    def __init__(self, control_nodes: int, variation: int = 0, max_angle=35, num_spline_nodes=20, seg_length=10):
        self.generator = ControlNodesGenerator(num_control_nodes=control_nodes,
                                               max_angle=max_angle,
                                               seg_length=seg_length,
                                               num_spline_nodes=num_spline_nodes)

        super().__init__(length=control_nodes, variation=variation)

    def generate(self):
        control_nodes = [(x, y) for (x, y, z, d) in self.generator.generate_key_control_nodes(self.get_length())]
        deltas_control_nodes = points_to_deltas(control_nodes)
        return deltas_control_nodes

    def to_cartesian(self, test):
        control_nodes = [(x, y, -28.0, 8.0) for x, y in deltas_to_points(test)]
        road = self.generator.control_nodes_to_road(control_nodes)
        return road

    def get_value(self, previous):
        raise Exception("This generator does not implement get value.")
