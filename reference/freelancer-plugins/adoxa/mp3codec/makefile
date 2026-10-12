# Makefile (VC6) for MP3codec.
# Jason Hood, 30 January, 2011.

CFLAGS = /nologo /W3 /O2 /MD

MP3codec.dll: MP3codec.obj MP3codec.res
	cl $(CFLAGS) /LD $** /link /base:0x6150000 /filealign:512
