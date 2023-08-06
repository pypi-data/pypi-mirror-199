import os
import importlib
import numpy as np

from brian2.core.clocks import Clock
from brian2.core.namespace import get_local_namespace
from brian2.core.network import TextReport, _get_all_objects
from brian2.groups.neurongroup import NeuronGroup
from brian2.synapses.synapses import Synapses
from brian2.units import second

from lava.magma.core.run_configs import Loihi1SimCfg
from lava.magma.core.run_conditions import RunSteps
from lava.proc.monitor.process import Monitor

from pprint import pprint


def network_run(
        self,
        net,
        duration,
        report=None,
        report_period=10 * second,
        namespace=None,
        profile=False,
        level=0,
        **kwds
    ):
    """
    Performs preparations and checks and finally calls the `build` method from the device.

    Parameters
    ----------
    TODO

    Notes
    -----
    This is called very early in the process and overwrites the `run()` method from `brian2.core.Network.run()`.
    """
    # Before doing anything check that the objects used by the user 
    # are supported by lava.
    check_for_brian2lava_support(net)
    
    # Store duration in device
    self.duration = duration
    
    # Log that the network run method was called
    self.logger.diagnostic("Network run is executing.")

    # Add the network from the current run call to the set of networks within this device
    #self.networks.add(net)
    
    # If keyword arguments are given, notify the user that these arguments are not used in Brian2Lava
    if kwds:
        self.logger.warn(
            'Unsupported keyword argument(s) provided for run: {}'.format(', '.join(kwds.keys()))
        )
        
    # FIXME Show an error if user enabled profiling, since it is not supported
    if profile is True:
        raise NotImplementedError('Brian2Lava does not yet support detailed profiling.')
    
    # FIXME Set clocks
    net._clocks = {obj.clock for obj in net.sorted_objects}
    t_end = net.t+duration
    for clock in net._clocks:
        clock.set_interval(net.t, t_end)
    
    # Get the local namespace, if no namespace was given
    if namespace is None:
        namespace = get_local_namespace(level=level+2)

    # Call before_run with namespace
    net.before_run(namespace)
    
    
    # Get all synapses objects
    #self.synapses |= {s for s in net.objects if isinstance(s, Synapses)}
    
    # Update device clocks by network clocks
    self.clocks.update(net._clocks)
    if len(self.clocks) > 1:
        raise NotImplementedError("Currently multiple clocks are not supported by brian2lava.")
    
    # Set current time to end time (FIXME why? and whyt is the difference between self.t and self.t_?)
    # NOTE by carlo: self.t is with unit, self.t_ is without unit
    net.t_ = float(t_end)

    # Gets the number of neurons for the neuron group
    # FIXME this currenty assumes only *one* NeuronGroup
    #       If multiple neuron groups are present, this needs to be changed
    for obj in net.objects:
        if isinstance(obj, NeuronGroup):
            self.N = obj._N
    
    # FIXME Taken from CPPStandaloneDevice, but unclear what it means
    # In the CPP device it is noted that this is a hack
    # https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L1404
    for clock in self.clocks:
        if clock.name == 'clock':
            clock._name = '_clock'
    
    # Collect code objects from network objects
    # Right now these lines don't really do anything since we're never referencing the 
    # variable code_objects again in this method
    code_objects = []
    self.lava_objects = []
    for obj in net.sorted_objects:
        # FIXME: Is this required? What does obj.active actually do?
        if obj.active:
            # These are (currently) the only BrianObjects that generate their own process
            # NOTE: This must be changed when implementing other Brian classes
            if any([isinstance(obj,supp_obj) for supp_obj in self.supported_processes]):
                self.lava_objects.append(obj)
            for codeobj in obj._code_objects:
                code_objects.append((obj.clock, codeobj))

    # FIXME This may require an update, similar to how CPPStandalone handles the report
    # https://github.com/brian-team/brian2/blob/master/brian2/devices/cpp_standalone/device.py#L1465
    #if report is not None:
    #    report_period = float(report_period)
    #    next_report_time = start_time + report_period
    #    if report == 'text' or report == 'stdout':
    #        report_callback = TextReport(sys.stdout)
    #    elif report == 'stderr':
    #        report_callback = TextReport(sys.stderr)
    #    elif isinstance(report, str):
    #        raise ValueError(f'Do not know how to handle report argument "{report}".')
    #    elif callable(report):
    #        report_callback = report
    #    else:
    #        raise TypeError(f"Do not know how to handle report argument, "
    #                        f"it has to be one of 'text', 'stdout', "
    #                        f"'stderr', or a callable function/object, "
    #                        f"but it is of type {type(report)}")
    #    report_callback(0*second, 0.0, t_start, duration)

    
    # TODO? At least in the CPPStandaloneDevice, there is some more code here,
    # that seems to generate some basic code lines ...

    #for a in self.arrays:
    #    if (a.name == 't') and isinstance(a.owner, Clock):
    #        print(a.get_value())
    
    # Call network after_run method
    net.after_run()
    
    # Call build method
    if self.build_on_run:
        if self.did_run:  # FIXME necessary?
            raise RuntimeError("The network has already been built and run "
                               "before. Use set_device with "
                               "build_on_run=False and an explicit "
                               "device.build call to use multiple run "
                               "statements with this device.")
        self.build(direct_call=False, **self.build_options)

