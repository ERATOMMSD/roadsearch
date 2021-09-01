import numpy as np

def relative_angle_distance_aux(road_points1, road_points2):
    """ Relative angle distance, similar to the approach in
    Rotation Invariant Distance Measures for Trajectories (http://alumni.cs.ucr.edu/~mvlachos/pubs/kdd04.pdf)
    """

    k = np.min([road_points1.shape[0], road_points2.shape[0]])
    dxs1 = road_points1[1:k, 0] - road_points1[0:k-1, 0]
    dys1 = road_points1[1:k, 1] - road_points1[0:k-1, 1]

    dxs2 = road_points2[1:k, 0] - road_points2[0:k-1, 0]
    dys2 = road_points2[1:k, 1] - road_points2[0:k-1, 1]

    delta_thetas1 = np.arctan2(dys1, dxs1)
    delta_thetas2 = np.arctan2(dys2, dxs2)

    delta_ss1 = np.sqrt(dxs1 * dxs1 + dys1 * dys1)
    delta_ss2 = np.sqrt(dxs2 * dxs2 + dys2 * dys2)

    ss1 = np.zeros(delta_ss1.shape[0] + 1)
    ss2 = np.zeros(delta_ss2.shape[0] + 1)
    ss1[1:] = np.cumsum(delta_ss1)
    ss2[1:] = np.cumsum(delta_ss2)

    # we want to take integral of |\Delta\Theta_1(s) - \Delta\Theta_2(s)|

    # print(ss1)
    # print(delta_thetas1)
    # print("")
    # print(ss2)
    # print(delta_thetas2)
    # print("")

    all_ss = [0.0]
    diff_delta_thetas = []

    index1 = 0
    index2 = 0
    while True:
        # print(all_ss[-1])
        # print(delta_thetas1[index1])
        # print(delta_thetas2[index2])
        # print("")
        if index1 < delta_thetas1.shape[0] and index2 < delta_thetas2.shape[0]:
            diff_delta_thetas.append(np.abs(delta_thetas1[index1] - delta_thetas2[index2]))
        else:
            break

        if ss1[index1 + 1] < ss2[index2 + 1]:
            index1 += 1
            all_ss.append(ss1[index1])
        else:
            index2 += 1
            all_ss.append(ss2[index2])

    integral = 0.0
    total_s = all_ss[-1]
    for i in range(len(all_ss) - 1):
        integral += diff_delta_thetas[i] * (all_ss[i + 1] - all_ss[i])

    return (integral, total_s)


def relative_angle_distance(road_points1, road_points2):
    (integral, total_s) = relative_angle_distance_aux(road_points1, road_points2)
    return integral


def normalized_relative_angle_distance(road_points1, road_points2):
    (integral, total_s) = relative_angle_distance_aux(road_points1, road_points2)
    return integral / total_s


# relative_angle_distance_aux(np.array([[0, 0], [2, 7], [2.5, 9], [3, 15], [10, 15]]),
#                             np.array([[0, 3], [2, 5], [1, 10], [-1, 9], [-2, 6], [-4.0, 2]]))
#
# print(relative_angle_distance(np.array([[0, 0], [2, 7], [2.5, 9], [3, 15], [10, 15]]),
#                               np.array([[0, 3], [2, 5], [1, 10], [-1, 9], [-2, 6], [-4.0, 2]])))
#
# print(normalized_relative_angle_distance(np.array([[0, 0], [2, 7], [2.5, 9], [3, 15], [10, 15]]),
#                                          np.array([[0, 3], [2, 5], [1, 10], [-1, 9], [-2, 6], [-4.0, 2]])))
