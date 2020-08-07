#!/bin/bash
export args=$@
export script=$(readlink -f $0)
export script_path=`dirname $script`/
export logs_folder="${script_path}logs/"
export log_file="${logs_folder}pik_checker_$(date +%Y%m%d%H%M%S).log"

[ -d ${logs_folder} ] || mkdir -p ${logs_folder}
[ -f ${log_file} ] || touch ${log_file}
exec > >(tee -a ${log_file})

while [ 1 ]; do
  date +%Y-%m-%d_%H:%M:%S
  python check.py
  test $? -gt 128 && break
  sleep 1800
done