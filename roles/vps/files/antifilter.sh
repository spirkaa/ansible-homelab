#!/bin/bash
WORKDIR=/opt/antifilter
MD5_FILE=$WORKDIR/md5.txt
LIST_PATH=$WORKDIR/list
LIST_NAME=allyouneed

URL=https://antifilter.download/list/$LIST_NAME.lst

touch $MD5_FILE
mkdir -p $LIST_PATH

cd $LIST_PATH || exit

wget -N $URL

OLD_LISTS_MD5=$(cat $MD5_FILE)
NEW_LISTS_MD5=$(cat $LIST_PATH/*.lst | md5sum | head -c 32)

if [ "$OLD_LISTS_MD5" != "$NEW_LISTS_MD5" ]; then
  cat $LIST_PATH/$LIST_NAME.lst | sed 's_.*_route & reject;_' > /etc/bird/$LIST_NAME.txt
  /usr/sbin/birdc configure
  logger "antifilter lists updated"
  echo $NEW_LISTS_MD5 > $MD5_FILE
fi
