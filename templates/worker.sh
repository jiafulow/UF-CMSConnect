#!/bin/bash

# Automatically generated on {{ timestamp }}

# The SCRAM architecture and CMSSW version of the submission environment.
readonly SUBMIT_SCRAM_ARCH="{{ environ['SCRAM_ARCH'] }}"
readonly SUBMIT_CMSSW_VERSION="{{ environ['CMSSW_VERSION'] }}"

# Capture the executable name and job input file from the command line.
readonly CONDOR_EXEC="$(basename $0)"
export CONDOR_EXEC
readonly TARBALL="default.tgz"
readonly ALGO="$1"
readonly ANALYSIS="$2"
readonly JOBID="$3"
readonly EXE="python my_app.py $ALGO $ANALYSIS $JOBID"


echo "[INFO] Environment variables: -"
echo "SUBMIT_SCRAM_ARCH=$SUBMIT_SCRAM_ARCH"
echo "SUBMIT_CMSSW_VERSION=$SUBMIT_CMSSW_VERSION"
echo "HOME=$HOME"
echo "CONDOR_EXEC=$CONDOR_EXEC"
echo "_CONDOR_SCRATCH_DIR=$_CONDOR_SCRATCH_DIR"
echo "PWD=$PWD"
echo "ARGS=$@"

echo "[INFO] Unpacking files"
tar xzf $TARBALL

echo "[INFO] Setting up CMSSW"

# Setup the CMS software environment.
export SCRAM_ARCH="$SUBMIT_SCRAM_ARCH"
source /cvmfs/cms.cern.ch/cmsset_default.sh
#scram project CMSSW "$SUBMIT_CMSSW_VERSION"
cd "$SUBMIT_CMSSW_VERSION/src"
eval "$(scramv1 runtime -sh)"

# Change back to the worker node's scratch directory.
cd "$_CONDOR_SCRATCH_DIR"

echo "[INFO] ls (pwd: $PWD)"
ls -l

echo "[INFO] Stand back I'm going to try Science!"

# Do Science
$EXE

EXIT_STATUS=$?
ERROR_TYPE=""
ERROR_MESSAGE="This is an error message."

if [ $EXIT_STATUS -ne 0 ]; then
  echo "[ERROR] Job has failed!"
  # Write report
  cat << EOF > FrameworkJobReport.xml
<FrameworkJobReport>
<FrameworkError ExitStatus="$EXIT_STATUS" Type="$ERROR_TYPE" >
$ERROR_MESSAGE
</FrameworkError>
</FrameworkJobReport>
EOF
else
  echo "[INFO] Job finished successfully"
fi

echo "[INFO] Cleaning up"

# Clean up
tar tzf $TARBALL | xargs rm -rf
rm -rf $TARBALL
rm -rf *.pyc

echo "[INFO] ls (pwd: $PWD)"
ls -l

exit $EXIT_STATUS
