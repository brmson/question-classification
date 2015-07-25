#!/bin/bash
echo "`cat ${1} | wc -l` ${2}" |cat - ${1} > /tmp/out && mv /tmp/out ${1} 

