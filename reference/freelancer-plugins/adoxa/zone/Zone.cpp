/*
  Zone.cpp - Display a message on entering and leaving a named zone.

  Jason Hood, 24 to 28 February, 2014.

  Use the "arrival" text (what you see on entering a system or exiting a trade-
  lane) to indicate that you have entered or left a named zone (i.e. one with
  ids_name).  The messages can be customised by editing the resources within
  the DLL; they use the same format as OfferBribeResources (but it will use
  ids_name if those don't exist), i.e. "%Z" as name (e.g. "Badlands") or "%Zv1"
  as noun (e.g. "the Badlands").  It may also include "%S" for the current
  system.  In the case that you enter a system within a zone, the system
  message will show first, then the zone.  If you are in more than one zone,
  all will be shown, in decreasing size.  If any zone is marked as dangerous
  (property_flags has bits 3, 4 or 5 set), all zones will show in a different
  color (low in yellow, medium in orange, high in red; these can be changed by
  adding "low=RRGGBB medium=RRGGBB high=RRGGBB ultra=RRGGBB" to the DLL line;
  "ultra" is medium & high).  Add "upper" to the DLL line to force upper case.

  v1.10, 9 March, 2014:
  * keep track of all zones;
  * ignore zones whose name is a single space (some tradelanes);
  * use %Z for non-vanilla zones even when Names is not installed.

  v1.11, 18 March, 2015:
  - fix show_left test for DBCS strings;
  - not showing left message would not display entered message again.

  v1.12, 27 May, 2015:
  * ignore zones whose ids_name is 60245 (tradelanes);
  * don't show messages for a zone having the same name as another zone.

  v1.20, 17 October, 2022:
  * use options for the colors;
  + "upper" option to force the message to upper case.

  Install:
	Copy Zone.dll to EXE and add it to [Libraries] in EXE\dacom.ini.
*/


#include "Common.h"
#include <set>
#include <algorithm>

#define NAKED	 __declspec(naked)
#define FASTCALL __fastcall
#define STDCALL  __stdcall


#define ADDR_TEST	((PDWORD)(0x41d02d+2))
#define ADDR_NAME	((PDWORD)(0x41d057+1))
#define ADDR_NL1	((PWORD)  0x45ac3e)
#define ADDR_NL2	((PBYTE)  0x45acb1)
#define ADDR_ZONE	((PBYTE)  0x51ce64)
#define ADDR_SYS	((PDWORD)(0x554686+1))
#define ADDR_RSRC	((PDWORD)(0x5b1cb2+1))


DWORD dummy;
#define ProtectX( addr, size ) \
  VirtualProtect( addr, size, PAGE_EXECUTE_READWRITE, &dummy );

#define RELOFS( from, to ) \
  *(PDWORD)(from) = (DWORD)(to) - (DWORD)(from) - 4

#define REL2ABS( addr ) ((DWORD)(addr) + *(PDWORD)(addr) + 4)

