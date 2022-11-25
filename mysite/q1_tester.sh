rm -f announcements.txt
python3 q1.py "$1" "$2" "Kalind Rajesh Karia"
DIFF=$(diff announcements.txt announcements1.txt)
if [ "$DIFF" = "" ];
then
    echo "testcase 1 passed"
else
    echo "testcase 1 failed"
fi
rm -f announcements.txt
python3 q1.py "$1" "$2" "Ekatpure Rutuja Dattatray Dattatray"
DIFF=$(diff announcements.txt announcements2.txt)
if [ "$DIFF" = "" ];
then
    echo "testcase 2 passed"
else
    echo "testcase 2 failed"
fi
rm -f announcements.txt
