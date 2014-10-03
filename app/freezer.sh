#!/bin/bash

DATE=$(date +%Y-%m-%d)

cp static/favicon.ico build/favicon.ico

cd build

find -maxdepth 3 -name index.html | sort | while read i
do
  md5sum "$i"
done >index.md5

wc -l index.md5

tar -czf $DATE.tar.gz --exclude='*.tar.gz' --exclude='deploy.sh' .

ls -lht $DATE.tar.gz
rm -f letras-viajeras.tar.gz
ln -s $DATE.tar.gz letras-viajeras.tar.gz

