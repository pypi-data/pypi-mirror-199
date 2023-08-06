import os
import tempfile
import regex
import numpy as np
from jinja2 import FileSystemLoader, Environment

# Import Brian2 modules
# from brian2.units.allunits import second
# from brian2.core.functions import Function
# from brian2.core.variables import Constant, ArrayVariable, AuxiliaryVariable
from brian2.groups.neurongroup import NeuronGroup, StateUpdater, Resetter, Thresholder, SubexpressionUpdater
from brian2.input.poissongroup import PoissonGroup
from brian2.input.spikegeneratorgroup import SpikeGeneratorGroup
from brian2.monitors.spikemonitor import SpikeMonitor
from brian2.monitors.ratemonitor import PopulationRateMonitor
from brian2.monitors.statemonitor import StateMonitor
from brian2.synapses.synapses import Synapses
# from brian2.units import second

from pprint import pprint


def build(
    self,
    hardware='CPU',
    debug=False,
    direct_call=True
):
    """
    Builds the Lava executables.

    It contains the following steps:

    *   includes some checks
    *   initializes file write
    *   renders the templates
    
    Parameters
    ----------
    hardware : `str`, optional
        The underlying hardware where the code is executed. Defaults to `CPU`.
    debug : `bool`, optional
        Whether to compile in debug mode. Defaults to ``False``.
    direct_call : `bool`, optional
        Whether this function was called directly. Is used internally to
        distinguish an automatic build due to the ``build_on_run`` option
        from a manual ``device.build`` call.

    Notes
    -----
    TODO change default hardware to `Loihi` as soon as Loihi is supported
    """
    
    # Log that the build method was called
    self.logger.debug("Building Lava device.")
    
    # Check if direct_call was used properly
    if self.build_on_run and direct_call:
        raise RuntimeError("You used set_device with build_on_run=True "
                           "(the default option), which will automatically "
                           "build the simulation at the first encountered "
                           "run call - do not call device.build manually "
                           "in this case. If you want to call it manually, "
                           "e.g. because you have multiple run calls, use "
                           "set_device with build_on_run=False.")
    
    # Check if network was already running before (FIXME necessarry?)
    if self.did_run:
        raise RuntimeError("The network has already been built and run "
                           "before. To build several simulations in "
                           "the same script, call \"device.reinit()\" "
                           "and \"device.activate()\". Note that you "
                           "will have to set build options (e.g. the "
                           "directory) and defaultclock.dt again.")
    
    # Prepare working directory
    self.prepare_directory()
    
    # TODO Unique network object names necessary?
    # See: https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L1238
    
    # Get dt in seconds without unit
    dt_ = self.defaultclock.dt_
    # Add 'dt' to 'lava_variables' to make it available to Lava
    self.lava_variables['_defaultclock_dt']['definition'] = f'np.array([{dt_}])'

    if hardware == 'CPU':
        # Render Lava templates
        for obj in self.lava_objects:
            process_rendered, process_model_rendered = self.render_templates(obj)
            self.logger.diagnostic(
                f"Compiling templates:\nProcess:\n{process_rendered}\nProcess Model:\n{process_model_rendered}"
            )
            # Write to file
            self.write_templates(process_rendered, process_model_rendered,obj.name)

        # Run Lava process
        self.run()
    else:
        raise NotImplementedError(f'Hardware {hardware} is not implemented (yet), the list of available hardware: {self.available_hardware}')


