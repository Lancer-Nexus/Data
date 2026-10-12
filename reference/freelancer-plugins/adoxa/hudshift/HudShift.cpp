/*
  HudShift.cpp - Reposition items in the HUD.

  Jason Hood, 13 to 16 June, 2010.

  v2.00, 19 June, 2010:
  * moved the offsets into the ini file;
  * removed hudshifter.dll, hudshift.dll can be used from either ini.

  v2.10, 28 June, 2011:
  + auto-shift based on ratio;
  + support for main menu.

  v2.11, 7 July, 2011:
  - fix auto-shift when using dacom.ini;
  + shift when changing resolution (from the main menu, otherwise load a game).

  v2.12, 23 October, 2021:
  * allow shifting gauge bars horizontally based on specific screen height.
    E.g.:
      GaugeBars = 0.005
      GaugeBars = 0.004,, 720
      GaugeBars = 0.006,, 960
    will shift 0.004 for 720, 0.006 for 960, otherwise 0.005.
*/


#include "common.h"
#include <stdio.h>
#include <map>
#include <list>

#define EXPORT __declspec(dllexport)
#define NAKED  __declspec(naked)


DWORD dummy;
#define ProtectX( addr, size ) \
  VirtualProtect( (LPVOID)addr, size, PAGE_EXECUTE_READWRITE, &dummy );

#define RELOFS( from, to ) \
  *(PDWORD)(from) = (DWORD)(to) - (DWORD)(from) - 4

#define REL2ABS( addr ) ((DWORD)(addr) + *(PDWORD)(addr) + 4)

