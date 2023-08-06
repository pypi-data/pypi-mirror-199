import numpy as np
import matplotlib.pyplot as plt
import math


def isMathematicalFunction(mapping):
    """
    Determines whether the given dictionary of sets represents a mathematical function.

    Args:
        mapping: A dictionary of sets representing the function.

    Returns:
        True if the mapping represents a function, False otherwise.
    """
    # Check if the mapping is empty
    if not mapping:
        return False

    # Check if every key maps to a single value
    for key in mapping:
        if len(mapping[key]) != 1:
            return False

    # Check if multiple keys map to the same value
    values = set()
    for key in mapping:
        value = tuple(mapping[key])[0]
        if value in values:
            return False
        values.add(value)

    # If we made it here, the mapping represents a function
    return True


def solveGraphically(f1, f2, x_range=(-10, 10), num_points=1000):
    x = np.linspace(*x_range, num=num_points)
    y1 = f1(x)
    y2 = f2(x)

    fig, ax = plt.subplots()
    ax.plot(x, y1, label='f1')
    ax.plot(x, y2, label='f2')
    ax.legend()

    intersections = []
    for i in range(num_points - 1):
        if np.sign(y1[i] - y2[i]) != np.sign(y1[i+1] - y2[i+1]):
            x_intersect = (x[i] * (y1[i+1] - y2[i+1]) - x[i+1] * (y1[i] - y2[i])) / (y1[i+1] - y1[i] - y2[i+1] + y2[i])
            y_intersect = f1(x_intersect)
            intersections.append((x_intersect, y_intersect))
    if not intersections:
        plt.show()
        return None
    else:
        for intersection in intersections:
            ax.plot(intersection[0], intersection[1], 'ro')
        plt.show()
        return intersections


def solveOneVarEquation(equation):
    try:
        # Split the equation into two sides using the equal sign
        lhs, rhs = equation.split('=')
        # Evaluate each side of the equation and subtract one from the other
        solution = eval(rhs) - eval(lhs)
        return solution

    except (NameError, SyntaxError, ValueError):
        return "Invalid equation"


def sqrt(__x):
    return __x ** 0.5


def rootOf(__x, num):
    return __x ** (1/num)


def isDivisible(x, num):
    if x % num != 0:
        return False
    else:
        return True


def normalize(value):
    value = value - int(value)
    if value < 0:
        value = value + 1
    return value