def check_for_brian2lava_support(net):
    """
    Checks that the objects defined by the user are supported by the lava device.
    If not, it throws a NotImplementedError
    Parameters
    ----------
    net : brian2.network.Network

    raises : NotImplementedError
            If any of the objects in the Network are not currently supported by brian2lava
    """
    from brian2 import get_device
    device = get_device()
    # Raise an error if the user is trying to implement unsupported objects
    objects = []
    for obj in net.sorted_objects:
        if any([isinstance(obj,unsupp_obj) for unsupp_obj in device.unsupported_processes]):
            obj_type = type(obj).__name__
            objects.append(obj_type)
        
    if len(objects):
        objects_repr = '\n\t\t'.join(objects)
        msg = f"""
        The following objects are not supported by brian2lava, yet:
                {objects_repr}
        You can expect them in future releases. You can also ask for features 
        on the official brian2lava repo on GitLab:
        https://gitlab.com/brian2lava/brian2lava/-/tree/main
        """
        raise NotImplementedError(msg)
        


def compile_templates(directory, names):
    """
    Compiles the rendered templates and returns the obtained process model

    Parameters
    ----------
    directory : `string`
        The project directory, necessary to find files to compile.
    names : network object names
        Names of network objects that are used for the Lava templates
    
    Returns
    -------
    compiled_processes: `Process`
        The compiled Lava process
    """
    # Execute Lava process and Lava process model
    # Add all outcomes to global scope
    compiled_processes = {}
    for name in names:
        exec(open(f'{directory}/{name}_process.py').read(), globals())
        exec(open(f'{directory}/{name}_process_model.py').read(), globals())
    
        exec(f"compiled_processes['{name}'] = {name}_P(name = '{name}')")
    
    # Get instance of the process
    # NOTE Linting assumes that 'Process' is not defined it does not
    #      understand that it comes from the exec above
    return compiled_processes  # noqa: F821


def run(self):
    """
    Executes the Lava simulation.

    We first compile the templates, initialize Lava and add configured monitors.
    Finally, the compiled Lava code is executed and monitor data is extracted.
    """
    
    # TODO should we use the exec or the import version?
    # NOTE import seems not to work at the moment, exec works
    #import sys
    #sys.path.append(self.project_dir)
    #from process_model import ProcessModel
    #from process import Process
    
    # Compile templates
    processes = compile_templates(self.project_dir, [obj.name for obj in self.lava_objects])

    
    # NOTE adding one step is necessary such that spikes are evaluated
    #      correctly by Lava and match Brian results
    num_steps = int(self.duration/self.defaultclock.dt) + 1

    # First initialize the monitors
    for process in processes.values():
        self.init_lava_monitors(process, num_steps)
    
    # Connect the ports of connected processes
    self.connect_lava_ports(processes)
    root_processes = self.select_root_processes(processes)
    # Log that the run method was called
    self.logger.diagnostic(f'Run Lava simulation for {self.duration} ({num_steps} steps)')
    print(f'Run Lava simulation for {self.duration} ({num_steps} steps)')
    
    # Run the simulation
    for process in root_processes:
        self.logger.debug(f"Running process: {process.name}")
        # Prepare simulation
        run_cfg = Loihi1SimCfg()
        process.run(condition=RunSteps(num_steps=num_steps), run_cfg=run_cfg)

    # After running the simulation, copy the monitored values from all the processes to brian
    for process in processes.values():
        # Set monitor values
        self.set_brian_monitor_values(process)
    
    # Indicate that the network simulation did run
    self.did_run = True


