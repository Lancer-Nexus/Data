# VC6 makefile for StoryFactions.
# Jason Hood, 23 March, 2010.
# 14 March, 2022: add base address, file alignment.

FL = \Games\Freelancer

storyfactions.dll: storyfactions.cpp storyfactions.res common.lib
	cl /nologo /W3 /EHsc /O2 /MD /LD storyfactions.cpp storyfactions.res /link /base:0x6220000 /filealign:512

common.lib: common.def
	lib /nologo /machine:ix86 /def:common.def /name:COMMON

install: storyfactions.dll
	copy storyfactions.dll $(FL)\EXE
	copy storyfactions.ini $(FL)\DATA
