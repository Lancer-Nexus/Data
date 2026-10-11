/*
  Common.h - Declarations for functions imported from Common.dll.

  Jason Hood, 19 August, 2009.
*/

#ifndef _COMMON_H
#define _COMMON_H

#pragma comment( lib, "Common.lib" )

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define EXTERN __declspec(dllimport)


UINT EXTERN CreateID( LPCSTR );


class EXTERN INI_Reader
{
public:
  INI_Reader();
  ~INI_Reader();
  void	 close();
  UINT	 get_num_parameters() const;
  bool	 get_value_bool( UINT );
  float  get_value_float( UINT );
  int	 get_value_int( UINT );
  LPCSTR get_value_string( UINT );
  LPCSTR get_value_string();
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
