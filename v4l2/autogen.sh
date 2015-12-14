#!/bin/sh

gprefix=`which glibtoolize 2>&1 >/dev/null`
if [ $? -eq 0 ]; then 
  glibtoolize --force
else
  libtoolize --force --automake
fi
aclocal -I m4
autoconf
autoheader
automake --add-missing

if [ -n "$CONFIGURE" ]; then
  if [ -n "$TARGET_SYS" ]; then
    ./configure "$@" --host=${TARGET_SYS}
  else
    ./configure "$@"
  fi
fi
