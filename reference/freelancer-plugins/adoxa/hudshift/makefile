# Makefile (VC6) for HUDSHIFT.
# Jason Hood, 19 June, 2010.

CPPFLAGS = /nologo /W3 /O2 /GX /MD /LD

HudShift.dll: HudShift.obj HudShift.res Common.lib
	cl $(CPPFLAGS) HudShift.obj HudShift.res /link /base:0x6200000 /filealign:512

Common.lib: Common.def
	lib /nologo /machine:ix86 /def:Common.def /name:Common