#define NEWOFS( from, to ) \
  to##_Old = REL2ABS( from ); \
  RELOFS( from, to##_Hook )

#define CALL( from, to ) \
  *(PBYTE)(from) = 0xE8; \
  RELOFS( (DWORD)from+1, to )


DWORD danger_col[] = { 0xff00ffff, 0xff007fff, 0xff0000ff, 0xff0000ff };

typedef Universe::IZone* PIZone;
typedef std::set<PIZone> ZoneSet;
typedef ZoneSet::const_iterator ZoneSetCI;

ZoneSet z, z0;
bool	blank;
bool	show_left;
bool	upper;
UINT	sys_id;

HMODULE g_hinst;
UINT	rsrcid;
DWORD	Resource_Old, Name_Old, Sys_Old;


NAKED
UINT FASTCALL FmtStr_sprintf( FmtStr& str, LPWSTR buf, UINT size )
{
  __asm {
	mov	eax, 0x41c970
	push	dword ptr [esp+4]
	push	edx
	call	eax
	ret	4
  }
}


NAKED
bool FASTCALL DisplayZone( UINT flags )
{
  __asm {
	// Wait for an existing message to be removed.
	mov	eax, ds:[0x66d398]
	test	eax, eax
	jz	dz
	xor	eax, eax
	ret
  dz:
	push	ebx
	mov	ebx, ecx
	mov	eax, 0x59db20
	push	0
	push	0
	push	0x5ce83c		// "NN_ArrivalText"
	push	0x5ce83c
	call	eax
	add	esp, 0x10
	mov	eax, ds:[0x66d398]
	test	eax, eax
	jz	done
	mov	dword ptr [eax+0x334], 0x3e800000 // 0.25
	mov	ecx, [eax+0x32c]
	mov	edx, [ecx]
	push	ecx
	push	edx
	push	0
	push	0x66fc60
	push	0x1d
	call	dword ptr [edx+0xa8]
	pop	edx
	pop	ecx
	and	ebx, 0x38
	jz	done
	and	bl, 0x30
	shr	bl, 2
	push	1
	add	ebx, offset danger_col
	push	ebx
	push	0x33
	call	dword ptr [edx+0xa8]
  done:
	mov	al, 1
	pop	ebx
	ret
  }
}


void FASTCALL get_zone( UINT id )
{
  Universe::get_zone( id );
}


NAKED
void Test_Hook()
{
  __asm {
	mov	edx, 0x41d040
	lea	esi, [eax+0x3fc58]	// outside Freelancer's range, so use
	jmp	edx			//  ids_name rather than nothing
	align	16
  }
}


NAKED
void Name_Hook()
{
  __asm {
	pop	ebx			// retrieve return address

	push	ecx
	push	eax
	push	esi
	push	edx
	call	Name_Old
	add	esp, 0x10
	cmp	esi, 60245		// ignore tradelane zone description
	je	done
	test	eax, eax
	jnz	ok
	mov	ecx, [edi+4]
	call	get_zone
	mov	eax, [eax+0xa0] 	// Zone ids_name
	mov	[esp+4], eax
	call	Name_Old
  ok:	cmp	eax, 1
	jne	done
	mov	ecx, [esp+8]		// buffer pointer is unchanged
	cmp	word ptr [ecx], ' '
  done: sete	blank
	jmp	ebx
  }
}


// Sort zones by their radius, placing larger zones first.
bool std::less<PIZone>::operator()( const PIZone& z1, const PIZone& z2 ) const
{
  return z1->radius > z2->radius;
}


struct Find_Name
{
  PIZone zone;

  Find_Name( PIZone z ) : zone( z ) { }

  operator()( PIZone z )
  {
    return zone->ids_name == z->ids_name;
  }
};


void STDCALL Zone( PIZone zone, bool in_zone, UINT idx, UINT total )
{
  if (idx == 0)
    z.clear();

  if (in_zone)
    z.insert( zone );

  if (idx == total - 1)
  {
    if (z != z0)
    {
      UINT   flags = 0;
      LPWSTR buf = (LPWSTR)0x66fc60;
      UINT   size = *(UINT*)0x6119f8;
      UINT   len = 0, wr;
      bool   left = false;
      if (sys_id == *(PUINT)0x673354)
      {
	for (ZoneSetCI iter = z0.begin(); iter != z0.end(); ++iter)
	{
	  Find_Name name( *iter );
	  if (std::find_if( z.begin(), z.end(), name ) == z.end())
	  {
	    FmtStr msg;
	    if (len)
	      buf[len++] = '\n';
	    msg.begin_mad_lib( rsrcid + 1 );
	    msg.append_zone_id( (*iter)->id );
	    msg.append_system( sys_id );
	    msg.end_mad_lib();
	    wr = FmtStr_sprintf( msg, buf + len, size - len );
	    if (!blank)
	    {
	      if (!show_left)
	      {
		left = true;
		break;
	      }
	      len += wr;
	    }
	  }
	}
      }
      for (ZoneSetCI iter = z.begin(); iter != z.end(); ++iter)
      {
	Find_Name name( *iter );
	if (std::find_if( z0.begin(), z0.end(), name ) == z0.end())
	{
	  FmtStr msg;
	  if (len)
	    buf[len++] = '\n';
	  msg.begin_mad_lib( rsrcid );
	  msg.append_zone_id( (*iter)->id );
	  msg.append_system( *(PUINT)0x673354 );
	  msg.end_mad_lib();
	  wr = FmtStr_sprintf( msg, buf + len, size - len );
	  if (!blank)
	    len += wr;
	  flags |= (*iter)->flags;
	}
      }
      if (len)
      {
	buf[len] = '\0';
	if (upper)
	  CharUpperW( buf );
      }
      if ((len && DisplayZone( flags )) || (!len && left))
      {
	z0 = z;
	sys_id = *(PUINT)0x673354;
      }
    }
  }
}


NAKED
void Zone_Hook()
{
  __asm {
	mov	bl, al

	xor	eax, eax
	cmp	[esi+0xa0], eax 	// Zone ids_name
	je	done

	lea	eax, [esp+0x20]
	push	0			// distance from zone
	push	eax			// ship position
	call	dword ptr [edx+0x34]	// ECX & EDX still set

  done:
	push	dword ptr [esp+0x2050]	// number of zones
	push	edi			// zone index
	push	eax			// in this zone?
	push	esi			// zone
	call	Zone

	test	bl, 0x81
	ret
  }
}


void reset()
{
  z0.clear();
}


NAKED
void Sys_Hook()
{
  __asm {
	call	reset
	jmp	Sys_Old
	align	16
  }
}


NAKED
void Resource_Hook()
{
  __asm {
	mov	eax, ds:[0x67c404]	// get the number of our resource
	sub	eax, ds:[0x67c400]
	shl	eax, 14
	mov	rsrcid, eax
	mov	eax, 0x57d800
	push	g_hinst
	call	eax
	add	esp, 4
	jmp	Resource_Old
	align	16
  }
}


void parse_color( LPSTR opt, LPCSTR col, int i )
{
  DWORD rgb;
  int len = strlen( col );
  LPSTR val = strstr( opt, col );
  if (!val || val[len] != ' ' || val[len+1] != '=')
    return;
  rgb = strtol( val + len + 2, NULL, 16 );
  danger_col[i] = 0xFF000000 | ((rgb & 0xFF) << 16) | (rgb & 0xFF00) | (rgb >> 16);
}


void Patch( LPSTR opt )
{
  ProtectX( ADDR_TEST, 4 );
  //ProtectX( ADDR_NAME, 4 );
  ProtectX( ADDR_NL1,  2 );
  //ProtectX( ADDR_NL2, 14 );
  ProtectX( ADDR_ZONE, 5 );
  ProtectX( ADDR_SYS,  4 );
  ProtectX( ADDR_RSRC, 4 );

  CALL(   ADDR_ZONE, Zone_Hook );
  NEWOFS( ADDR_RSRC, Resource );
  NEWOFS( ADDR_NAME, Name );
  NEWOFS( ADDR_SYS,  Sys );

  if (*ADDR_TEST == 0xFFFFF9C2) 	// may have already been patched, in
    RELOFS( ADDR_TEST, Test_Hook );	//  which case there should be no need

  // Allow multiple lines of arrival text, to display more than one zone.
  *ADDR_NL1 = 0x71EB;
  memcpy( ADDR_NL2, "\x8B\x80\x34\x03\x00\x00"  // mov eax, [eax+334]
		    "\xC6\x40\x30\x01"          // mov [eax+30], 1
		    "\x8B\x06\xEB\x81", 14 );

  // Test if the left message actually exists.
  char test[4];
  if (LoadString( g_hinst, 1, test, 4 ) && *test)
    show_left = true;

  if (opt && *opt)
  {
    if (strstr( opt, "upper" ))
      upper = true;
    parse_color( opt, "low", 0 );
    parse_color( opt, "medium", 1 );
    parse_color( opt, "high", 2 );
    parse_color( opt, "ultra", 3 );
  }
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
  {
    // Process options by reading the line stored from dacom.ini.  The ini
    // parser strips comments and adds spaces around equal signs; the DLL parser
    // stops at the first space/tab.  The entire line is MAX_PATH chars
    // (including NUL).
    LPSTR opt = NULL;
    // Find the LoadLibrary return address in the stack.
    DWORD dacom = 0x65b2689 - 0x65b0000 + (DWORD)GetModuleHandle( "dacom.dll" );
    PDWORD esp = (PDWORD)&hinstDLL + 0x730/4;
    int i = 0, d = 1;
    for (;;)
    {
      if (esp[i] == dacom)
      {
	opt = (LPSTR)(esp+i) + 0x2254;
	opt += strlen( opt ) + 1;	// skip the DLL and its NUL
	_strlwr( opt );
	break;
      }
      i += d;
      if (i == 256)
      {
	i = d = -1;
      }
      else if (i == -256)
      {
	break;
      }
    }
    g_hinst = hinstDLL;
    Patch( opt );
  }

  return TRUE;
}
