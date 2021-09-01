import bezier
import numpy as np
from utils.trapezoidal_integration import frenet_to_cartesian, thetas_to_cartesian
from utils.catmull import catmull_rom, deltas_to_points


def transform_kappa_to_cartesian(test, step=7.5):
    ss = np.cumsum([step] * len(test)) - step  # start from zero
    return frenet_to_cartesian(x0=0, y0=0, theta0=1.57, ss=ss, kappas=test)


def transform_kappa_step_to_cartesian(test):
    kappas, ss_deltas = zip(*test)

    # the last value of ss_deltas is not used
    ss = np.zeros(len(kappas))  # ss =[0, 0, 0, 0]
    ss[1:] = np.cumsum(ss_deltas[0:-1])  # [0, 2, 4, 6]

    return frenet_to_cartesian(x0=0, y0=0, theta0=1.57, ss=ss, kappas=kappas)


def transform_theta_to_cartesian(test, step=5):
    ss_deltas = [step] * len(test)
    return thetas_to_cartesian(x0=0, y0=0, theta0=1.57, ss_deltas=ss_deltas, delta_thetas=test)


def transform_theta_step_to_cartesian(test):
    delta_thetas, ss_deltas = zip(*test)
    return thetas_to_cartesian(x0=0, y0=0, theta0=1.57, ss_deltas=ss_deltas, delta_thetas=delta_thetas)


def transform_control_nodes_to_cartesian(test, initial_node=(125.0, 0.0, -28.0, 8.0), num_spline_nodes=10):
    control_nodes = [(x, y, -28.0, 8.0) for x, y in deltas_to_points(test)]
    nodes = [initial_node] + control_nodes
    sample_nodes = catmull_rom(nodes, num_spline_nodes)
    road = [(node[0], node[1]) for node in sample_nodes]
    return road


def transform_bezier_to_cartesian(test, interpolation_nodes=9):
    delta_xs, delta_ys = zip(*test)
    xs = np.cumsum(list(delta_xs))
    ys = np.cumsum(list(delta_ys))

    nodes = np.asfortranarray([xs, ys])

    # generate curve
    curve = bezier.Curve.from_nodes(nodes)

    # to cartesian
    cartesian = curve.evaluate_multi(np.linspace(0, 1.0, len(xs) * interpolation_nodes))
    road = list(zip(cartesian[0], cartesian[1]))

    return road


def transformation_function(representation):
    mapping = {'bezier': transform_bezier_to_cartesian,
               'cartesian': transform_control_nodes_to_cartesian,
               'kappa': transform_kappa_to_cartesian, 
               'kappa+step': transform_kappa_step_to_cartesian, 
               'theta': transform_theta_to_cartesian, 
               'theta+step': transform_theta_step_to_cartesian}
    
    return mapping[representation]
