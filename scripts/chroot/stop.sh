#!/bin/bash

set -e

. vars.sh

function unmount() {
	echo "Unmounting mountpoints in old chroot"
	for i in `cat /proc/mounts | cut -d' ' -f2 | grep "^$1" | sort -r`; do
		echo "Unmounting ${i}"
		sudo umount "${i}";
	done
}

if [ -d ${FULL_CHROOT_PATH} ]; then
	echo "Kill remaining processes that run in the chroot"
	KILL_PIDS=""
	for i in /proc/[0-9]*; do
		PID=$(echo -n $i | sed "s:/proc/::");
		ROOT=$(sudo readlink "$i/root" || true);
		if [ "${ROOT}" == "${FULL_CHROOT_PATH}" ]; then
			echo "Killing PID ${PID}";
			KILL_PIDS="${KILL_PIDS} ${PID}";
			sudo kill "${PID}" || echo "Process with PID ${PID} already exited";
		fi
	done

	for time_left in `seq 29 -1 0`; do
		RUNNING_KILL_PIDS="";
		echo "Checking if all processes died (${time_left}s left)"

		if [ "${KILL_PIDS}" != "" ]; then
			echo "Will check PIDs ${KILL_PIDS}"
		fi

		for pid in ${KILL_PIDS}; do
			echo "Checking if process with PID ${pid} is still running";
			STATUS=$(sudo kill -CONT ${pid} 2>&1 && echo "RUNNING" || echo "KILLED")
			if [ "${STATUS}" == "RUNNING" ]; then
				echo "Process with PID ${pid} is still running";
				RUNNING_KILL_PIDS="${RUNNING_KILL_PIDS} ${pid}";
			fi
		done

		KILL_PIDS="${RUNNING_KILL_PIDS}";

		if [ "${KILL_PIDS}" == "" ]; then
			break;
		fi

		sleep 1;
	done
	
	unmount "${FULL_CHROOT_PATH}";
fi
