#!/bin/bash

USERNAME=jiafulow

# Do some clean up in the local area
if [ -d connect_projects ]
then
  rm -rf connect_projects_old/
  mv connect_projects/ connect_projects_old/
fi

# Do some clean up in the remote area
connect shell find /local-scratch/$USERNAME/connect-client/ -name "test*" -type d -exec rm -rf {} +

# Make jobs
python make_jobs_test7_displ.py

# Submit jobs
#cd connect_projects/test1 && connnode && cd -
#cd connect_projects/test2 && connnode && cd -
#cd connect_projects/test3 && connnode && cd -
#cd connect_projects/test3_140 && connnode && cd -
#cd connect_projects/test3_250 && connnode && cd -
#cd connect_projects/test3_300 && connnode && cd -
#cd connect_projects/test4 && connnode && cd -
#cd connect_projects/test4_200 && connnode && cd -
