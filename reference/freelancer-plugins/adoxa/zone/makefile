# Makefile (VC6) for Zone.
# Jason Hood, 24 February, 2014.

CPPFLAGS = /nologo /W3 /O2 /MD /LD

Zone.dll: Zone.cpp Zone.res Common.lib
	cl $(CPPFLAGS) $** user32.lib /link /base:0x6140000 /filealign:512

Common.lib: Common.def
	lib /nologo /machine:ix86 /def:Common.def
