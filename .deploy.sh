read -p "Enter UCL CS Username: " uname
rsync -av --delete -e ssh --exclude=".*" ./. $uname@csrw2.cs.ucl.ac.uk:/cs/student/www/2020/group19/