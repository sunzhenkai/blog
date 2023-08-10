#!/bin/bash
set -x
base=`pwd`

pushd docs && git checkout master && git pull && popd && bash deploy.sh
