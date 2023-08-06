import numpy as np

# from brian2.core.base import BrianObjectException
# from brian2.core.preferences import prefs, BrianPreference
from brian2.core.variables import DynamicArrayVariable, ArrayVariable, AuxiliaryVariable, Subexpression
from brian2.core.functions import Function

from brian2.codegen.codeobject import CodeObject, constant_or_scalar, check_compiler_kwds
from brian2.codegen.targets import codegen_targets

from brian2lava.codegen.lava_generator import LavaCodeGenerator
from brian2lava.codegen.templater import Templater


class LavaCodeObject(CodeObject):
    """
    Class of code objects that generate Lava compatible code
    """


    templater = Templater('brian2lava.codegen','.py_', env_globals={'constant_or_scalar': constant_or_scalar})
    generator_class = LavaCodeGenerator
    class_name = 'lava'


    def __init__(
            self, owner, code, variables, variable_indices,
            template_name, template_source, compiler_kwds,
            name='lava_code_object*'
        ):
        check_compiler_kwds(compiler_kwds, [], 'lava')

        from brian2.devices.device import get_device
        self.device = get_device()
        self.namespace = {
            '_owner': owner,
            'logical_not': np.logical_not  # TODO: This should maybe go somewhere else
        }
        CodeObject.__init__(
            self, owner, code, variables, variable_indices,
            template_name, template_source,
            compiler_kwds=compiler_kwds, name=name
        )
        self.variables_to_namespace()


    @classmethod
    def is_available(cls):
        """
        Checks if the given backend is available

        Parameters
        ----------
        cls
            A CodeObject derived class

        Returns
        -------
        `bool`
            Indicates if the given backend is avialable or not
        """

        # TODO
        # For all hardwares perhaps check if Lava is installed?
        # For Loihi, we need to check if Loihi is actually available
        # For now, just return true
        return True


    def variables_to_namespace(self):
        """
        Adds variables to the Brian namespace.

        Notes
        -----
        Variables can refer to values that are either constant (e.g. dt) or change every timestep (e.g. t).
        We add the values of the constant variables here and add the names of non-constant variables to a list.
        """

        # A list containing tuples of name and a function giving the value
        self.nonconstant_values = []

        for name, var in self.variables.items():
            if isinstance(var, (AuxiliaryVariable, Subexpression)):
                continue

            try:
                if not hasattr(var, 'get_value'):
                    raise TypeError()
                value = var.get_value()
            except TypeError:
                # Either a dummy Variable without a value or a Function object
                if isinstance(var, Function):
                    impl = var.implementations[self.__class__].get_code(self.owner)
                    self.namespace[name] = impl
                else:
                    self.namespace[name] = var
                continue

            if isinstance(var, ArrayVariable):
                self.namespace[self.generator_class.get_array_name(var)] = value
                if var.scalar and var.constant:
                    self.namespace[name] = value[0]
            else:
                self.namespace[name] = value

            if isinstance(var, DynamicArrayVariable):
                dyn_array_name = self.generator_class.get_array_name(var, access_data=False)
                self.namespace[dyn_array_name] = self.device.get_value(var, access_data=False)

            # Also provide the Variable object itself in the namespace (can be
            # necessary for resize operations, for example)
            self.namespace[f"_var_{name}"] = var

            # There is one type of objects that we have to inject into the
            # namespace with their current value at each time step: dynamic
            # arrays that change in size during runs (i.e. not synapses but
            # e.g. the structures used in monitors)
            if (isinstance(var, DynamicArrayVariable) and var.needs_reference_update):
                self.nonconstant_values.append((
                    self.generator_class.get_array_name(var, self.variables),
                    var.get_value
                ))


    def update_namespace(self):
        """
        Updates variables from the code object in the Brian namespace.
        """

        # Update the values of the non-constant values in the namespace
        for name, func in self.nonconstant_values:
            self.namespace[name] = func()


    def compile_block(self, block):
        """
        Compiles a block of code.

        Parameters
        ----------
        block
            A block of code

        Returns
        -------
        `str`
            Compiled code
        """

        code = getattr(self.code, block, '').strip()
        if not code or 'EMPTY_CODE_BLOCK' in code:
            return None
        # TODO What does python's compile return?
        return code


    def run(self):
        """
        Runs the code.

        Notes
        -----
        The execution of compiled code is deligated to the device.
        """

        pass


    def run_block(self, block):
        """
        Runs a block of code.

        Parameters
        ----------
        block
            A block of code

        Notes
        -----
        The execution of compiled code is deligated to the device.
        """

        pass


codegen_targets.add(LavaCodeObject)
