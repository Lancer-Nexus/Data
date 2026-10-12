/*
  ranks.cpp - Add a name to your current level.

  Jason Hood, 15 & 16 August, 2010.

  Uses new file MISSIONS\ranks.ini to assign a name to a range of levels.  The
  names are stored as string resources inside the plugin itself.  The format
  string replaces "%%d" (two percents!) with the level number and "%s" (one
  percent!) with the name.  There are two ways to assign a rank to levels:
  "next_rank = LEVEL[, ID]" and/or "set_ranks = INTERVAL, COUNT[, ID]".  The
  former starts the next rank from LEVEL; the latter creates ranks at INTERVAL
  levels, for COUNT ranks.  Use [SP Ranks] to set the ranks for single player
  and [MP Ranks] for multiplayer.  There may be multiple [MP Ranks], each
  containing multiple "group" values for each faction using these ranks.  The
  "format" value can be used to reuse an existing format string;
  "first_rank_id" explicitly sets the initial id.  By default, the format will
  use the next id and the first rank will follow format.

  For example:

	 [SP Ranks]
	 ; format = 0		; implied
	 ; first_rank_id = 1	; implied
	 set_ranks = 5, 6	; 1..5 = 1, 6..10 = 2, 11..15 = 3,
				; 16..20 = 4, 21..25 = 5, 26..
	 next_rank = 32 	; ..31 = 6, 32..
	 next_rank = 38 	; ..37 = 7, 38+ = 8

	 [MP Ranks]
	 ; format = 9
	 ; first_rank_id = 10
	 ; group = player	; if not affiliated, or faction not defined
	 next_rank = 5		; 1..4 = 10, 5..
	 set_ranks = 5, 5	; ..9 = 11, 10..14 = 12, 15..19 = 13,
				; 20..24 = 14, 25..29 = 15, 30+ = 16

  There are also two options, defined in the [Rank Settings] section.
  Normally, groups not defined will use the default ("player") ranks; add
  "just_levels" to only show the level number.  If you have a rank that is too
  long for the window, define an "offset" value to shift the status display
  left a bit to make extra room.  The offset is divided by 100 and subtracted
  from 0.38 (the default).  E.g.: "offset = 8" will be 0.38 - 8 / 100 = 0.30.
*/

#include "Common.h"
#include <vector>
#include <map>

#define NAKED	__declspec(naked)
#define STDCALL __stdcall

#define lenof(a) (sizeof(a) / sizeof(*(a)))


// The position of the stats.
#define ADDR_OFFSET ((float*)(0x4a7fd6+4))

// The format string to use.
#define ADDR_FORMAT ((PBYTE)0x4a8a9d)


DWORD dummy;
#define ProtectX( addr, size ) \
  VirtualProtect( addr, size, PAGE_EXECUTE_READWRITE, &dummy );

#define RELOFS( from, to ) \
  *(PDWORD)(from) = (DWORD)(to) - (DWORD)(from) - 4;

#define CALL( from, to ) \
  *(PBYTE)(from) = 0xe8; \
  RELOFS( (DWORD)from+1, to )


HMODULE g_hinst;


struct LevelId
{
  int  level;
  UINT id;
};

typedef std::vector<LevelId> Rank;

struct Ranks
{
  UINT format;
  Rank rank;
};

typedef std::map<UINT, Ranks*> Group;

Group group;
bool  just_levels;