def render_templates(self, obj):
    """
    Renders Jinja templates based on Brian network objects that are used in the lava taplates.
    We call them `lava objects`.

    Parameters
    ----------
    obj : lava_object
        Lava related network object
    
    Returns
    -------
    process_rendered : `string`
        A rendered lava `process` template
    process_model_rendered : `string`
        A rendered lava `process model` template
    """
    
    # Extract variables and abstract code
    process_methods, process_model_methods = self.get_compiled_code(obj)
    
    # Log extracted lava code
    s = "Extracted process methods:\n"
    for item in process_methods:
        s += f'{item}\n'
    self.logger.diagnostic(s)

    s = "Extracted process model methods:\n"
    for item in process_model_methods:
        s += f'{item}\n'
    self.logger.diagnostic(s)

    # Get a list of ordered function calls to be implemented in
    # the 'run' and '__init__' function
    # TODO rename to 'process' and 'process_model' functions
    lava_init_function_calls, lava_multi_init, lava_run_function_calls = self.get_lava_function_calls(obj)

    # Get the port definitions for process and process model
    proc_ports, proc_model_ports = self.get_lava_ports_definitions(obj)
    
    # Get formatted variables for lava process
    proc_variables_init, proc_variables_lava = self.get_lava_proc_variables(obj, lava_init_function_calls)
    
    # Log extracted lava process variables
    s = "Extracted lava process variables:\n"
    for item in proc_variables_lava:
        s += f'{item}\n'
    self.logger.diagnostic(s)
    
    # Get formatted variables for lava process **model**
    lava_proc_model_variables = self.get_lava_proc_model_variables(obj)
    
    # Add the port initializations:
    proc_variables_lava = proc_ports + proc_variables_lava
    lava_proc_model_variables = proc_model_ports + lava_proc_model_variables

    # Log extracted lava process variables
    s = "Extracted lava process model variables:\n"
    for item in lava_proc_model_variables:
        s += f'{item}\n'
    self.logger.diagnostic(s)
    
    # Get jinja environment
    env = self.get_jinja_environment()

    # Load and render 'process'
    process_template = env.get_template('process.py.j2')
    process_rendered = process_template.render(
        variables_init=proc_variables_init,
        variables_lava=proc_variables_lava,
        multi_init_calls = lava_multi_init,
        init_methods=process_methods,
        required_imports=collect_required_imports(process_methods),
        name = obj.name
    )
    
    # Load and render 'process model'
    process_model_template = env.get_template('process_model.py.j2')
    process_model_rendered = process_model_template.render(
        methods=process_model_methods,
        run_functions=lava_run_function_calls,
        variables=lava_proc_model_variables,
        required_imports=collect_required_imports(process_model_methods),
        name = obj.name
    )
    
    return process_rendered, process_model_rendered


def get_jinja_environment(self):
    """
    Creates a Jinja environment.

    The environment contains a loader which includes a path to the templates.
    
    Returns
    -------
    env : Environment
        A jinja environment that contains a loader with a path to the Jinja template files
    """
    
    # Get path to templates
    template_path = os.path.join(self.package_root, 'templates')
    
    # Defined Jinja file system loader based on a path to the template files
    loader = FileSystemLoader(searchpath=template_path)
    
    # Return the environment, containing the file loader
    return Environment(
        loader=loader,
        trim_blocks=True,
        lstrip_blocks=True
    )


def get_compiled_code(self, obj):
    """
    Collects the compiled code for lava process and lava process model

    Parameters
    ----------
    obj : lava_object
        Lava related network object

    Returns
    -------
    process_methods : `string[]`
        Process methods to include into the `process`
    process_model_methods : `string[]`
        Process methods to include into the `process model`
    """
    
    # Define variables to collect lava code
    process_methods = ''
    process_model_methods = ''
        
    # Iterate over code objects
    for code_object in self.code_objects.values():
        if code_object.owner.name == obj.name:
            lava_code_tmp = None
            for block in ['before_run','run','after_run']:
                # Get compiled code for specific code object and block
                lava_code_tmp = code_object.compiled_code[block]
                
                # Add the code collected from the code objects to either
                # the Lava process or the Lava process model
                if lava_code_tmp is not None:
                    if code_object.template_name in self.init_template_functions:
                        process_methods += lava_code_tmp + '\n\n'
                    else:
                        process_model_methods += lava_code_tmp + '\n\n'

    return process_methods.splitlines(), process_model_methods.splitlines()


