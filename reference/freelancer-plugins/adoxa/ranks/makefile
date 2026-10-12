# VC6 Makefile for Ranks.
# Jason Hood, 16 August, 2010.

FLPATH = \Games\Freelancer

ranks.dll: ranks.cpp ranks.res common.lib
	cl /nologo /W3 /GfX /Ox /MD /LD ranks.cpp ranks.res user32.lib

common.lib: common.def
	lib /nologo /machine:ix86 /def:common.def /name:COMMON

install: ranks.dll
	copy ranks.dll $(FLPATH)\EXE
