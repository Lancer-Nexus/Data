/*
  Common.h - Declarations for functions imported from Common.dll.

  Jason Hood, 23 March, 2010.
*/

#ifndef _COMMON_H
#define _COMMON_H

#pragma comment( lib, "Common.lib" )

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define EXTERN __declspec(dllimport)


class EXTERN INI_Reader
{
public:
  INI_Reader();
  ~INI_Reader();
  void	 close();
  LPCSTR get_name_ptr();
  bool	 open( LPCSTR, bool = false );
  bool	 read_header();
  bool	 read_value();

private:
  BYTE	 data[0x1568];
};

#endif