def collect_required_imports(abstract_code):
    """
    Search for functions in abstract code that require an import (e.g. random function)
    and return these imports as array.
    
    Parameters
    ----------
    abstract_code : 'string''
        The whole abstract code as string
    
    Returns
    -------
    required_imports : `string[]`
        Array of strings that contain required imports
    """
    
    # Define potential imports
    potential_imports = {
        'random': 'from random import random',
        'timestep': 'from brian2.core.functions import timestep',
        'LazyArange': 'from brian2.codegen.runtime.numpy_rt.numpy_rt import LazyArange',
        'ceil': 'from brian2.codegen.generators.numpy_generator import ceil_func as ceil',
        'floor': 'from brian2.codegen.generators.numpy_generator import floor_func as floor',
        'int': 'from brian2.codegen.generators.numpy_generator import int_func as int',
        'rand': 'from brian2.codegen.generators.numpy_generator import randn_func as rand',
        'randn': 'from brian2.codegen.generators.numpy_generator import randn_func as randn',
        'poisson': 'from brian2.codegen.generators.numpy_generator import poisson_func as poisson',
        'logical_not': 'from numpy import logical_not',
        'sign': 'from numpy import sign',
        'abs': 'from numpy import abs',
        'sqrt': 'from numpy import sqrt',
        'exp': 'from numpy import exp',
        'log': 'from numpy import log',
        'log10': 'from numpy import log10',
        'sin': 'from numpy import sin',
        'cos': 'from numpy import cos',
        'tan': 'from numpy import tan',
        'sinh': 'from numpy import sinh',
        'cosh': 'from numpy import cosh',
        'tanh': 'from numpy import tanh',
        'arcsin': 'from numpy import arcsin',
        'arccos': 'from numpy import arccos',
        'arctan': 'from numpy import arctan',
        
    }
    
    # Create empty array to collect required imports
    required_imports = []
    # Check if relevant function is in abstract code and if yes, add import
    for func, imp in potential_imports.items():
        for line in abstract_code:
            if f'{func}(' in line:
                required_imports.append(imp)
                # avoid multiple imports of the same function
                break
    
    return required_imports     

def get_lava_ports_definitions(self, obj):
    """
    TODO

    Parameters
    ----------
    obj : lava_object
        Lava related network object
    
    Returns
    -------
    proc_ports : `string[]`
        A list of code lines that define process ports
    proc_model_ports : `string[]`
        A list of code lines that define process model ports
    """

    proc_ports = []
    proc_model_ports = []
    # Use the information contained in the objects to format the input and output ports
    if isinstance(obj, NeuronGroup) or isinstance(obj,SpikeGeneratorGroup):
        # Add the spikes_out ports, NOTE that the name has to be compatible with the name used
        # in the SpikeMonitor.
        spike_port = obj.name + '_s_out'
        proc_ports.append(f"self.{spike_port} = OutPort(shape= ({obj.N},))")
        proc_model_ports.append(f"{spike_port}: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)")
        for var in self.lava_ports.values():
            if not obj.name == var['receiver']:
                continue
            portname = var['portname']
            proc_ports.append(f"self.{portname}_in = InPort(shape=(0,))",)
            port_type = 'float' if not 'idx' in portname else 'int,precision = 1'
            proc_model_ports.append(f"{portname}_in: PyInPort = LavaPyType(PyInPort.VEC_DENSE, {port_type})")   
            
    elif isinstance(obj,Synapses):
        # First receive the incoming spikes from the neurons
        for pathway in obj._pathways:
            # Note that in this case the port doesn't need the obj.name prefix since we don't read values from it!
            prepost = pathway.prepost
            proc_ports.append(f'self.s_in_{prepost} = InPort(shape=(0,))')
            proc_model_ports.append(f"s_in_{prepost}: PyInPort = LavaPyType(PyInPort.VEC_DENSE, bool, precision=1)")
        # Then make ports for synaptic transmission to neurons
        for var in self.lava_ports.values():
            for pathway in obj._pathways:
                if not var['pathway'] == pathway:
                    continue
                portname = var['portname']
                shape_var = self.get_array_name(obj.variables['_synaptic_pre'], prefix = 'self.init')
                proc_ports.append(f"self.{portname}_out = OutPort(shape = {shape_var}.shape)")
                port_type = 'float' if not 'idx' in portname else 'int,precision = 1'
                proc_model_ports.append(f"{portname}_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, {port_type})")

    # If there are aliases of the same variable, make sure to initialize them only once
    proc_ports = list(set(proc_ports))
    # Add a return just to make the code slightly cleaner
    proc_ports[-1] += '\n'
    proc_model_ports = list(set(proc_model_ports))
    proc_model_ports[-1] += '\n'

    return proc_ports, proc_model_ports


