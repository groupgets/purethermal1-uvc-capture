ACLOCAL_AMFLAGS = -I build ${ACLOCAL_FLAGS}

AM_CFLAGS = $(GLOBAL_CFLAGS)

bin_PROGRAMS = pt1-v4l2-grab
pt1_v4l2_grab_SOURCES = \
    pt1-v4l2-grab.c

pt1_v4l2_grab_CPPFLAGS = $(AM_CFLAGS) $(libv4l2_CFLAGS) $(libv4lconvert_CFLAGS)
pt1_v4l2_grab_LDADD = $(libv4l2_LIBS) $(libv4lconvert_LIBS)
