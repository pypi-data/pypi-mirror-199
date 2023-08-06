"""Implementation of overdamped equations of motion."""

import math


def l_to_lambda(l, p):
    """Convert from continuous number of sites in an overlap to lambda."""
    return (l - 1) * p.deltad / p.deltas


def lambda_to_l(lmbda, p):
    """Convert from lambda to continuous number of sites in an overlap."""
    return 1 + p.deltas / p.deltad * lmbda


def lambda_to_l_discrete(lmbda, p):
    """Convert from lambda to discrete number of sites in an overlap."""
    return math.floor(p.deltas / p.deltad * lmbda) + 1


def lambda_to_R(lmbda, p):
    """Convert from ring radius to lambda."""
    return p.Nsca / (2 * math.pi) * (p.Lf - p.deltas * lmbda)


def R_to_lambda(R, p):
    """Convert from ring radius to lambda."""
    return 1 / p.deltas * (p.Lf - 2 * math.pi * R / p.Nsca)


def calc_equilibrium_occupancy(p) -> float:
    """Calculate the equilibrium occupancy."""
    xi_d = p.cX / p.KdD
    xi_s = p.cX / p.KsD

    return xi_d / ((1 + xi_s) ** 2 + xi_d)
