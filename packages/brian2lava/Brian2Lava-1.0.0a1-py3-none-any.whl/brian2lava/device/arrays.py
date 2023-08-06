import numpy as np

from brian2.memory.dynamicarray import DynamicArray, DynamicArray1D
from brian2.core.variables import ArrayVariable, DynamicArrayVariable

from brian2.monitors.spikemonitor import SpikeMonitor
from brian2.monitors.statemonitor import StateMonitor

def get_value(self, var, access_data=True):
    """
    Get a value from an array.
    Returning a value from the device arrays depends on the type of array,
    which can either be a static array (ArrayVariable) or a dynamic array (DynamicArrayVariable).

    Parameters
    ----------
    var : `ArrayVariable`
        The array to get
    access_data : `bool`
        A flag that indicates if it is intended to access only the data of the dynamic array (True)
        or the whole dynamic array (False)

    Returns
    -------
    `any`
        Values of the array variable as list
    """

    # Log that a value was requested from arrays
    self.logger.diagnostic(f'get_value {var.name}')

    return self.arrays[var]


def get_var_by_lava_name(self, lava_var_name):
    """
    Get an array variable from array by lava variable name

    Parameters
    ----------
    lava_var_name : `string`
        The name of the lava variable

    Returns
    -------
    `ArrayVariable`
        An array variable
    """

    # Iterate over all arrays
    for var, values in self.arrays.items():
        # Check if variable is not DynamicArrayVariable, since we don't want to get monitor variables
        is_no_monitor = not isinstance(var, DynamicArrayVariable)
        # Check if name of variable matches given name
        is_name_match = self.get_lava_var_name(var) == lava_var_name

        # If both conditions match, break loop and return variable
        if is_no_monitor and is_name_match:
            return var


def get_lava_var_name(self, var):
    """
    Get a lava variable name based on an array variable.

    Parameters
    ----------
    var : `ArrayVariable`
        An array variable

    Returns
    -------
    `string`
        The corresponding lava variable name

    Notes
    -----
    TODO This can possibly be hamrmonized with `get_array_name`.
    """

    if isinstance(var.owner, StateMonitor):
        source_name = 'defaultclock' if var.name == 't' else var.owner.source.name
        #source_name = var.owner.name
        return f'_{source_name}_{var.name}'
    elif isinstance(var.owner, SpikeMonitor):
        lava_var_name = ''
        if var.name == 't': lava_var_name = '_defaultclock_t'
        if var.name == 'i': lava_var_name = var.owner.source.name +'_s_out'
        return lava_var_name
    else:
        return f'_{var.owner.name}_{var.name}'


def get_array_name(self, var, access_data=True, prefix='self.'):
    """
    Gets the name of an array variable.

    Parameters
    ----------
    var : `ArrayVariable`
        The array to get.
    access_data : `bool`
        A flag that indicates if it is intended to access only the data of the dynamic array (True)
        or the whole dynamic array (False)
    prefix : `string`
        A string that is added as a prefix to the array name
        Default is 'self.', in case of 'None', no prefix is added

    Returns
    -------
    `string`
        The corresponding variable name as it is used in Brian

    Notes
    -----
    TODO This can possibly be hamrmonized with `get_lava_var_name`.
    """
    
    # The name of the array is part of the owner attribute
    # The owner is a `Nameable`, e.g. `NeuronGroup` or `Synapses`
    # If no owner name is available, 'temporary' is assigned
    owner_name = getattr(var.owner, 'name', 'temporary')

    # Redefine prefix to empty string if it was set to 'None'
    if prefix is None:
        prefix = ''
    
    return f'{prefix}_{owner_name}_{var.name}'


def get_monitor_type_name(owner):
    """
    Get monitor type name, i.e. spike monitor or state monitor

    Parameters
    ----------
    owner : `StateMonitor` or `SpikeMonitor`
        The owner of a group

    Returns
    -------
    `string`
        The corresponding monitor type as string
    """

    # Init monitor type variables
    monitor_type_name = ''

    # Check instance of owner and define types
    if isinstance(owner, StateMonitor):
        monitor_type_name = 'state'
    elif isinstance(owner, SpikeMonitor):
        monitor_type_name = 'spike'
    else:
        raise Exception('Unknown owner instance. Owner instance has to be StateMonitor or SpikeMonitor.')

    return monitor_type_name


