#!/bin/bash
WORKDIR=/opt/antifilter
LIST_PATH=$WORKDIR/list
MD5_FILE=$WORKDIR/md5.txt

URL=https://antifilter.download/list

touch $MD5_FILE
mkdir -p $LIST_PATH

cd $LIST_PATH || exit

wget -N $URL/ipsum.lst $URL/subnet.lst

OLD_LISTS_MD5=$(cat $MD5_FILE)
NEW_LISTS_MD5=$(cat $LIST_PATH/*.lst | md5sum | head -c 32)

if [ "$OLD_LISTS_MD5" != "$NEW_LISTS_MD5" ]; then
  cat $LIST_PATH/ipsum.lst | sed 's_.*_route & reject;_' > /etc/bird/ipsum.txt
  cat $LIST_PATH/subnet.lst | sed 's_.*_route & reject;_' > /etc/bird/subnet.txt
  /usr/sbin/birdc configure
  logger "antifilter lists updated"
  echo $NEW_LISTS_MD5 > $MD5_FILE
fi
