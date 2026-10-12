# Makefile (VC6) for Territory.
# Jason Hood, 21 August, 2009 (updated 21 February, 2014).

CPPFLAGS = /nologo /W3 /GX /O2 /MD /LD

Territory.dll: Territory.cpp Territory.res Common.lib
	cl $(CPPFLAGS) $** /link /base:0x6130000 /filealign:512

Common.lib: Common.def
	lib /nologo /machine:ix86 /def:Common.def
