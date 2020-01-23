import os

from postprocessjobs import PostProcessJobs


# Input files
# The main python script should always be the first file.
input_dir = '/home/jlow/nobackup/L1MuonTrigger/P2_CMSSW_10_6_3/src/L1TMuonSimulations/Analyzers/test7/'
input_files = [
  'rootpy_trackbuilding11.py', 'nn_*.py', 'pattern_bank_18patt.29.npz',
  'model.29.h5', 'model_weights.29.h5', 'model.29.json',
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

jobs.create(tag='test1', algo='default', analysis='roads', jobids=range(100), commands=commands)
jobs.create(tag='test2', algo='default', analysis='mixing', jobids=range(357), commands=commands)
jobs.create(tag='test3', algo='default', analysis='rates', jobids=range(40,85), commands=commands)
jobs.create(tag='test3_140', algo='default', analysis='rates140', jobids=range(30,63), commands=commands)
jobs.create(tag='test3_250', algo='default', analysis='rates250', jobids=range(50,125), commands=commands)
jobs.create(tag='test3_300', algo='default', analysis='rates300', jobids=range(0,111), commands=commands)
jobs.create(tag='test4', algo='default', analysis='effie', jobids=range(5), commands=commands)
jobs.create(tag='test4_200', algo='default', analysis='effie200', jobids=range(33), commands=commands)