def get_lava_proc_variables(self, obj, lava_init_function_calls):
    """
    Takes variable name/value pairs and generates a list of variables
    for the lava process

    Parameters
    ----------
    obj : lava_object
        Lava related network object
    lava_init_function_calls : `string[]`
        A list of strings containing function calls for the process
    
    Returns
    -------
    formatted_variables_init : `string[]`
        A list of code lines that contain variable declarations for the `process`
    formatted_variables_lava : `string[]`
        A list of code lines that contain variable declarations for the `process model`
    """
    
    # Store formatted init variables for a Lava process
    # This contains all variables again, but initialized as plain numpy arrays
    formatted_variables_init = []
    formatted_variables_lava = []

    for name, var in self.lava_variables.items():
        if not var['owner'] == obj.name and not var['owner'] == obj.clock.name:
            continue
        elif var['owner'] == obj.name:
            init_var_name = f'self.init{name}'
            numpy_definition = var["definition"]

            # Statement for the definition of an array variable in Lava
            formatted_variables_init.append(f'{init_var_name} = {numpy_definition}')
            
            # Check if Brian provides us with an init function for the variable,
            # that contains instructions to set user-defined initial values
            init_func = None
            if name in lava_init_function_calls:
                init_func = lava_init_function_calls[name]
                exp = f'Var(shape={var["shape"]}, init={init_func})'
            # Otherwise init with init variable that contains a plain numpy definition
            else:
                # Here I look at the shape of the init variable instead, it's useful if at the beginning
                # the shape is set to (0,) in brian due to the fact that they will resize this array.
                # This is because the lava shape of a variable doesn't get update according to the shape of its
                # init value.
                exp = f'Var(shape={init_var_name}.shape, init={init_var_name})'
        # NOTE: implementing multiple clocks will require checking on each obj.clock.name
        elif var['owner'] == obj.clock.name:
            dt = obj.clock.dt_
            exp = f'Var(shape= (1,), init = np.array([{dt}]))'
        
        # Statement for the definition of an array variable in Lava
        formatted_variables_lava.append(f'self.{name} = {exp}')

    return formatted_variables_init, formatted_variables_lava


def get_lava_proc_model_variables(self, obj):
    """
    Takes variable name/value pairs and generates a list of variables for the lava process model.

    Parameters
    ----------
    obj : lava_object
        Lava related network object
    
    Returns
    -------
    formatted_variables : str[]
        A list of code lines that contain variable declarations
    """
    
    # Init variable to store formatted variables for a Lava process model
    formatted_variables = []
    
    # Then the variables themselves
    for name, var in self.lava_variables.items():
        if var['owner'] == obj.name or var['owner'] == obj.clock.name:
            # Check if array or not
            value_type_arr = 'np.ndarray' if var["size"] > 1 else var["type"]

            # Format the expression to what a Lava process expects
            exp = f'LavaPyType({value_type_arr}, {var["type"]})'

            # Statement for the definition of an array variable in Lava
            formatted_variables.append(f'{name}: {value_type_arr} = {exp}')

            # Statement for the definition of an actual variable
            #formatted_variables.append(f'{var["name"]}: {value_type_arr} = {exp}')
        
    return formatted_variables


