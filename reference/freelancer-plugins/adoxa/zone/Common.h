/*
  Common.h - Declarations for functions imported from Common.dll.

  Jason Hood, 24 February, 2014.
*/

#ifndef _COMMON_H
#define _COMMON_H

#pragma comment( lib, "Common.lib" )

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define IMPORT __declspec(dllimport)


namespace Universe
{
  struct IZone			// partial definition
  {
    LPVOID vftable;
    UINT   id;
    BYTE   stuff[0x38];
    UINT   flags;
    BYTE   more[0x24];
    float  radius;		// cached value from a virtual call
    BYTE   extra[0x34];
    UINT   ids_name;
  };

  IMPORT const IZone* get_zone( UINT );
}


struct IMPORT FmtStr
{
  UINT something;	// head of type list
  UINT strid;		// resource containing text
  BYTE tnav_marker;	// counters for each type
  BYTE tsystem;
  BYTE tbase;
  BYTE tstring;
  BYTE tgood;
  BYTE tunused;
  BYTE tint;
  BYTE trep_instance;
  BYTE trep_group;
  BYTE tzone_id;
  BYTE tspace_obj_id;
  BYTE tfmt_str;
  BYTE tinstallation;
  BYTE tloot;

  FmtStr() : something( 0 ),
	     strid( 0 ),
	     tnav_marker( 0 ),
	     tsystem( 0 ),
	     tbase( 0 ),
	     tstring( 0 ),
	     tgood( 0 ),
	     tunused( 0 ),
	     tint( 0 ),
	     trep_instance( 0 ),
	     trep_group( 0 ),
	     tzone_id( 0 ),
	     tspace_obj_id( 0 ),
	     tfmt_str( 0 ),
	     tinstallation( 0 ),
	     tloot( 0 )
	     { }
  ~FmtStr();
  void append_zone_id( const UINT& );
  void append_system( const UINT& );
  void begin_mad_lib( UINT );
  void end_mad_lib();
};

#endif
