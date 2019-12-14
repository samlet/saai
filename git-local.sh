#!/bin/bash
rm /pi/archive/sagas-saai*
git archive --format=tar --prefix=saai/ HEAD | gzip >/pi/archive/sagas-saai-0.1.tar.gz
echo 'done.'
ls -alh /pi/archive/sagas-saai*

