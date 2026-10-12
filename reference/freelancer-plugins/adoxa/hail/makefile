# Makefile (VC6) for Hail.
# Jason Hood, 22 May, 2013.

CFLAGS = /nologo /W3 /GfX /Ox /MD

Hail.dll: Hail.obj Hail.res
	cl $(CFLAGS) /LD $** /link /base:0x6090000 /filealign:512

clean:
	del *.obj *.res
