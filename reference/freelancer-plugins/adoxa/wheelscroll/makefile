# Makefile (VC6) for WheelScroll.
# Jason Hood, 16 February, 2016.

CPPFLAGS = /nologo /W3 /O2 /MD /LD

WheelScroll.dll: WheelScroll.cpp WheelScroll.res
	cl $(CPPFLAGS) $** /link /base:0x6190000 /filealign:512
