

### Requirements

You need to have a CMS Connect account. See: <https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCMSConnect>.

### Install CMS Connect client

To install the CMS Connect client, follow the commands in `connect-client.sh`. See [here]( https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCMSConnect#Using_the_Connect_client) for more details.

You should also add the SSH key to your account. See [here](https://ci-connect.atlassian.net/wiki/spaces/CMS/pages/57436024/Generate+SSH+key+pair+and+add+the+public+key+to+your+account) for instructions.

### Use this repository

First, check out this repository:

``` shell
# Make sure to use the correct branch for the CMSSW version
git clone -b L1MuonTrigger-P2_10_6_3 git@github.com:jiafulow/UF-CMSConnect.git CMSConnect/P2_10_6_3
```

To set up the environment, follow the commands in `startup.sh`. Note that this changes the CMSSW base. Also note that this needs to be done at the beginning of every new session.

To create the jobs, first change the `input_dir` variable in `make_jobs_test7_displ.py` to point to the input directory of your python script. If necessary, also change the `input_files` variable to include all the files you want to submit together with the python script.

Then, execute `make_jobs_test7_displ.sh`. (Note: '.sh' instead of '.py'.)

``` shell
source make_jobs_test7_displ.sh
```

Several directories are created under 'connect_projects'. These directories contain the inputs necessary to run the jobs, but the jobs are not yet submitted. To submit the jobs, go into each generated directory (e.g. 'connect_projects/myproj') and do the following:

``` shell
cd connect_projects/myproj
connect submit node
cd -
```

(If you want, you can automatize this process by writing a simple bash script.)

To check the status of the submitted jobs:

``` shell
connect q
```

To retrieve the job outputs when the jobs are done, go into each generated directory and do the following:

``` shell
cd connect_projects/myproj
connect pull
cd -
```


### Additional notes

#### Note 1

The grid certificate on the CMS Connect machine needs to be renewed from time to time. (Note: This is not the grid certificate on your local machine). To do so, first connect to the CMS Connect machine:

``` shell
connect shell
```

It will give you a new shell. In this new shell, do:

``` shell
export HOME=/home/$USER
voms-proxy-init -voms cms -valid 192:00
exit
```

#### Note 2

If the job outputs are ROOT files, you can merge them:

``` shell
hadd -f histos_add.root connect_projects/myproj/histos_*.root
```

If the job outputs are Numpy array files (.npz), you can merge them using the script `etc/hadd_npz.py`:

``` shell
python etc/hadd_npz.py -f histos_add.npz connect_projects/myproj/histos_*.npz
```


### Acknowledgement

This repository was derived from Sean-Jiun Wang's [cmslpc_postproc](https://github.com/swang373/cmslpc_postproc) repository.

