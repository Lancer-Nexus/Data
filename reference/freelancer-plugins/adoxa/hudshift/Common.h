/*
  Common.h - Declarations for functions imported from Common.dll.

  Jason Hood, 14 June, 2010.
*/

#ifndef _COMMON_H
#define _COMMON_H

#pragma comment( lib, "Common.lib" )

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define IMPORT __declspec(dllimport)


UINT IMPORT CreateID( LPCSTR );


class IMPORT INI_Reader
{
public:
	 INI_Reader();
	~INI_Reader();
  void	 close();
  LPCSTR get_name_ptr();
  UINT	 get_num_parameters() const;
  float  get_value_float( UINT );
  int	 get_value_int( UINT );
  LPCSTR get_value_string( UINT );
  bool	 is_header( LPCSTR );
  bool	 is_value( LPCSTR );
  bool	 is_value_empty( UINT );
  bool	 open( LPCSTR, bool = false );
  bool	 read_header();
  bool	 read_value();
  void	 reset();

private:
  BYTE	 data[0x1568];
};

#endif
