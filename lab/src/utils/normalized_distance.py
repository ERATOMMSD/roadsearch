import numpy as np


def road_length(road_points):
    dxs = road_points[1:, 0] - road_points[0:-1, 0]
    dys = road_points[1:, 1] - road_points[0:-1, 1]
    delta_ss = np.sqrt(dxs * dxs + dys * dys)
    return np.sum(delta_ss)


def normalized_distance(distance_function, road_points1, road_points2):
    length1 = road_length(road_points1)
    length2 = road_length(road_points2)
    return distance_function(road_points1, road_points2) / np.array([length1, length2]).max()


def normalized_distance_value(distance_value, road_points1, road_points2):
    length1 = road_length(road_points1)
    length2 = road_length(road_points2)
    return distance_value / np.array([length1, length2]).max()

# print(normalized_distance(simple_frechet, road_points1, road_points2))
# print(normalized_distance(relative_angle_distance, road_points1, road_points2))
