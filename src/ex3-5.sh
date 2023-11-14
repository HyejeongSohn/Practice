#!/bin/bash

function list_files() {
	local options

if [[ $# -eq 1 ]]; then
options="$1"
else
options="-1"
fi

ls "$options"
}

# main
if [[ $# -eq 0 ]]; then
echo "사용법: $(basename "$0") [옵션]"
exit 1
fi

#함수 호출
list_files() "$@"

#스크립트 종료
exit 0
