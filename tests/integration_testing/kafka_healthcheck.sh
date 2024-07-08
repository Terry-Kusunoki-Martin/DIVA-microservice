#! /bin/bash

unset JMX_PORT # https://github.com/wurstmeister/kafka-docker/issues/171#issuecomment-327097497
                                                                                         
function contains() {
     local n=$#
     local value=${!n}
     for ((i=1;i < $#;i++)) {
         if [ "${!i}" == "${value}" ]; then
             echo "y"
             return 0
         fi
     }
     echo "n"
     return 1
}

LOG_DIR=$(awk -F= -v x="log.dirs" '$1==x{print $2}' /opt/bitnami/kafka/config/server.properties)
x=`cat ${LOG_DIR}/meta.properties | awk 'BEGIN{FS="="}/^node.id=/{print $2}'`
if [ $(contains "0" "$x") == "y" ]; then echo "ok"; exit 0; else echo "doh"; exit 1; fi