def connect_lava_ports(self, processes):
    """
    Connect the ports of the connected processes.

    Parameters
    ----------
    processes : `Process[]`
        Compiled Lava processes.
    """

    for var in self.lava_ports.values():
        portname = var['portname']
        pathway = var['pathway']

        # First connect the spiking sources to the synapses
        source = processes[var['sender']]
        synapses = processes[pathway.synapses.name]

        # To avoid the DuplicateConnection error from Lava
        syn_spikes_in = synapses.in_ports._members['s_in_'+pathway.prepost]
        # Only reshape the spike port once
        if syn_spikes_in.size == 0:
            # Here we shape the InPort of synapses to accomodate the spikes
            neur_spike_port = processes[source.name].out_ports._members[source.name+'_s_out']
            syn_spikes_in.shape = neur_spike_port.shape
            # Connect the spike ports
            neur_spike_port.connect(syn_spikes_in)
            self.logger.debug(f"Connected {source.name} spiking port to {synapses.name} input")

        # Then connect the synapses to the neurons, here we only require the name
        target = var['receiver']

        # Again, first reshape the ports as needed
        # TODO: not sure this is the intended use of the _members attribute of the Collection class:
        # https://github.com/lava-nc/lava/blob/4283428c3dda02ea6c326d5660a952cafcdd2c03/src/lava/magma/core/process/process.py
        syn_out_port = processes[synapses.name].out_ports._members[portname+'_out']
        neur_in_port = processes[target].in_ports._members[portname+'_in']

        # Reshape the input port of the neuron 
        neur_in_port.shape = syn_out_port.shape
        # Connect the port
        syn_out_port.connect(neur_in_port)

        self.logger.debug(f"Connected {synapses.name} variable {portname} to target neuron: {target}")


def select_root_processes(self, processes):
    """
    This is a helper function to determine which processes to run, in order to avoid running 
    processes connnected to each other twice. Lava automatically runs connected processes together,
    so if we have A-->B-->C we only need to run A.
    This function selects one node from each isolated subnetwork in the lava_ports dictionary through
    a breadth-first search algorithm.

    Parameters
    ----------
    processes : `Process[]`
        A list of the initialized processes in the simulation.

    Returns
    -------
    `list`
        A list of root processes, one from each isolated subnetwork.
    """

    # Build the graph of connected processes
    graph = {}
    for node in self.lava_ports.values():
        sender = node['sender']
        receiver = node['receiver']
        synapses = node['pathway'].synapses.name
        if sender not in graph:
            graph[sender] = set()
        if receiver not in graph:
            graph[receiver] = set()
        graph[sender].add(receiver)
        # Also add the synapses to the sender graph
        graph[sender].add(synapses)
        graph[receiver].add(sender)
    
    # Check for processes which don't require lava ports (isolated components)
    for process in processes:
        if not process in list(graph.keys()):
            graph[process] = set()

    # Log the whole graph to know that everything is working out correctly
    self.logger.diagnostic(graph)

    # Traverse the graph to find connected components
    visited = set()
    components = []
    # BFS algorithm: https://en.wikipedia.org/wiki/Breadth-first_search
    for node in graph:
        if node not in visited:
            component = set()
            queue = [node]
            while queue:
                curr_node = queue.pop(0)
                if curr_node not in visited:
                    visited.add(curr_node)
                    component.add(curr_node)
                    # Add the neighboring nodes to the queue
                    queue.extend(graph[curr_node])
            components.append(component)

    # Select one node from each component
    root_nodes = []
    for component in components:
        root_nodes.append(processes[list(component)[0]])

    return root_nodes


