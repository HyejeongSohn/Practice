#!/bin/bash

operand1=$1
operator=$2
operand2=$3

result=$(expr $operand1 $operator $operand2)

echo $result
