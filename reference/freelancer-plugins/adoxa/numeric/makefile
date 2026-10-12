# MinGW/NASM makefile for Numeric.

CC = gcc
CFLAGS = -O2 -Wall

numeric.dll: numeric.o numerica.o numericr.o
	$(CC) -mwindows -shared $^ -s -o $@ $(LIBS)

numerica.o: numeric.nsm
	nasm -w-orphan-labels -O9 -f coff $< -o $@

numericr.o: numeric.rc
	windres $< $@
