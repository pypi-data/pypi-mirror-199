import os
import tempfile

# Import Brian2 modules
from brian2.utils.filetools import ensure_directory

# Import Brian2Lava modules
from brian2lava.writer.py import PyWriter


def prepare_directory(self):
    """
    Prepare the directory and make sure a given directory exists
    """
        
    # Create project directories (if not exists)
    ensure_directory(self.project_dir)
    #for d in ['code_objects', 'results', 'static_arrays']:
    #    ensure_directory(os.path.join(directory, d))

    # Log directory path
    self.logger.debug(
        "Writing Lava project to directory " + os.path.normpath(self.project_dir)
    )


def write_templates(self, process_rendered, process_model_rendered, name):
    """
    Write the rendered templates to files
    
    Parameters
    ----------
    process_rendered : `str`
        The rendered Lava process template as string
    process_model_rendered : `str`
        The rendered Lava process model template as string
    name : `str`
        Name of the network object (e.g. 'neurongroup_0')
    """
    
    # Instantiate python file writer
    writer = PyWriter(self.project_dir)
    
    # Write 'process' to working directory
    writer.write(f'{name}_process.py', process_rendered)
    
    # Log that process.py was stored
    self.logger.diagnostic(f'{name}_process.py stored in working directory.')
    
    # Write 'process model' to working directory
    writer.write(f'{name}_process_model.py', process_model_rendered)
    
    # Log that process_model.py was stored
    self.logger.diagnostic(f'{name}_process_model.py stored in working directory.')
