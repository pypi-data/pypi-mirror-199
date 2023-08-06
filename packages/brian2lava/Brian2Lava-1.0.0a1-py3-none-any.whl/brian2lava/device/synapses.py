from collections import defaultdict
from collections.abc import Sequence, MutableMapping, Mapping
import functools
import weakref
import re
import numbers

import numpy as np

from brian2.core.base import weakproxy_with_fallback
from brian2.core.base import device_override
from brian2.core.namespace import get_local_namespace
from brian2.core.variables import (DynamicArrayVariable, Variables)
from brian2.codegen.codeobject import create_runner_codeobj
from brian2.codegen.translation import get_identifiers_recursively
from brian2.devices.device import get_device
from brian2.equations.equations import (Equations,
                                        DIFFERENTIAL_EQUATION, SUBEXPRESSION,
                                        PARAMETER,
                                        check_subexpressions, EquationError)
from brian2.groups.group import Group, CodeRunner, get_dtype
from brian2.groups.neurongroup import (extract_constant_subexpressions,
                                       SubexpressionUpdater,
                                       check_identifier_pre_post)
from brian2.parsing.expressions import is_boolean_expression, parse_expression_dimensions
from brian2.stateupdaters.base import (StateUpdateMethod,
                                       UnsupportedEquationsException)
from brian2.stateupdaters.exact import linear, independent
from brian2.units.fundamentalunits import (Quantity, DIMENSIONLESS, DimensionMismatchError,
                                           fail_for_dimension_mismatch)
from brian2.units.allunits import second
from brian2.utils.logger import get_logger
from brian2.utils.stringtools import get_identifiers, word_substitute
from brian2.utils.arrays import calc_repeats
from brian2.core.spikesource import SpikeSource
from brian2.synapses.parse_synaptic_generator_syntax import parse_synapse_generator
from brian2.parsing.bast import brian_ast
from brian2.parsing.rendering import NodeRenderer
MAX_SYNAPSES = 2147483647


def spike_queue(self, source_start, source_end):
    """
    TODO

    Parameters
    ----------
    source_start
        TODO
    source_end
        TODO
    
    Returns
    -------
    `SpikeQueue`
        TODO
    """

    # TODO REMOVE! In brian2lava there is no need for a spike queue.
    # Use the C++ version of the SpikeQueue when available
    try:
        from brian2.synapses.cythonspikequeue import SpikeQueue
        self.logger.diagnostic('Using the C++ SpikeQueue', once=True)
    except ImportError:
        from brian2.synapses.spikequeue import SpikeQueue
        self.logger.diagnostic('Using the Python SpikeQueue', once=True)

    return SpikeQueue(source_start=source_start, source_end=source_end)


def synapses_connect(
        self, synapses, condition=None, i=None, j=None, p=1., n=1,
        skip_if_invalid=False, namespace=None, level=0
    ):
    """
    Connects synapses.

    This method overwrites the `connect` function from Brian.

    Parameters
    ----------
    synapses : `Synapses`
        Equals the `self` of the original `connect` function from Brian,
        which is an instance of the `Synapses` class.
    condition : str, bool, optional
        A boolean or string expression that evaluates to a boolean.
        The expression can depend on indices ``i`` and ``j`` and on
        pre- and post-synaptic variables. Can be combined with
        arguments ``n``, and ``p`` but not ``i`` or ``j``.
    i : int, ndarray of int, str, optional
        The presynaptic neuron indices  It can be an index or array of
        indices if combined with the ``j`` argument, or it can be a string
        generator expression.
    j : int, ndarray of int, str, optional
        The postsynaptic neuron indices. It can be an index or array of
        indices if combined with the ``i`` argument, or it can be a string
        generator expression.
    p : float, str, optional
        The probability to create ``n`` synapses wherever the ``condition``
        evaluates to true. Cannot be used with generator syntax for ``j``.
    n : int, str, optional
        The number of synapses to create per pre/post connection pair.
        Defaults to 1.
    skip_if_invalid : bool, optional
        If set to True, rather than raising an error if you try to
        create an invalid/out of range pair (i, j) it will just
        quietly skip those synapses.
    namespace : dict-like, optional
        A namespace that will be used in addition to the group-specific
        namespaces (if defined). If not specified, the locals
        and globals around the run function will be used.
    level : int, optional
        How deep to go up the stack frame to look for the locals/global
        (see ``namespace`` argument).
    """

    # Check types
    synapses._verify_connect_argument_types(condition, i, j, n, p)

    synapses._connect_called = True

    # Get namespace information
    if namespace is None:
        namespace = get_local_namespace(level=level + 2)

    try:  # wrap everything to catch IndexError
        # which connection case are we in?
        # 1: Connection condition
        if condition is None and i is None and j is None:
            condition = True
        if condition is not None:
            if i is not None or j is not None:
                raise ValueError("Cannot combine condition with i or j "
                                    "arguments")
            if condition is False or condition == 'False':
                # Nothing to do
                return
            j = synapses._condition_to_generator_expression(condition, p, namespace)
            print("Using synapses generator")
            synapses._add_synapses_generator(j, n, skip_if_invalid=skip_if_invalid,
                                            namespace=namespace, level=level + 2,
                                            over_presynaptic=True)
        # 2: connection indices
        elif (i is not None and j is not None) and not (isinstance(i, str) or isinstance(j, str)):
            if skip_if_invalid:
                raise ValueError("Can only use skip_if_invalid with string "
                                    "syntax")
            i, j, n = synapses._verify_connect_array_arguments(i, j, n)
            synapses._add_synapses_from_arrays(i, j, n, p, namespace=namespace)
        # 3: Generator expression over post-synaptic cells (i='...')
        elif isinstance(i, str):
            i = synapses._finalize_generator_expression(i, j, p, 'i', 'j')
            synapses._add_synapses_generator(i, n, skip_if_invalid=skip_if_invalid,
                                            namespace=namespace, level=level + 2,
                                            over_presynaptic=False)
        # 4: Generator expression over pre-synaptic cells (i='...')
        elif isinstance(j, str):
            j = synapses._finalize_generator_expression(j, i, p, 'j', 'i')
            synapses._add_synapses_generator(j, n, skip_if_invalid=skip_if_invalid,
                                            namespace=namespace, level=level + 2,
                                            over_presynaptic=True)
        else:
            raise ValueError("Must specify at least one of condition, i or "
                                "j arguments")
    except IndexError as e:
        raise IndexError("Tried to create synapse indices outside valid "
                            "range. Original error message: " + str(e))
    # Do some refactoring of the synapses code to adapt it to Lava API:
    # FIXME: Probably this will be useless, but I'll wait before deleting it since it does no harm here for now.
    self.add_lava_synapses_generator(synapses)


def add_lava_synapses_generator(self, synapses):
    """
    A helper function to correctly tell lava which synaptic variables will be
    initialized through this generator codeobject.

    Parameters
    ----------
    synapses : `Synapses`
        An instance of the `Synapses` class

    Notes
    -----
    At the moment I'm using a trick, which just adds a random int, used in build() to determine that this codeobject
    initializes multiple variables. In the future this should be changed: either expanded if the variables themselves
    are needed, or replaced by something more elegant.
    """
    # Extract the generator codeobj from the device's code_objects
    # TODO: This is not clean and should be handled in a different way.
    generator_codeobj = [self.code_objects[name] for name in self.code_objects if ('synapses_create' in name and self.code_objects[name].owner == synapses)][-1]
    self.init_variables[generator_codeobj.name] = 123
