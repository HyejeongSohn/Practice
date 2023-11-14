#!bin/bash

#사용자에게 질문하기
echo "리눅스가 재미있나요 ? (yes / no)"
read answer

#입력된 답변을 소문자로 변환하기
answer=$(echo "$answer"| tr '[:upper:]' '[:lower:]')

#입력된 답변이 yes 또는 no로 시작하는지 확인

case $answer in
y* | yes )
echo "yes"
;;
n* | no)
echo "no"
;;
*)
echo "yes or no로 입력해 주세요."
;;
esac


