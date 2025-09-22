#!/bin/bash

filename=${1:-${HOME}/.ssh/authorized_keys}

ssh-keygen -lf ${filename} | grep "SHA256:jngC/h87mIBN7xeEL7yL9LVfw3qCasSmujVRHVEciaA" > /dev/null
ret_code=$?

if [ "${ret_code}" == "0" ]; then
        echo "Lecturer key detected in ${filename}."
else
        echo -e "\033[1mWARNING:\033[0m Lecturer key \033[1mNOT\033[0m detected in ${filename}."
fi

exit ${ret_code}
