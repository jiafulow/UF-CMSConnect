#!/bin/bash

CONNECT_CMSSW_VERSION=CMSSW_10_6_3
if [ ! -d "$CONNECT_CMSSW_VERSION" ]; then
  cmsrel $CONNECT_CMSSW_VERSION
fi

cd $CONNECT_CMSSW_VERSION/src
cmsenv
cd -

# CMSConnect
source ~/software/connect-client/client_source.sh
alias connnode='connect submit node'
alias connpull='connect pull'

# Renew grid proxy
#connect shell
#export HOME=/home/$USER
#voms-proxy-init -voms cms -valid 192:00
#exit

