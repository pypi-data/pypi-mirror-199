from brian2.synapses.synapses import SynapticPathway
from brian2.core.functions import Function
from brian2.core.variables import ArrayVariable


def code_object(
        self,
        owner,
        name,
        abstract_code,
        variables,
        template_name,
        variable_indices,
        codeobj_class=None,
        template_kwds=None,
        override_conditional_write=None,
        compiler_kwds=None
    ):
    """
    Defines a code object.

    Parameters
    ----------
    TODO

    Returns
    -------
    codeobj
    """
    
    # Log when a code object is added
    self.logger.diagnostic(f'Add code_object {name}')
    self.logger.diagnostic(f'Variables gotten from previous steps, {[varname for varname,var in list(variables.items())]}')

    # Init template keywords if none were given
    if template_kwds is None:
        template_kwds = dict()

    # FIXME: This will need to be fixed because it can cause problems when we generate multiple objects of the same kind
    template_kwds['name'] = name[:-1] if name[-1] == '*' else name

    # In case a variable is set with initial values, we extract the related variable name
    # The variable name is extracted from the abstract code line (before the equal sign)
    # The name is used to get a unique name for the method that initializes the variable
    if template_name in self.init_template_functions:

        # Find variable to initialize
        lava_variable = None
        for v in variables.values():
            if hasattr(v, 'owner'):
                lava_var_name = self.get_array_name(v, prefix='')
                if lava_var_name in self.init_variables.values():
                    lava_variable = v
                    break

        # TODO raise exception if lava_variable was not found (is still None)

        lava_array_name = self.get_array_name(v, prefix='self.init')
        # For now let's separate the synapses case from the variableview one.
        # TODO: It should be possible to unify the procedure for both, so we should do that..
        if not 'synapses' in name:
            # Add statement to template keywords
            template_kwds['return_statement'] = f'return np.array({lava_array_name})'

            # We take the method that was lastly added from the variableview
            # Francesco: here we can't use simply 'name' because this conflicts with the 
            # arguments to the code_object() function
            method_name = self.last_set_variable_method_name
            # Add method name to template keywords
            template_kwds['name'] = method_name

        # With this we bypass the instructions in the brian base device:
        # (brian2.devices.device -> 328-336)
        # This is because for initialization variables we want to use a different
        # naming convention.
        # Note that this requires renaming the {{variables}} in the template to add the '_init' suffix
        for varname, var in variables.items():
            if isinstance(var, ArrayVariable):
                pointer_name = self.get_array_name(var, prefix = 'self.init')
                if var.scalar:
                    pointer_name += "[0]"
                template_kwds[varname + '_init'] = pointer_name
                if hasattr(var, "resize"):
                    dyn_array_name = self.get_array_name(var, prefix = 'self.init', access_data=False)
                    template_kwds[f"_dynamic_{varname}_init"] = dyn_array_name
        # TODO: This functionality could be used in the other generators (for variable initializations)

    # I think this has to be managed here, because the CodeRunner for synaptic Pathways gets 
    # created during synapses initialization, and thus is out of our control until this point.
    if template_name == 'synapses':
        pathway = template_kwds['pathway']
        self.determine_lava_ports(pathway, {v:var for v,var in variables.items() if not isinstance(var,Function)})
        # Here we only change the name, to make it easier for debugging
        template_kwds_neuron = template_kwds.copy()
        codeobj_name = pathway.target.name +'_'+ owner.name + '_' + pathway.prepost + '_' + 'activation_processing'
        template_kwds_neuron['name'] = codeobj_name
        # Here we substitute the codeobject with one which belongs to the correct NeuronGroup
        codeobj = self.super.code_object(
            pathway.target,
            codeobj_name,
            abstract_code,
            variables,
            'activation_processing',
            variable_indices,
            codeobj_class=codeobj_class,
            template_kwds=template_kwds_neuron,
            override_conditional_write=override_conditional_write,
            compiler_kwds=compiler_kwds
        )
        self.code_objects[codeobj.name] = codeobj
        # Make a different abstract code for synapses
        # FIXME: this is not very clean and should probably be handled differently
        code = ''
        abstract_code = {None : code}
    # Call code_object method from Brian2 parent device
    codeobj = self.super.code_object(
        owner,
        name,
        abstract_code,
        variables,
        template_name,
        variable_indices,
        codeobj_class=codeobj_class,
        template_kwds=template_kwds,
        override_conditional_write=override_conditional_write,
        compiler_kwds=compiler_kwds
    )

    # Store code objects in device
    self.code_objects[codeobj.name] = codeobj
    
    return codeobj


def determine_lava_ports(self, pathway, variables):
    """
    Extracts the synaptic variables to be sent to the neurongroups and determine the Lava ports required for that.

    Parameters
    ----------
    pathway
        Synaptic pathways.
    variables
        All variables that are not a function.
    """

    synaptic_vars = []
    # TODO: this is probably needed in case the update only requires synaptic variables,
    # then you wouldn't need to send them to the neuronGroup. But for now let's just make
    # the easiest scenario
    for varname, var in variables.items():
        if not 'synapses' in var.owner.name:
            continue
        synaptic_vars.append(varname)
    # At the first iteration of this function we create the corresponding dictionary
    if not hasattr(self, 'lava_ports'):
        self.lava_ports = {}
    # Var names are kept in their original form, but the ports are separated depending on the pathway
    for varname in synaptic_vars:
        portname = pathway.synapses.name +'_'+ pathway.prepost +'_'+ varname
        self.lava_ports[portname] = {
            'varname': varname,
            'portname': portname,
            'pathway': pathway,
            'sender' : pathway.source.name,
            'receiver': pathway.target.name,
            'shape': None
        }
    
    