def init_lava_monitors(self, process, num_steps):
    """
    Initializes monitors, defined by the user in Brian.

    Parameters
    ----------
    process : `Process`
        Lava process that is provided with a monitor
    num_steps : `int`
        Number of steps for which the monitor shall be active

    Notes
    -----
    Each probed Lava variable can be assigned to multiple monitors defined in Brian.
    E.g. time can be necessary for a state and a spike monitor, while time is only probed once from Lava.
    """
    # TODO: This might not be the best way to do this, but it ensures that no extra monitors are created
    # and that they are associated with the correct 'sources' only. Probably we could find a more efficient way to do this.
    for m in self.lava_monitors.values():
        # Only look at the right monitors
        if not process.name == m['source']:
            continue

        # If you find a process which should be monitored, look at which variable should be monitored
        lava_var_name = m['lava_var_name']

        # If the given process does not have the required variable, raise an error
        # This should never happen, but just for debugging I'll leave it for now
        if not hasattr(process,lava_var_name):
            raise ValueError(f"Something went wrong: the process {process} does not have the variable {lava_var_name} required from the monitor")
        
        
        # NOTE Lava allows only one monitor per variable, so we only create one if one was not already created
        try:
            # Init Lava monitor and define probe for variable
            monitor = Monitor()
            monitor.probe(getattr(process, lava_var_name), num_steps)
        # If the monitor already exists, lava throws an AssertionError
        except AssertionError:
            # If that's the case, we look for the monitor in the previously defined monitors
            for k in self.lava_monitors.values():
                if not k['lava_monitor'] is None and k['source'] == m['source'] and m['lava_var_name'] == k['lava_var_name']:
                    monitor = k['lava_monitor']
        m['lava_monitor'] = monitor
        m['process_name'] = getattr(process, 'name')


def set_brian_monitor_values(self, process):
    """
    Transform Lava monitors to Brian monitor format.

    Parameters
    ----------
    process : `Process`
        Lava process that is provided with a monitor
    """

    # Iterate over Lava monitors
    for k, m in self.lava_monitors.items():
        # Only do this if the monitor refers to this process
        if not getattr(process,"name") == m['process_name']:
            continue
        # Get monitor variable
        var = m['var']

        # Define empty data variable
        # NOTE Lava monitors do not probe the inital values while Brian does
        #      We need to manually prepend the initial values to the monitored data
        init_data = None  # Contains initial values
        data = None  # Contains all other values

        # In case of a spike monitor, we need a more specific handling to get the time/spike indices
        if m['type'] == self.monitor_types['spike']:

            if var.name == 't':
                # Find monitor that contains 'i' variable
                spike_monitor_name = f'_spike_{var.owner.name}_i'
                spike_monitor = self.lava_monitors[spike_monitor_name]
                # Get raw data from Lava monitor
                raw = get_monitor_values(spike_monitor)
                # Transform data to get actual spike times
                data = (np.nonzero(raw)[0] * self.defaultclock.dt) - self.defaultclock.dt

                # Get initial values from process
                init_raw = getattr(process, f'_{getattr(process,"name")}__spikespace').init
                # Transform data to get actual spike times
                init_data = np.nonzero(init_raw)[0] * self.defaultclock.dt

            if var.name == 'i':
                # Get raw data from Lava monitor
                raw = get_monitor_values(m)
                # Make sure that we always have two dimensions
                if np.ndim(raw) == 1:
                    raw = [raw]
                # Transform data to get indices
                data = np.nonzero(raw)[1]

                # Get initial values from process
                init_raw = getattr(process, f'_{getattr(process,"name")}__spikespace').init
                # Transform initial data to get indices
                init_data = np.nonzero(init_raw)[0]

        # In case of a state monitor, just take the raw data from Lava
        if m['type'] == self.monitor_types['state']:
            # NOTE remove additional simulation steps from monitor to match Brian simulation
            data = get_monitor_values(m)[:-2]

            # Get initial values from process
            init_data = getattr(process, m['lava_var_name']).init

        # Get dimension of data array
        dim = np.ndim(data)

        # Append init values and store data in related array variable
        if dim == 1:
            self.arrays[var] = np.append(init_data, data)

        if dim == 2:
            self.arrays[var] = np.append([init_data], data, axis=0)


def get_monitor_values(monitor):
    """
    Get data from a Lava monitor.

    Parameters
    ----------
    monitor
        A monitor as defined in the device
    """
    # Define variables
    lava_monitor = monitor['lava_monitor']
    lava_var_name = monitor['lava_var_name']
    process_name = monitor['process_name']
    # Return lava monitor values
    # TODO we need to find out how Lava processes are numbered, 'Process_0'
    #      is probably not generalizing for more than one process
    # NOTE: SHOULD BE FIXED NOW!
    data = lava_monitor.get_data()[process_name][lava_var_name]
    return np.squeeze(np.array(data))
