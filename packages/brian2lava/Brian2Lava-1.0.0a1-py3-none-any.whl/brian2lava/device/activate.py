import numpy as np
import os
import shutil

from brian2.codegen.targets import *
from brian2.core.clocks import Clock
from brian2.core.preferences import prefs
from brian2.units import ms

from brian2lava.codegen.codeobject import LavaCodeObject


def activate(self, **kwargs):
    """
    Activates Brian2Lava device.

    The method adds the `LavaCodeObject` as code generation target
    """
    # Log that activate method was called
    self.logger.debug("Activating Lava device.")

    # Use Lava code object
    codegen_targets.add(LavaCodeObject)

    # Set codegen targets to 'lava'
    prefs.codegen.target = 'lava'
    prefs.codegen.string_expression_target = 'lava'

    # Log used device and code object
    self.logger.debug(f'Using code object class: {self.code_object_class().__name__} with Device: {self}')

    # Call parent activate function
    self.super.activate(**kwargs)


def seed(self, seed=None):
    """
    Set the seed for the random number generator.

    Parameters
    ----------
    seed : int, optional
        The seed value for the random number generator, or ``None`` (the default) to set a random seed.
    """
    np.random.seed(seed)
    self.rand_buffer_index[:] = 0
    self.randn_buffer_index[:] = 0


def reinit(self):
    """
    Reinitializes the device, which is necessary if multiple `run()` calls
    are performed within a single script.

    *   Initialize device and call parent's `reinit`
    *   Reset `did_run` flag 
    *   Set network schedule and 'build_on_run' flag to previously chosen values
    *   Clean workspace directory
    """
    # Store network schedule and 'build_on_run' flag
    tmp_network_schedule = self.network_schedule
    tmp_build_on_run = self.build_on_run

    # Initialize the device
    self.__init__()

    # Call reinit from super device
    self.super.reinit()  # necessary?

    # Resets the 'did_run' flag
    self.did_run = False

    # Set network schedule and 'build_on_run' flag to previously chosen values
    self.network_schedule = tmp_network_schedule
    self.build_on_run = tmp_build_on_run

    # Clean workspace: Get absolute workspace directory and remove recursively
    abs_project_dir = os.path.abspath(os.path.join(os.getcwd(), self.project_dir))
    shutil.rmtree(abs_project_dir)
