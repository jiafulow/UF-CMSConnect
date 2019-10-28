import os

from postprocessjobs import PostProcessJobs


# Input files
# The main python script should always be the first file.
input_dir = '/home/jlow/nobackup/L1MuonTrigger/P2_CMSSW_10_6_3/src/L1TMuonSimulations/Analyzers/test9/'
input_files = [
  'emtfpp_ristretto.py', 'emtfpp_espresso.py', 'emtfpp_algos.py', 'emtfpp_utils.py',
]
input_files = map(lambda x: os.path.join(input_dir, x), input_files)  # prepend input dir

# Additional HTCondor commands
commands = {
  '+ProjectName': 'cms.org.ufl',
  '+REQUIRED_OS': '\"rhel7\"',
}

# Create jobs
print('Using CMSSW base: {0}'.format(os.environ['CMSSW_BASE']))
jobs = PostProcessJobs()
jobs.pack(input_files)

jobs.create(tag='signal', algo='default', analysis='signal', jobids=range(100), commands=commands)
jobs.create(tag='bkgnd', algo='default', analysis='bkgnd', jobids=range(192), commands=commands)