def get_lava_function_calls(self, obj):
    """
    Given the code objects we return an ordered list of function calls that should
    happend within our code. The ordering should be made more customizable

    Parameters
    ----------
    obj : lava_object
        Lava related network object

    Returns
    -------
    init_calls : `string[]`
        A list of code that describes methods for the `process`
    run_calls : `string[]`
        A list of code that describes methods for the `process model`
    """
    init_calls_lists = {}
    init_calls = {}
    run_calls = []
    multi_var_init_calls = []

    # Collect code objects for process
    code_objects = [c_o for c_o in list(self.code_objects.values()) if c_o.owner.name == obj.name]

    # Iterate over all code blocks and code objects
    # NOTE: The after_run code blocks are not really used at any point yet. 
    # FIXME: I take them out for now, because their behavior should be implemented differently!
    for block in ['_before_run()', '_run()']:
        for code_obj in code_objects:
            # If the codeobject is not empty, assign function names to related lists
            if code_obj.compiled_code[block[1:-2]] is not None:
                function_name = f'self.{code_obj.name}{block}'
                # Currently added synapses_create_array to the init functions because I believe we should only call it once.
                #if 'group_variable_set_conditional' in code_obj.name or block == '_before_run()' or 'synapses_create_array' in code_obj.name: 
                # # TODO: Here we might have to make sure that the 'group_...' gets added to index 0
                #    init_calls.append(function_name)
                # These functions are added to the lava process and initialize variables
                if code_obj.template_name in self.init_template_functions:
                    # Get variable that will be initialized in process
                    var_name = self.init_variables[code_obj.name]
                    # TODO: this can for sure be done more cleanly, but for now it suffices, check synapses.py to see why this works
                    if isinstance(var_name,str):
                        # If variable was not already added to list, just add it    
                        if var_name not in init_calls_lists:
                            init_calls_lists[var_name] = [function_name]
                        # If variable was already added to list, append it to the existing item
                        else:
                            init_calls_lists[var_name].append(function_name)
                    else:
                        multi_var_init_calls.append(function_name)
                # These functions handle the simulation and are part of the lava process model
                else:
                    run_calls.append(function_name)
    run_calls = schedule_sort(run_calls, obj)

    # Postprocess init calls
    for key, values in init_calls_lists.items():
        # If we have only one init function for the variable, just take it
        if len(values) == 1:
            init_calls[key] = values[0]
        # If we have two or more init functions for the variable,
        # we need to construct a lambda function that calls all init functions
        else:
            # Starting string definition for lambda function that calls all functions
            st = '(lambda: ['
            suffix = '])()[-1]'
            # Iteratively add all function calls as string
            for i, v in enumerate(values):
                st += f'{v}'
                if (i+1) < len(values):
                    st += ', '
            # Add suffix and add to init calls
            st += suffix
            init_calls[key] = st

    # If in any of our code objects there's a time variable (probably always)
    # Add a line to update at each time step
    time_update_set = False
    timestep_update_set = False
    for code_obj in code_objects:
        code_obj_varnames = code_obj.variables.keys()
        if 't' in code_obj_varnames and not time_update_set:
            # TODO: this has to be made more generalizable to multiple clocks
            run_calls.append('self._defaultclock_t += self._defaultclock_dt')
            time_update_set = True
        if 't_in_timesteps' in code_obj_varnames and not timestep_update_set:
            run_calls.append('self._defaultclock_timestep += 1')
            timestep_update_set = True

    return init_calls, multi_var_init_calls, run_calls


def schedule_sort(func_list, obj):
    """
    TODO

    Parameters
    ----------
    obj : lava_object
        Lava related network object

    Returns
    -------
    ordered_list
        A list containing the schedule, i.e the order of exectutions for code objects
    """

    from itertools import chain
    from brian2 import CodeRunner
    schedule = {
        'start': [],
        'groups': [],
        'thresholds': [],
        'synapses': [],
        'resets': [],
        'end': []
    }
    for func_call in func_list:
        if not isinstance(obj,CodeRunner):
            code_runner = [item for item in obj.contained_objects if item.name in func_call]
        else:
            # The only supported object which is itself a CodeRunner is the SpikeGeneratorGroup
            assert type(obj) == SpikeGeneratorGroup
            code_runner = [obj]
        
        #If the function doesn't correspond to the contained objects then it must be
        # the activation_processing code object, which doesn't have a corresponding CodeRunner object.
        # NOTE: This might be changed in future updates
        if not len(code_runner):
            # We want to receive the activations and update the neuron at the start of the timestep.
            # NOTE: The various run_ functions from lava might prove useful here in the future.
            assert 'activation_processing' in func_call
            schedule['synapses'].insert(0, func_call)
            continue

        if not len(code_runner) == 1:
            raise ValueError(f"""More than one CodeRunner corresponding to the same code_object. 
            Try restarting the simulation. If the bug persists please report it to us.
            CodeRunners: {code_runner}""")
        code_runner = code_runner[0]
        schedule[code_runner.when].insert(code_runner.order,func_call)
    ordered_list = []
    for when in schedule:
        ordered_list = list(chain(ordered_list, schedule[when]))

    return ordered_list
