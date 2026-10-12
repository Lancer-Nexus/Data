/*
  Common.h - Declarations for functions imported from Common.dll.

  Jason Hood, 16 August, 2010.
*/

#ifndef _COMMON_H
#define _COMMON_H

#pragma comment( lib, "Common.lib" )

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define IMPORT __declspec(dllimport)


IMPORT USHORT MakeId( LPCSTR );
IMPORT bool   SinglePlayer();


class IMPORT INI_Reader
{
public:
	 INI_Reader();
	~INI_Reader();
  void	 close();
  float  get_value_float( UINT );
  int	 get_value_int( UINT );
  LPCSTR get_value_string( UINT );
  bool	 is_header( LPCSTR );
  bool	 is_value( LPCSTR );
  bool	 is_value_empty( UINT );
  bool	 open( LPCSTR, bool = false );
  bool	 read_header();
  bool	 read_value();

private:
  BYTE	 data[0x1568];
};

#endif
