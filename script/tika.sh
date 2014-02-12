#!/bin/bash

# Apache Tika Start Stop Script
# description: Control Apache Tika

tika_path="/opt/tika/tika-server-1.4.jar"
ps_name_tika="`basename $tika_path`"
java_path="/usr/bin/java"


if [ ! -f $tika_path ]
then
        echo "Error: Tika cannot be found on this system !!!"
        exit 1
fi


function is_tika_running()
{
      tika_proc="`ps -ef | grep "$ps_name_tika" | grep -v grep | wc -l`"
      
      if [ ! "$tika_proc" == "0" ]
      then
	  echo "1"
      else	    
	  echo "0"  
      fi
}


case "$1" in
'start')
	tika_result="`is_tika_running`"
	
	if [ $tika_result == "1" ]
	then
	    echo "[-] Tika is already running !!!"
	else
	    $java_path -jar $tika_path >/dev/null 2>/dev/null &
	    
	    if [ $? -eq 0 ]
	    then
		echo "[+] Tika has been started ..."
	    else
		echo "[-] Tika cannot be started ..."
	    fi
	    
	fi    
;;	
'stop')
	tika_result="`is_tika_running`"
	
	if [ $tika_result == "0" ]
	then
	    echo "[-] Tika was already stopped ..."
	else
	    ps -ef | grep "$ps_name_tika" | grep -v grep | awk '{print $2}' | while read -r line
	    do
                kill -9 $line 2>/dev/null
	    done
        
	    echo "[+] Tika has been stopped ..."
	fi
	;;
'status')
        ps -ef | grep "$ps_name_tika" | grep -vq grep
        
        if [ $? -eq 0 ]
        then
                echo "[+] Tika is: Up"
        else
                echo "[+] Tika is: Down"
        fi
;;
*)
        echo "Usage: $0 { start | stop | status }"
        exit 1
;;
esac
exit 0