#define NEWOFS( from, to ) \
  to##_Old = REL2ABS( from ); \
  RELOFS( from, to##_Hook )


#define ADDR_RES ((PDWORD)(0x424ad4+1))

#define WIDTH  *(int*)0x679bc8
#define HEIGHT *(int*)0x679bcc

#define GAUGEBARS 0x91b7bdcc	// CreateID( "GaugeBars" )


struct Position
{
  float* addr;
  float  scale;
};

typedef std::list<Position> LPosition;
typedef std::list<UINT>     LGroup;

enum { Top = 1, Bottom = 2, Left = 4, Right = 8 };

struct Group
{
  LPosition* xpos;
  LPosition* ypos;
  LGroup*    group;
  int	     location;
};

typedef std::map<UINT, Group> MGroup;

typedef LPosition::const_iterator LPositionCIter;
typedef LGroup::const_iterator	  LGroupCIter;
typedef MGroup::const_iterator	  MGroupCIter;


MGroup groups;


void Shift( const LPosition* pos, float delta )
{
  if (pos == NULL || delta == 0)
    return;

  LPositionCIter iter, end;
  end = pos->end();
  for (iter = pos->begin(); iter != end; ++iter)
    *iter->addr += delta * iter->scale;
}


void Shift( UINT group, float dx, float dy )
{
  MGroupCIter iter = groups.find( group );
  if (iter == groups.end())
    return;

  // Just to make life difficult, the actual status bars use screen coordinates.
  if (group == GAUGEBARS)
  {
    int bar = int(WIDTH * *(double*)0x5d7e60 * *(double*)0x5d7e58);
    *(double*)0x4d56c8 = 0.5f + dx * 1000 / bar;
  }

  Shift( iter->second.xpos, dx );
  Shift( iter->second.ypos, dy );

  if (iter->second.group != NULL)
  {
    LGroupCIter giter, end;
    end = iter->second.group->end();
    for (giter = iter->second.group->begin(); giter != end; ++giter)
      Shift( *giter, dx, dy );
  }
}


void Shift( bool horiz, float delta )
{
  MGroupCIter iter, end;
  end = groups.end();
  for (iter = groups.begin(); iter != end; ++iter)
  {
    if (horiz)
    {
      if (iter->second.location & Left)
	Shift( iter->second.xpos, -delta );
      else if (iter->second.location & Right)
	Shift( iter->second.xpos, delta );
    }
    else
    {
      if (iter->second.location & Top)
	Shift( iter->second.ypos, delta );
      else if (iter->second.location & Bottom)
	Shift( iter->second.ypos, -delta );
    }
  }
}


void Shift()
{
  INI_Reader ini;
  Position   pos;
  Group      group;
  UINT	     nickname;

  if (!ini.open( "../data/interface/hudshift.ini" ))
    return;

  groups.clear();

  // Special handling required for the X offset of the gauge bars.
  ProtectX( (0x4d54cb+2), 4 );
  ProtectX( 0x4d56c8, 4 );
  *(int*)(0x4d54cb+2) = 0x4d56c8;
  *(double*)0x4d56c8 = 0.5;

  // X offset for the ManeuverBar is used in other locations, relocate to filler.
  ProtectX( (0x4d8b5d+2), 4 );
  ProtectX( 0x4d8bec, 4 );
  *(int*)(0x4d8b5d+2) = 0x4d8bec;
  *(float*)0x4d8bec = 0.02f;

  // Y offset for WeaponText & AmmoText uses double, use WeaponNumberText's float.
  ProtectX( 0x4dabb5, 4 );
  *(int*)0x4dabb5 = 0x87682dd8;

  // Main menu text uses double (for the animation), change it to float.
  ProtectX( 0x566630, 1 );
  //ProtectX( 0x566636, 1 );
  //ProtectX( 0x566790, 1 );
  //ProtectX( 0x566796, 1 );
  *(PBYTE)0x566630 =
  *(PBYTE)0x566636 =
  *(PBYTE)0x566790 =
  *(PBYTE)0x566796 = 0xD8;

  while (ini.read_header())
  {
    if (ini.is_header( "Group" ))
    {
      nickname = 0;
      group.xpos = group.ypos = NULL;
      group.group = NULL;
      group.location = 0;
      while (ini.read_value())
      {
	if (ini.is_value( "nickname" ))
	{
	  nickname = CreateID( ini.get_value_string( 0 ));
	}
	else if (ini.is_value( "location" ))
	{
	  LPCSTR loc;
	  for (int i = ini.get_num_parameters(); --i >= 0; )
	  {
	    loc = ini.get_value_string( i );
		 if (stricmp( loc, "top" )    == 0) group.location |= Top;
	    else if (stricmp( loc, "bottom" ) == 0) group.location |= Bottom;
	    else if (stricmp( loc, "left" )   == 0) group.location |= Left;
	    else if (stricmp( loc, "right" )  == 0) group.location |= Right;
	  }
	}
	else if (ini.is_value( "group" ))
	{
	  if (group.group == NULL)
	    group.group = new LGroup;
	  group.group->push_back( CreateID( ini.get_value_string( 0 ) ) );
	}
	else if (ini.is_value( "position" ))
	{
	  pos.scale = (ini.is_value_empty( 4 )) ? 1.0f : ini.get_value_float( 4 );
	  if (!ini.is_value_empty( 0 ))
	  {
	    pos.addr = (float*)strtol( ini.get_value_string( 0 ), NULL, 16 );
	    ProtectX( pos.addr, 4 );
	    *pos.addr = ini.get_value_float( 1 );
	    if (group.xpos == NULL)
	      group.xpos = new LPosition;
	    group.xpos->push_back( pos );
	  }
	  if (!ini.is_value_empty( 2 ))
	  {
	    pos.addr = (float*)strtol( ini.get_value_string( 2 ), NULL, 16 );
	    ProtectX( pos.addr, 4 );
	    *pos.addr = ini.get_value_float( 3 );
	    if (group.ypos == NULL)
	      group.ypos = new LPosition;
	    group.ypos->push_back( pos );
	  }
	}
      }
      groups[nickname] = group;
    }
  }

  ini.reset();
  while (ini.read_header())
  {
    if (ini.is_header( "HUDShift" ))
    {
      while (ini.read_value())
      {
	float dx = ini.is_value_empty( 0 ) ? 0.0f : ini.get_value_float( 0 );
	float dy = ini.is_value_empty( 1 ) ? 0.0f : ini.get_value_float( 1 );
	if (ini.is_value( "Horizontal" ))
	{
	  if (dx == 0)
	  {
	    // 0.3825 just happens to be the constant found from 16:9 & 16:10.
	    dx = ((float)WIDTH / HEIGHT - 4.0f / 3) * 0.3825f;
	  }
	  Shift( true, dx );
	}
	else if (ini.is_value( "Vertical" ))
	{
	  Shift( false, dx );
	}
	else
	{
	  UINT group = CreateID( ini.get_name_ptr() );
	  if (group != GAUGEBARS || ini.is_value_empty( 2 ) ||
	      ini.get_value_int( 2 ) == HEIGHT)
	    Shift( group, dx, dy );
	}
      }
    }
  }

  ini.close();
}


// Shift on changing resolution.

DWORD Resolution_Old;

NAKED
void Resolution_Hook()
{
  Shift();
  __asm jmp	Resolution_Old
  __asm align	16
}


struct IDLL
{
  virtual void whatever( int, LPVOID ) { }
};


extern "C" {

EXPORT
LPVOID CreateInstance( LPVOID a1, LPCSTR a2, LPVOID a3 )
{
  Shift();
  return new IDLL;
}


EXPORT
void DestroyInstance( LPVOID a1 )
{
  RELOFS( ADDR_RES, Resolution_Old );
}

} // "C"


void Patch()
{
  ProtectX( ADDR_RES, 4 );
  NEWOFS( ADDR_RES, Resolution );
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
    Patch();

  return TRUE;
}
