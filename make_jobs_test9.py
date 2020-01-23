import os

from postprocessjobs import PostProcessJobs


# Input files
# The main python script should always be the first file.
input_dir = '/home/jlow/nobackup/L1MuonTrigger/P2_CMSSW_10_6_3/src/L1TMuonSimulations/Analyzers/test9/'
input_files = [
  'emtf_ristretto.py', 'emtf_algos.py', 'emtf_utils.py',
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

jobs.create(tag='test1', algo='default', analysis='signal', jobids=range(200), commands=commands)
jobs.create(tag='test2', algo='default', analysis='bkgnd', jobids=range(192), commands=commands)

#jobs.create(tag='test1_prompt', algo='default', analysis='signal', jobids=range(100), commands=commands)