bool Init()
{
  INI_Reader ini;
  // Assume "data path = ..\data".
  if (!ini.open( "..\\data\\missions\\Ranks.ini" ))
    return false;

  LevelId lid;
  UINT	  grp;

  lid.id = 0;
  while (ini.read_header())
  {
    if (ini.is_header( "SP Ranks" ))
    {
      grp = 0;
    }
    else if (ini.is_header( "MP Ranks" ))
    {
      grp = -1;
    }
    else
    {
      if (ini.is_header( "Rank Settings" ))
      {
	while (ini.read_value())
	{
	  if (ini.is_value( "offset" ))
	  {
	    *ADDR_OFFSET = 0.38f - ini.get_value_float( 0 ) / 100;
	  }
	  else if (ini.is_value( "just_levels" ))
	  {
	    just_levels = true;
	  }
	}
      }
      continue;
    }

    Ranks* ranks = new Ranks;
    ranks->format = lid.id++;
    lid.level = 1;
    ranks->rank.push_back( lid );
    ++lid.id;

    while (ini.read_value())
    {
      if (ini.is_value( "format" ))
      {
	lid.id = ini.get_value_int( 0 );
	ranks->format = lid.id++;
	ranks->rank.begin()->id = lid.id++;
      }
      else if (ini.is_value( "first_rank_id" ))
      {
	lid.id = ini.get_value_int( 0 );
	ranks->rank.begin()->id = lid.id++;
      }
      else if (ini.is_value( "next_rank" ))
      {
	lid.level = ini.get_value_int( 0 );
	if (!ini.is_value_empty( 1 ))
	  lid.id = ini.get_value_int( 1 );
	ranks->rank.push_back( lid );
	++lid.id;
      }
      else if (ini.is_value( "set_ranks" ))
      {
	int interval = ini.get_value_int( 0 );
	int count = ini.get_value_int( 1 );
	if (!ini.is_value_empty( 2 ))
	  lid.id = ini.get_value_int( 2 );
	while (count--)
	{
	  lid.level += interval;
	  ranks->rank.push_back( lid );
	  ++lid.id;
	}
      }
      else if (ini.is_value( "group" ))
      {
	if (grp == 0)
	  continue;
	LPCSTR fac = ini.get_value_string( 0 );
	if (stricmp( fac, "player" ))
	  grp = -1;
	else
	  grp = MakeId( fac );
	group[grp] = ranks;
      }
    }

    if (grp == 0 || grp == -1)
      group[grp] = ranks;
  }

  return true;
}


NAKED
UINT Affiliation()
{
  __asm {
	mov	eax, 0x4c4670
	call	eax
	push	eax
	push	-1
	mov	eax, esp
	push	0
	push	eax
	add	eax, 4
	push	eax
	call	ds:[0x5c6320]		// Reputation::Vibe::GetAffiliation
	pop	eax
	pop	eax
	pop	eax
	pop	eax
	pop	ecx
	ret
  }
}


LPCWSTR STDCALL RankName( int level )
{
  static WCHAR buf[128];
	 WCHAR fmt[128], name[128];
  Ranks* ranks;

  if (level == 0)
    level = 1;

  UINT grp = (SinglePlayer()) ? 0 : Affiliation();
  Group::const_iterator iter = group.find( grp );
  if (iter == group.end())
  {
    if (grp == 0 || just_levels || group.find( -1 ) == group.end())
      return (LPCWSTR)0x5d0ec4; // L"%d"
    ranks = group[-1];
  }
  else
  {
    ranks = iter->second;
  }

  int rank = ranks->rank.size();
  while (level < ranks->rank[--rank].level)
    ;

  LoadStringW( g_hinst, ranks->format, fmt, lenof(fmt) );
  LoadStringW( g_hinst, ranks->rank[rank].id, name, lenof(name) );
  _snwprintf( buf, lenof(buf), fmt, name );
  return buf;
}


NAKED
void Rank_Hook()
{
  __asm {
	push	eax
	call	RankName
	pop	ecx
	push	eax
	jmp	ecx
  }
}


void Patch()
{
  ProtectX( ADDR_OFFSET, 4 );
  ProtectX( ADDR_FORMAT, 5 );

  if (!Init())
    return;

  CALL( ADDR_FORMAT, Rank_Hook );
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
  {
    g_hinst = hinstDLL;
    Patch();
  }

  return TRUE;
}
