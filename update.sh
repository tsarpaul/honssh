# Ugly hack, didn't find a trivial way to import packages with twistd running as root
rm -r /usr/lib/python2.7/dist-packages/kippo /usr/lib/python2.7/dist-packages/honssh
cp -r kippo honssh /usr/lib/python2.7/dist-packages/

