# https://stackoverflow.com/questions/15993062/bash-scripting-missing

$y "Pssad"
top -b -n 1 > topLog.log
grep -w "$y" topLog.log > p1
if [ -s "p1"];  # Error
then 
    echo "Successful "
else
    echo "Unsuccessful"
fi
rm p1