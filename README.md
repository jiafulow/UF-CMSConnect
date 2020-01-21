

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

To create the jobs, do the following:

``` shell
python example.py
```

To submit the jobs, go into the generated directory (e.g. 'connect_projects/myproj') and do the following:

``` shell
cd connect_projects/myproj
connect submit node
cd -
```

To check the status of the submitted jobs:

``` shell
connect q
```

To retrieve the job outputs when the jobs are done:

``` shell
cd connect_projects/myproj
connect pull
cd -
```


### Acknowledgement

This repository was derived from Sean-Jiun Wang's [cmslpc_postproc](https://github.com/swang373/cmslpc_postproc) repository.

