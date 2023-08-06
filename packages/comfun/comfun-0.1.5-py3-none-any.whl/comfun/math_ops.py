#!/usr/bin/env python3

import logging
import sympy


def partial_derivative(der_var: str, remaining_parameters: str, formula: str):
    """

    :param der_var: variable to solve the partial derivative for
    :param remaining_parameters: Space-delimited symbols (e.g. "x y")
    :param formula:
    :return:
    """
    rempams = remaining_parameters.split(" ")
    logging.debug(f"{rempams=}")
    parameters = [der_var] + rempams  # Mundane list concat
    logging.debug(f"{parameters=}")
    d_var, symbols = sympy.symbols(parameters)
    f = sympy.parsing.sympy_parser.parse_expr(formula)
    der = sympy.diff(f, d_var)
    return der