def add_array(self, var):
    """
    Add a variable array to the `arrays` list of the device.
    It can either be added directly or as a `DynamicArrayVariable` object.
    The `DynamicArrayVariable` can dynamically be extended (in contrast to a static array).

    We separate between monitors and all other owner types of the variable to add.
    Monitors are added to the `lava_monitors` list. All other variable types are added to `lava_variable_names`.

    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to add
    """

    # NOTE only for Loihi hardware, on CPU this is not necessary
    # Only add array if owner is of class SpikeMonitor or StateMonitor
    #if not isinstance(var.owner, (SpikeMonitor, StateMonitor)):
    #    return

    # Log that a value was added to arrays
    self.logger.diagnostic(f'add_array {var.name}')

    # Create a static numpy array
    arr = np.empty(var.size, dtype=var.dtype)

    # Add array to device arrays
    self.arrays[var] = arr

    if isinstance(var.owner, (SpikeMonitor, StateMonitor)):
        # NOTE Currently only dynamic array variables of a monitor (like v, t, etc.) are added
        #      Constant values like N or __indices are currently ignored
        if isinstance(var, DynamicArrayVariable):

            # Get monitor type name from owner ('state' or 'spike')
            monitor_type_name = get_monitor_type_name(var.owner)

            # Define monitor name and lava variable name
            monitor_name = f'_{monitor_type_name}_{var.owner.name}_{var.name}'
            lava_var_name = self.get_lava_var_name(var)

            # Collect lava variable names that shall be monitored by lava
            # NOTE Only add variable name if it's not already in the list
            #      Variable names can occure in multiple monitors, e.g. time
            if lava_var_name not in self.lava_variables_to_monitor:
                self.lava_variables_to_monitor.append(lava_var_name)
            # Define monitor
            self.lava_monitors[monitor_name] = {
                'name' : monitor_name, # The name of this monitor, mainly for debugging
                'source': var.owner.source.name,
                'var': var,  # Brian variable
                'lava_var_name': lava_var_name,  # The variable name used in Lava
                'type': self.monitor_types[monitor_type_name],  # The monitor type ('state' or 'spike')
                'lava_monitor': None  # The Lava monitor, instance is added later during 'run'
            }
    else:
        # Add the definition of a numpy array as string for lava
        var_definition = f'np.empty({var.size}, dtype=np.{arr.dtype.name})'

        # TODO this can be done better probably
        dtype = arr.dtype.name        
        value_type = dtype.replace('32', '')
        value_type = value_type.replace('64', '')

        # TODO is the key unique?
        # See also: https://github.com/brian-team/brian2/pull/304
        name = f'_{var.owner.name}_{var.name}'
        self.lava_variables[name] = {
            'name': var.name,
            'owner': var.owner.name,
            'definition': var_definition,
            'size': var.size,
            'shape': np.shape(arr),
            'type': value_type,
            'dtype': arr.dtype.name
        }

        # NOTE information from this dict can also be obtained from self.lava_variables
        #      directly, but it's a bit complicated, for now we can leave it as a kind of cache
        self.lava_variable_names[var.name] = name


def init_with_zeros(self, var, dtype):
    """
    Initialize an array with zeros and adds it to the `arrays` list.

    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to initialize with zeros
    dtype : `dtype`
        The data type to use for the array
    """

    # Redefine variable definition for Lava variables
    name = f'_{var.owner.name}_{var.name}'
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]
        lv['definition'] = f'np.zeros({lv["size"]}, dtype=np.{lv["dtype"]})'
    
    # Log that an empty array was initialized
    self.logger.diagnostic(f'init_with_zeros {var.name}')
    
    self.arrays[var][:] = 0


def init_with_arange(self, var, start, dtype):
    """
    Initializes an array using the numpy arange function and adds it to the `arrays` list.
    The `start` value defines the start of the range, the length is given by the length of the `var` array.
    
    Parameters
    ----------
    var : `ArrayVariable`
        The array to initialize is based on the length of this `var` array
    start : `int`
        Start value of the range
    dtype : `dtype`
        The data type to use for the array
    """

    # Redefine variable definition for Lava variables
    name = f'_{var.owner.name}_{var.name}'
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]
        lv['definition'] = f'np.arange({start}, {lv["size"]+start}, dtype=np.{lv["dtype"]})'
    
    # Log that an array was created based on numpy arange
    self.logger.diagnostic(f'init_with_arange, arange from {start} to {var.get_len()+start}')
    
    self.arrays[var][:] = np.arange(start, stop=var.get_len()+start, dtype=dtype)


def fill_with_array(self, var, arr):
    """
    Fill array vatiable `var` with the values given in an array `arr` and add it to the `arrays` list.
    
    Parameters
    ----------
    var : `ArrayVariable`
        The array variable to fill
    arr : `ndarray`
        The array values that should be copied to `var`
    """

    arr = np.asarray(arr)
    # Redefine variable definition for Lava variables
    name = f'_{var.owner.name}_{var.name}'
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]

        # Check if 'arr' is given as scalar
        is_scalar = not bool(len(np.shape(arr)))
        
        # If 'arr' is scalar and size is 1, add a simple array
        if is_scalar and lv['size'] == 1:
            lv['definition'] = f'np.array([{arr}], dtype=np.{lv["dtype"]})'
        # If 'arr' is scalar and size > 1, add an array that repeats the value accordingly
        elif is_scalar and lv['size'] > 1:
            lv['definition'] = f'np.array(np.repeat({arr}, {lv["size"]}), dtype=np.{lv["dtype"]})'
        # If 'arr' is actually an array, it's just transformed to a string definition
        else:
            arr_str = np.array2string(np.array(arr), separator=', ')
            lv['definition'] = f'np.array({arr_str}, dtype=np.{lv["dtype"]})'

    # Log that an array was filled with given values
    self.logger.diagnostic(f'fill_with_array, add {arr} to {var.name}')
    
    # Set array value
    self.arrays[var][:] = arr

def resize(self, var, new_size):
    """
    Method called most times a DynamicArray variable is created. Updates the size of a DynamicArray.
    """
    # First resize it in our array-cache
    self.arrays[var].resize(new_size)

    # Change the size of the variable in our variable dictionary
    # We also make sure to update the default definition in case the variable
    # is not initialized with a 'fill_with' method afterwards (in most cases it is).
    # This is probably redundant but ensures no bugs come up later on.
    name = f'_{var.owner.name}_{var.name}'
    if name in self.lava_variables.keys():
        lv = self.lava_variables[name]
        lv["size"] = new_size
        if 'np.empty' in lv["definition"]:
            lv["definition"] = f'np.empty({lv["size"]}, dtype=np.{lv["dtype"]})'


    

