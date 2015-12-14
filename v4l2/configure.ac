dnl Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)
AC_INIT(pure-thermal-examples, 1.0, labs@groupgets.com)
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_AUX_DIR([m4])

AM_INIT_AUTOMAKE([1.11 subdir-objects -Wall foreign no-define])

AC_PROG_CC
AM_PROG_CC_C_O
AC_PROG_CXX
AC_PROG_LIBTOOL

PKG_CHECK_MODULES([libv4l2], [libv4l2 >= 0.0.0])
PKG_CHECK_MODULES([libv4lconvert], [libv4lconvert >= 0.0.0])
# PKG_CHECK_MODULES([libusb], [libusb-1.0 >= 0.0.0])
# PKG_CHECK_MODULES([zlib], [zlib >= 0.0.0])

# Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS([stdint.h stdlib.h string.h])

AC_OUTPUT(Makefile grab/Makefile)

echo "
Configuration for $PACKAGE $VERSION:
-------------------------------------------

  Install prefix: .........: $prefix

  Now type 'make' to build $PACKAGE $VERSION,
  and then 'make install' for installation.
"
