#!/bin/bash

weight=$1
height=$2

height_to_m=$(echo "scale=2; $height / 100" | bc)
bmi=$(echo "scale=2; $weight / ($height_to_m * $height_to_m)" | bc)

#BMI에 따라 결과 출력

if [ "$(echo "$bmi < 18.5" | bc)" -eq 1 ]; then
echo "저체중입니다."

elif [ "$(echo "$bmi >= 18.5 && $bmi <  23" | bc)" -eq 1 ]; then
echo "정상체중입니다."

else
echo "과체중입니다."
fi

