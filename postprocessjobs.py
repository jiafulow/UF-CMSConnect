import os
import time
import shutil
import jinja2
import glob
import tarfile


TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

class PostProcessJobs(object):
  """An interface for creating postprocessing jobs for HTCondor submission.
  """
  def __init__(self, datatype=None):
    self.datatype ='mc' if datatype is None else datatype
    self._templates = jinja2.Environment(
      loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
      trim_blocks=True,
    )

  def create(self, tag, algo=None, analysis=None, is_data=False, jobids=[], commands={}):
    """Create postprocessing jobs to HTCondor.
    Parameters
    ----------
    tag : str
        The name of the job submission directory.
    algo : str, optional
        The algorithm type used in the user script. The default is None.
    analysis : str, optional
        The analysis mode used in the user script. The default is None.
    is_data : bool, optional
        Whether the ntuples are data or Monte Carlo. The default is False for Monte Carlo.
    jobids : list, optional
        The ids of the jobs to submit. The default is nothing.
    commands : dict, optional
        HTCondor commands to additionally include in the submit description file. The default is nothing.
    """
    # Create context used by the template.
    context = {
      'environ': os.environ,
      'timestamp': time.strftime('%a %b %d %H:%M:%S %Z %Y'),
      'algo': algo,
      'analysis': analysis,
      'is_data': is_data,
      'jobids': jobids,
      'commands': commands,
    }

    # Create the job submission directory.
    dagdir_short = os.path.join('connect_projects', tag)
    dagdir = os.path.join(os.getcwd(), dagdir_short)
    if not os.path.exists(dagdir):
      os.makedirs(dagdir)

    # Generate the job submission files.
    self._generate_from_template('node', os.path.join(dagdir, 'node'), context)

    shutil.copy(os.path.join(TEMPLATE_DIR, 'worker.sh'), dagdir)  # preserve executable permission
    self._generate_from_template('worker.sh', os.path.join(dagdir, 'worker.sh'), context)

    shutil.copy(os.path.join(TEMPLATE_DIR, 'default.tgz'), dagdir)

    shutil.copy(os.path.join(TEMPLATE_DIR, 'FrameworkJobReport.xml'), dagdir)

    logdir = os.path.join(dagdir, 'logs')
    if not os.path.exists(logdir):
      os.makedirs(logdir)

    print('Generated job submission directory: {0}/'.format(dagdir_short))

  def _generate_from_template(self, name, path, context):
    """Generate a job submission file by rendering its template.
    Each job submission file has a corresponding template with variables
    that are rendered using the job submission arguments and environment.
    Parameters
    ----------
    name : str
        The name of the template. The available templates are:
          * node
          * worker.sh
    path : path
        The output file path.
    context : dict
        The mapping between job submission arguments and environment
        variables to the names of their corresponding template variables.
    """
    template = self._templates.get_template(name)
    with open(path, 'w') as f:
      f.write(template.render(context))

  def pack(self, files):
    """Add user files into a tarball, including the CMSSW base.
    """
    # Assume files[0] is the executable, rename it to 'my_app.py' (by making a temporary copy)
    shutil.copy(files[0], os.path.join(TEMPLATE_DIR, 'my_app.py'))
    files[0] = os.path.join(TEMPLATE_DIR, 'my_app.py')

    # Include files from the CMSSW base
    cmssw_base = os.environ['CMSSW_BASE']
    files += [cmssw_base]

    # Pack the files into a tarball
    self._pack_files(name=os.path.join(TEMPLATE_DIR, 'default.tgz'), files=files)

    os.remove(files[0])  # remove the temporary copy

  def _pack_files(self, name='default.tgz', mode='w:gz', dereference=True, files=None, filter_func=None):
    files = files or []
    with tarfile.open(name, mode, dereference=dereference) as tar:
      for globname in files:
        filenames = glob.glob(globname)
        if not filenames:
          raise Exception("The input file '%s' cannot be found." % globname)
        for filename in filenames:
          arcname = os.path.basename(filename)
          tar.add(filename, arcname, recursive=True, filter=filter_func)
