import numpy as np
from similaritymeasures import frechet_dist


def procrustes_rotate(road_points1, road_points2):
    """
    Given road_points1 and road_points2 with starting points both at the origin (0, 0)
    This function rotates road_points1 based on Procrusted analysis mentioned in
    https://en.wikipedia.org/wiki/Procrustes_analysis
    https://github.com/chanind/curve-matcher
    Returns (rotated road_points1, original road_points2)
    """

    k = np.min([road_points1.shape[0], road_points2.shape[0]])

    # columns of road_points1
    xs = road_points1[0:k, 0] # column 1
    ys = road_points1[0:k, 1] # column 2

    # columns of road_points2
    ws = road_points2[0:k, 0] # column 1
    zs = road_points2[0:k, 1] # column 2

    theta = np.arctan2(ws.T @ ys - zs.T @ xs, ws.T @ xs + zs.T @ ys)

    rotation_matrix = np.array([[np.cos(-theta), np.sin(-theta)],
                                [-np.sin(-theta), np.cos(-theta)]])

    return (road_points1 @ rotation_matrix, road_points2)


def move(road_points):
    """
    This function moves road_points so that the road starts from (0, 0)
    """
    start_x = road_points[0, 0]
    start_y = road_points[0, 1]

    starting_point = np.array([[start_x, start_y]])
    moved_road_points = road_points - np.repeat(starting_point, road_points.shape[0], axis=0)

    return moved_road_points


def move_procrustes_rotate(road_points1, road_points2):
    """
    Given road_points1 and road_points2
    This function first moves both roads so that the starting points are both at the origin (0, 0) and then rotates the road_points1 using procrustes_rotate function above
    Returns (rotated moved road_points1, moved road_points2)
    """

    moved_road_points1 = move(road_points1)
    moved_road_points2 = move(road_points2)

    return procrustes_rotate(moved_road_points1, moved_road_points2)


def procrustes_frechet(road_points1, road_points2):
    """
    THE CODE IS BASED ON THE IDEA FROM: https://github.com/chanind/curve-matcher
    Before calculating Frechet distance, do Procrustes analysis for rotation, find theta
    Then rotate one of the road for -theta, then compute Frechet distance
    https://en.wikipedia.org/wiki/Procrustes_analysis
    """
    (moved_rotated_road_points1, moved_rotated_road_points2) = move_procrustes_rotate(road_points1, road_points2)
    return frechet_dist(moved_rotated_road_points1, moved_rotated_road_points2)

def move_rotate(road_points):
    """
    Moves and rotates a given list of road points (so that road starts from (0, 0) and the end point is on the x axis)
    Takes numpy array([[x0, y0], ..., [xN-1, yN-1]])
    Returns numpy array([[0, 0], ..., [barxN-1, 0]])
    """

    start_x = road_points[0, 0]
    start_y = road_points[0, 1]
    end_x = road_points[-1, 0]
    end_y = road_points[-1, 1]

    # angle of the last point on road
    theta = np.arctan2(end_y-start_y, end_x-start_x)

    # move the start point to origin (0, 0)
    starting_point = np.array([[start_x, start_y]])
    moved_road_points = road_points - np.repeat(starting_point, road_points.shape[0], axis=0)

    # we rotate all points by -theta radians (theta in opposite direction)
    # this rotation matrix is for multiplying from right, so it is the transpose of the standard form
    rotation_matrix = np.array([[np.cos(-theta), np.sin(-theta)],
                                [-np.sin(-theta), np.cos(-theta)]])

    # rotate the moved road points
    return moved_road_points @ rotation_matrix


def simple_frechet(road_points1, road_points2):
    (moved_rotated_road_points1, moved_rotated_road_points2) = move_rotate(road_points1), move_rotate(road_points2)
    return frechet_dist(moved_rotated_road_points1, moved_rotated_road_points2)
