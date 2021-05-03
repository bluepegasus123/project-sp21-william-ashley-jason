 #!/bin/bash

for file in ./inputs/small/*.in
do
    python3 jason.py $file  #2>>./errors_small.txt 1>>./stdout_small.txt
done

for file in ./inputs/medium/*.in
do
    python3 jason.py $file& #2>>./errors_medium.txt 1>>./stdout_medium.txt
done

for file in ./inputs/large/*.in
do
    python3 jason.py $file& #2>>./errors_large.txt 1>>./stdout_large.txt
done

