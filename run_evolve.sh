#!/bin/bash
i="0"

while [ $i -lt 50 ]
do
"python" "evolve.py" "-saved"
i=$[$i+1]
done