#!/bin/bash
rm /pi/archive/sagas/sagas-saai*
git archive --format=tar --prefix=sagas-ai/ HEAD | gzip >/pi/archive/sagas/sagas-saai-0.1.tar.gz
echo 'done.'
ls -alh /pi/archive/sagas/sagas-saai*

