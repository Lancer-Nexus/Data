/*
  Territory.cpp - Patch Freelancer to customise system entry message.

  Jason Hood, 18 to 24 August & 2 September, 2009.

  v1.01, 21 February, 2010:
  * caps setting will also apply to tradelane exit.

  v1.02, 21 February, 2014:
  * allow multiline format strings.

  v1.03, 9 February, 2024:
  * define the function at 0x5A0E30 (4 May, 2019);
  - copy only what was allocated.

  Freelancer's territory names (as in "New York System, LIBERTY Space.") are
  hardcoded into Freelancer.exe, based on the system resource numbers.	This is
  a patch to add additional territories, by adding a library to DACOM.ini and
  reading DATA\UNIVERSE\Territory.ini, which is of the form:

	[Settings]
	caps = false	 ; don't force the message to upper case
	codepage = UTF-8 ; the default is ANSI, may also be OEM, MAC or number

	; Define a house and the systems that use it.
	[Houses]
	; Change the message, either specifying it directly, or by its resource
	; number.  The first %s will be replaced with the system, the second
	; with the house.  Maximum length of 63 characters.
	format	  = %s System, %s Territory.
	format	  = %s System^%s Territory	; ^ indicates a new line
	format_id = number

	; No need to create a resource, the house can be named directly.
	house = name

	; The first number is the resource id of the house; the second allows a
	; separate name for the Nav Map.  The Nav Map has to be a resource
	; number, so the first number is optional if you use the house value.
	house_id = [number][, number]

	; The system(s) that belong to the house.  This value can be repeated.
	systems = system[-system][, ...]

	; Add the house to the Nav Map.  The coordinates are the same as the
	; pos value for the systems.  Font will default to SubHeader; see
	; DATA\FONTS\fonts.ini for the list, or to add your own.
	NavMap = X, Y[, font]

	; Repeat for each house you want to add.

	; Define a general format for systems, where the %s is replaced by the
	; system name (it's optional, allowing the system to have a different
	; name in space).  Maximum length of 63 characters.
	[Systems]
	format	  = %s System, Independent.
	format_id = number
	systems   = system[-system][, ...]

	; Repeat for each format you want to add.

  The house and format strings are expected to be encoded according to the
  supplied code page.  Systems can be specified as a resource number (strid_name
  in DATA\UNIVERSE\universe.ini) or a nickname.  The dash represents a range of
  numbers, which can be shortened to just the changed digits (thus "196609-13"
  is the same as "196609-196613").  Nicknames can also have a range (like
  "Li01-5").  See the supplied territory.ini for an example.
*/


#include "Common.h"
#include <map>
#include <vector>

#define NAKED	__declspec(naked)
#define STDCALL __stdcall


UINT codepage;

struct TTer
{
  int res;
  int fmt;
};

typedef std::map<int, TTer> TerritoryMap;
TerritoryMap territories;

typedef std::vector<LPCWSTR> StringStore;
StringStore store;

TTer	ter;
LPCWSTR nam, fmt;


struct NavMapData
{
  int	 res;
  float  x, y;
  LPCSTR font;
};

typedef std::vector<NavMapData> NavMapVec;
NavMapVec  NavMap;
NavMapData nm;
LPVOID* buffer;
LPVOID* my_buffer;


// Given the hash or resource number, see if there's a definition for it.
bool STDCALL find_territory( int id )
{
  TerritoryMap::const_iterator t = territories.find( id );
  if (t == territories.end())
    return false;

  ter = t->second;
  if (ter.res < 0)
    nam = store[~ter.res];
  if (ter.fmt < 0)
    fmt = store[~ter.fmt];

  return true;
}


// Determine if the system is defined, adjust the message if so.
NAKED
void Territory_Patch()
{
  __asm {
	push	ds:[0x673354]		// call 0x4c4830/push eax
        call	find_territory		// try nickname hash first
        test	al, al
        jnz	gotit
        push	ebx			// now the resource number
        call	find_territory
        test	al, al
        jnz	gotit
        lea	eax, [ebx-0x30001]
        push	0x45b026
        ret

  gotit:
        mov	eax, ter.res
        test	eax, eax
        jz	sys
        js	tp1
        cmp	ter.fmt, 0
        jnz	tp1
        mov	ebp, eax		// resource number of the house
        push	0x45b057		// do the normal house routine
        ret

  tp1:
        push	esi			// need to duplicate the original code
        push	edi			//  in order to use the new string(s)
        lea	edi, [esp+0xC+8]
        mov	esi, ds:[0x67ECA8]	// resource structure
        mov	ebp, 0x4347e0		// get string resource function
        mov	ecx, 0x40		// Freelancer uses 0x80, which I think
        cmp	ter.fmt, 0		//  is a bug, since that's all it
        jl	cpyhfmt 		//  subtracts from the stack
        push	ecx
        push	edi
        push	ter.fmt
        jnz	hid
        mov	dword ptr [esp], 0x55E	// "%s System, %s Space."
  hid:
        push	esi
        call	ebp
        add	esp, 0x10
        jmp	hsys
  cpyhfmt:
        push	esi
        mov	esi, fmt
	call	cpy
        pop	esi
  hsys:
        cmp	ter.res, 0
        jl	cpyhnam
        pop	edi
        sub	esp, 0x10		// set up the expected stack
        mov	ebp, ter.res
        push	0x45b083
        ret
  cpyhnam:
        mov	eax, ds:[0x6119F8]	// size of buffer
        shr	eax, 1			// in wide characters
        push	eax
        push	0x66DC60
        lea	edi, [eax*2+0x66DC60]
        push	ebx			// system resource number
        push	esi
        call	ebp
        add	esp, 0x10
        mov	esi, nam
        push	edi
	call	cpy
        pop	esi			// ESI points to the new string
        pop	edi
        sub	esp, 0x30		// set up the expected stack
        push	0x45b0bf
        ret

  sys:
        mov	eax, ter.fmt
        lea	ecx, [esp+0xC]
        test	eax, eax
        jl	cpysfmt
        push	0x40
        push	ecx
        push	eax			// new format resource number
        mov	edx, ds:[0x67ECA8]
        push	0x45b108
        ret

  cpysfmt:
        push	esi
        push	edi
        mov	esi, fmt		// copy the format to the buffer
        mov	edi, ecx
	call	cpy
        pop	edi
        pop	esi
        sub	esp, 0x10		// set up the expected stack
        push	0x45b10e
	ret

  cpy:
	lodsw
	stosw
	test	ax, ax
	jnz	cpy
	ret
  }
}


struct Vector
{
  float x, y, z;
};

class TextControl
{
public:
  virtual void m00(); virtual void m04(); virtual void m08(); virtual void m0C();
  virtual void m10(); virtual void m14(); virtual void m18(); virtual void m1C();
  virtual void m20(); virtual void m24(); virtual void m28(); virtual void m2C();
  virtual void m30(); virtual void m34(); virtual void m38(); virtual void m3C();
  virtual void m40(); virtual void m44(); virtual void m48(); virtual void m4C();
  virtual void m50(); virtual void m54(); virtual void m58(); virtual void m5C();
  virtual void m60(); virtual void m64(); virtual void m68(); virtual void m6C();
  virtual void m70(); virtual void m74(); virtual void m78(); virtual void m7C();
  virtual void m80(); virtual void m84(); virtual void m88(); virtual void m8C();
  virtual void m90(); virtual void m94(); virtual void m98(); virtual void m9C();
  virtual void mA0(); virtual void mA4();

  virtual void mA8( int cmd, int arg1, int arg2 = 0 );
};

enum
{
  ALIGN_LEFT,
  ALIGN_CENTER,
  ALIGN_RIGHT
};

typedef TextControl* (__fastcall *fnCreateTextControl)(
    LPVOID thisptr, int dummy,
    LPCSTR id, LPCSTR font, const Vector& pos, LPCSTR hardpoint,
    float size_x, float size_y, float size_z,
    UINT resid, int align, UINT tip, bool center );

fnCreateTextControl CreateTextControl = (fnCreateTextControl)0x5A0E30;


void STDCALL navmap_houses( LPVOID thisptr )
{
  NavMapVec::iterator iter, end;
  int items = 0;
  Vector pos;

  pos.z = 0;
  end = NavMap.end();
  for (iter = NavMap.begin(); iter != end; ++iter)
  {
    pos.x = iter->x;
    pos.y = iter->y;
    TextControl* tc = CreateTextControl(
			  thisptr, 0,
			  NULL, iter->font, pos, NULL,
			  0.132f, 0.03f, 1.9f,
			  iter->res, ALIGN_LEFT, 0, true );
    tc->mA8( 1, 1 );
    my_buffer[items++] = tc;
  }
}


// Hook in code to add houses to the Nav Map.
NAKED
void NavMap_Patch1()
{
  __asm {
	push	ebp
	call	navmap_houses

        push	1
        push	esi
        push	1

        push	0x4904c9
	ret
  }
}


NAKED
void NavMap_Patch2()
{
  __asm {
        push	ecx

        lea	esi, [esp+0xc0+4]
        mov	edi, buffer
        mov	ecx, 33
        rep	movsd

        pop	ecx
        push	0x492944
	ret
  }
}


NAKED
void NavMap_Patch3()
{
  __asm {
        call	dword ptr [edx+0xA8]

        mov	ebx, my_buffer
        mov	ecx, [ebx]
        test	ecx, ecx
        jz	done
  nxt:
        mov	edx, [ecx]
        push	0
        push	1
        push	1
        call	dword ptr [edx+0xA8]
        mov	ecx, [ebx+4]
        add	ebx, 4
        test	ecx, ecx
        jnz	nxt

  done:
        push	0x49480c
	ret
  }
}


NAKED
void NavMap_Patch4()
{
  __asm {
        call	dword ptr [edx+0xA8]

        mov	edi, my_buffer
        mov	ecx, [edi]
        test	ecx, ecx
        jz	done
  nxt:
        mov	edx, [ecx]
        push	ebx
        lea	eax, [esp+0x14]
        push	eax
        push	0x33
        call	dword ptr [edx+0xA8]
        mov	ecx, [edi+4]
        add	edi, 4
        test	ecx, ecx
        jnz	nxt

  done:
        push	0x495d75
	ret
  }
}


NAKED
void NavMap_Patch5()
{
  __asm {
        mov	edi, my_buffer
        mov	ecx, [edi]
        test	ecx, ecx
        jz	done
  nxt:
        mov	eax, [ecx]
        push	ebx
        lea	edx, [esp+0x14+4]
        push	edx
        push	0x33
        call	dword ptr [eax+0xA8]
        mov	ecx, [edi+4]
        add	edi, 4
        test	ecx, ecx
        jnz	nxt

  done:
        mov	eax, ds:[0x679bb0]
        ret
  }
}


NAKED
void NavMap_Patch6()
{
  __asm {
        call	dword ptr [edx+0xA8]

        mov	edi, my_buffer
        mov	ecx, [edi]
        test	ecx, ecx
        jz	done
  nxt:
        mov	edx, [ecx]
        push	1
        lea	eax, [esp+0x14]
        push	eax
        push	0x33
        call	dword ptr [edx+0xA8]
        mov	ecx, [edi+4]
        add	edi, 4
        test	ecx, ecx
        jnz	nxt

  done:
        push	0x496119
        ret
  }
}


NAKED
void NavMap_Patch7()
{
  __asm {
        call	dword ptr [edx+0xA8]

        mov	edi, my_buffer
        mov	ecx, [edi]
        test	ecx, ecx
        jz	done
  nxt:
        mov	edx, [ecx]
        push	ebx
        push	1
        push	1
        call	dword ptr [edx+0xA8]
        mov	ecx, [edi+4]
        add	edi, 4
        test	ecx, ecx
        jnz	nxt

  done:
        push	0x497cb1
        ret
  }
}


NAKED
void NavMap_Patch8()
{
  __asm {
        call	dword ptr [eax+0xA8]

        mov	edi, my_buffer
        mov	ecx, [edi]
        test	ecx, ecx
        jz	done
  nxt:
        mov	eax, [ecx]
        push	0
        push	1
        push	1
        call	dword ptr [eax+0xA8]
        mov	ecx, [edi+4]
        add	edi, 4
        test	ecx, ecx
        jnz	nxt

  done:
        push	0x49e4ab
        ret
  }
}


NAKED
void NavMap_Patch9()
{
  __asm {
        call	dword ptr [edx+0xA8]

        mov	edi, my_buffer
        mov	ecx, [edi]
        test	ecx, ecx
        jz	done
  nxt:
        mov	edx, [ecx]
        push	0
        push	0
        push	1
        call	dword ptr [edx+0xA8]
        mov	ecx, [edi+4]
        add	edi, 4
        test	ecx, ecx
        jnz	nxt

  done:
        push	0x49e7e9
        ret
  }
}


NAKED
void NavMap_Patch10()
{
  __asm {
        call	dword ptr [eax+0xA8]

        mov	edi, my_buffer
        mov	ecx, [edi]
        test	ecx, ecx
        jz	done
  nxt:
        mov	eax, [ecx]
        push	0
        push	0
        push	1
        call	dword ptr [eax+0xA8]
        mov	ecx, [edi+4]
        add	edi, 4
        test	ecx, ecx
        jnz	nxt

  done:
        push	0x4a037e
        ret
  }
}


// Convert the string to wide and store it, returning the NOT of its index.
int stows( LPCSTR s, bool nl = true )
{
  int pos = ~store.size();

  int len = MultiByteToWideChar( codepage, 0, s, -1, 0, 0 );
  if (len > 1)
  {
    if (len > 64)
      len = 64;
    LPWSTR ws = new WCHAR[len];
    MultiByteToWideChar( codepage, 0, s, -1, ws, len );
    ws[len-1] = '\0';
    if (nl)
      while (--len >= 0)
	if (ws[len] == '^')
	  ws[len] = '\n';
    store.push_back( ws );
  }
  else
    pos = 0;

  return pos;
}


// Yeah, I know, I should be using a class...
static int  range_pos, range_last;
static char range_string[128];
static int  range_nn;

// Convert S to a number, returning it and leaving S pointing to the character
// that stopped conversion.  Assumes no leading or trailing space.
int get_num( LPCSTR& s )
{
  for (int num = 0;; ++s)
  {
    if (*s < '0' || *s > '9')
      return num;
    num = num * 10 + *s - '0';
  }
}

// Get the first number in the range of numbers represented by S.  It is of the
// form NUMBER or FIRST-LAST or STRINGNN-MM; anything else is treated as a
// nickname.  LAST and MM may be shortened to just the changed digits (eg:
// "196609-13" is the same as "196609-196613" and "Li01-5" is the same as
// "Li01-05"; however, "Li01-Li05" will be treated as an invididual nickname).
int get_first_range( LPCSTR s )
{
  *range_string = '\0';
  range_last = 0;

  LPCSTR n = s;
  range_pos = get_num( s );
  if (s != n)
  {
    if (*s == '\0')
      return range_pos;

    int prefix = s - n;
    if (*s == '-' && prefix <= 10)
    {
      char buf[32];
      prefix -= strlen( ++s );
      if (prefix > 0)
      {
	sprintf( buf, "%.*s%s", prefix, n, s );
	s = buf;
      }
      range_last = get_num( s );
      if (*s == '\0' && range_last >= range_pos)
	return range_pos;
    }
  }

  LPCSTR d = strchr( n, '-' );
  int len = (d) ? d - n : 0;
  if (len < 3 || len >= sizeof(range_string) ||
      d[-1] < '0' || d[-1] > '9' || d[-2] < '0' || d[-2] > '9')
  {
    return CreateID( n );
  }
  range_pos  = (d[-2] - '0') * 10 + d[-1] - '0';
  range_last = get_num( ++d );
  if (*d || range_last < range_pos)
    return CreateID( n );

  range_nn = len - 1;
  memcpy( range_string, n, len );
  range_string[len] = '\0';
  return CreateID( range_string );
}


int get_next_range()
{
  if (++range_pos > range_last)
    return 0;

  if (*range_string)
  {
    if (++range_string[range_nn] > '9')
    {
      range_string[range_nn] = '0';
      ++range_string[range_nn-1];
    }
    return CreateID( range_string );
  }

  return range_pos;
}


// Read system resource numbers or nicknames from each parameter, storing the
// territory for each one.
void set_territories( INI_Reader& ini )
{
  for (int i = ini.get_num_parameters(); --i >= 0;)
  {
    int id = get_first_range( ini.get_value_string( i ) );
    while (id)
    {
      territories[id] = ter;
      id = get_next_range();
    }
  }
}


// Read in ..\DATA\UNIVERSE\territory.ini and make the necessary patches to
// the memory of Freelancer.exe.
void Patch()
{
  #define ADDR_NL1	((PWORD)0x45ac3e)
  #define ADDR_NL2	((PBYTE)0x45acb1)
  #define ADDR_CAPS3	((PBYTE)0x45af5a+1)
  #define ADDR_SPACE	((PBYTE)0x45b020)
  #define ADDR_CAPS1	((PBYTE)0x45b0d8+1)
  #define ADDR_CAPS2	((PBYTE)0x45b142+1)
  #define ADDR_CAPS4	((PBYTE)0x45b278+1)
  #define ADDR_LI	((PBYTE)0x490358)
  #define ADDR_BR	((PBYTE)0x4903b4)
  #define ADDR_KU	((PBYTE)0x490410)
  #define ADDR_RH	((PBYTE)0x49046c)
  #define ADDR_NAVMAP1	((PBYTE)0x4904c4)
  #define ADDR_NAVMAP2	((PBYTE)0x49293d)
  #define ADDR_NAVMAP2a ((PBYTE)0x4932fe)
  #define ADDR_NAVMAP3	((PBYTE)0x494806)
  #define ADDR_NAVMAP4	((PBYTE)0x495d6f)
  #define ADDR_NAVMAP5	((PBYTE)0x495eb1)
  #define ADDR_NAVMAP6	((PBYTE)0x496113)
  #define ADDR_NAVMAP7	((PBYTE)0x497cab)
  #define ADDR_NAVMAP8	((PBYTE)0x49e4a5)
  #define ADDR_NAVMAP9	((PBYTE)0x49e7e3)
  #define ADDR_NAVMAP10 ((PBYTE)0x4a0315)

  DWORD dummy;

  INI_Reader ini;
  // Let's just assume "data path = ..\data".
  if (!ini.open( "..\\data\\universe\\territory.ini" ))
    return;

  #define VirtualProtectX( addr, size ) \
    VirtualProtect( addr, size, PAGE_EXECUTE_READWRITE, &dummy )

  VirtualProtectX( ADDR_LI, ADDR_NAVMAP1 + 5 - ADDR_LI );

  while (ini.read_header())
  {
    ter.res = ter.fmt = 0;
    if (ini.is_header( "Houses" ))
    {
      while (ini.read_value())
      {
	if (ini.is_value( "house" ))
	{
	  ter.res = stows( ini.get_value_string(), false );
	}
	else if (ini.is_value( "house_id" ))
	{
	  if (ini.is_value_empty( 0 ))
	    nm.res = ini.get_value_int( 1 );
	  else
	  {
	    ter.res = ini.get_value_int( 0 );
	    nm.res = ini.is_value_empty( 1 ) ? ter.res : ini.get_value_int( 1 );
	  }
	}
	else if (ini.is_value( "format" ))
	{
	  ter.fmt = stows( ini.get_value_string() );
	}
	else if (ini.is_value( "format_id" ))
	{
	  ter.fmt = ini.get_value_int( 0 );
	}
	else if (ini.is_value( "systems" ))
	{
	  if (ter.res)
	    set_territories( ini );
	}
	else if (ini.is_value( "NavMap" ))
	{
	  if (nm.res)
	  {
	    nm.x    = ini.get_value_float( 0 ) *  0.0272f - 0.2090f;
	    nm.y    = ini.get_value_float( 1 ) * -0.0272f + 0.2010f;
	    nm.font = (ini.is_value_empty( 2 )) ? (LPCSTR)0x5d01a8 // SubHeader
		      : strdup( ini.get_value_string( 2 ) );
	    switch (ter.res)
	    {
	      case 1249:
		*(int*)   (ADDR_LI+0x01) = nm.res;
		*(float*) (ADDR_LI+0x2a) = nm.x;
		*(float*) (ADDR_LI+0x32) = nm.y;
		*(LPCSTR*)(ADDR_LI+0x1b) = nm.font;
	      break;
	      case 1250:
		*(int*)   (ADDR_BR+0x01) = nm.res;
		*(float*) (ADDR_BR+0x2a) = nm.x;
		*(float*) (ADDR_BR+0x32) = nm.y;
		*(LPCSTR*)(ADDR_BR+0x1b) = nm.font;
	      break;
	      case 1251:
		*(int*)   (ADDR_KU+0x01) = nm.res;
		*(float*) (ADDR_KU+0x2a) = nm.x;
		*(float*) (ADDR_KU+0x32) = nm.y;
		*(LPCSTR*)(ADDR_KU+0x1b) = nm.font;
	      break;
	      case 1252:
		*(int*)   (ADDR_RH+0x01) = nm.res;
		*(float*) (ADDR_RH+0x0e) = nm.x;
		*(float*) (ADDR_RH+0x16) = nm.y;
		*(LPCSTR*)(ADDR_RH+0x33) = nm.font;
	      break;
	      default:
		NavMap.push_back( nm );
	      break;
	    }
	    nm.res = 0;
	  }
	}
      }
    }
    else if (ini.is_header( "Systems" ))
    {
      while (ini.read_value())
      {
	if (ini.is_value( "format" ))
	{
	  ter.fmt = stows( ini.get_value_string() );
	}
	else if (ini.is_value( "format_id" ))
	{
	  ter.fmt = ini.get_value_int( 0 );
	}
	else if (ini.is_value( "systems" ))
	{
	  if (ter.fmt)
	    set_territories( ini );
	}
      }
    }
    else if (ini.is_header( "Settings" ))
    {
      while (ini.read_value())
      {
	if (ini.is_value( "caps" ))
	{
	  if (!ini.get_value_bool( 0 ))
	  {
	    VirtualProtectX( ADDR_CAPS3, 1 );
	    VirtualProtectX( ADDR_CAPS1, ADDR_CAPS4 - ADDR_CAPS1 + 1 );
	    *ADDR_CAPS1 = *ADDR_CAPS2 = *ADDR_CAPS3 = *ADDR_CAPS4 = 0x5E;
	  }
	}
	else if (ini.is_value( "codepage" ))
	{
	  LPCSTR cp = ini.get_value_string( 0 );
	  if (stricmp( cp, "UTF-8" ) == 0)
	    codepage = CP_UTF8;
	  else if (stricmp( cp, "ANSI" ) == 0)
	    codepage = CP_ACP;
	  else if (stricmp( cp, "OEM" ) == 0)
	    codepage = CP_OEMCP;
	  else if (stricmp( cp, "MAC" ) == 0)
	    codepage = CP_MACCP;
	  else
	    codepage = ini.get_value_int( 0 );
	}
      }
    }
  }
  ini.close();

  #define JUMP( from, to ) \
    *from = 0xE9;\
    *(DWORD*)(from+1) = (PBYTE)to - from - 5

  #define CALL( from, to ) \
    *from = 0xE8;\
    *(DWORD*)(from+1) = (PBYTE)to - from - 5

  if (!territories.empty())
  {
    VirtualProtectX( ADDR_SPACE, 5 );
    JUMP( ADDR_SPACE, Territory_Patch );
    VirtualProtectX( ADDR_NL1, 2 );
    //VirtualProtectX( ADDR_NL2, 14 );
    *ADDR_NL1 = 0x71eb;
    memcpy( ADDR_NL2, "\x8B\x80\x34\x03\x00\x00"        // mov eax, [eax+334]
		      "\xC6\x40\x30\x01"                // mov [eax+30], 1
		      "\x8B\x06\xEB\x81", 14 );
  }

  if (!NavMap.empty())
  {
    VirtualProtectX( ADDR_NAVMAP2,  5 );
    VirtualProtectX( ADDR_NAVMAP3,  5 );
    VirtualProtectX( ADDR_NAVMAP4,  5 );
    VirtualProtectX( ADDR_NAVMAP5,  5 );
    VirtualProtectX( ADDR_NAVMAP6,  5 );
    VirtualProtectX( ADDR_NAVMAP7,  5 );
    VirtualProtectX( ADDR_NAVMAP8,  5 );
    VirtualProtectX( ADDR_NAVMAP9,  5 );
    VirtualProtectX( ADDR_NAVMAP10, 5 );

    JUMP( ADDR_NAVMAP1,  NavMap_Patch1	);
    JUMP( ADDR_NAVMAP2,  NavMap_Patch2	);
    JUMP( ADDR_NAVMAP3,  NavMap_Patch3	);
    JUMP( ADDR_NAVMAP4,  NavMap_Patch4	);
    CALL( ADDR_NAVMAP5,  NavMap_Patch5	);
    JUMP( ADDR_NAVMAP6,  NavMap_Patch6	);
    JUMP( ADDR_NAVMAP7,  NavMap_Patch7	);
    JUMP( ADDR_NAVMAP8,  NavMap_Patch8	);
    JUMP( ADDR_NAVMAP9,  NavMap_Patch9	);
    JUMP( ADDR_NAVMAP10, NavMap_Patch10 );

    VirtualProtectX( ADDR_NAVMAP2a, 7 );
    ADDR_NAVMAP2a[0] = 0x90;
    ADDR_NAVMAP2a[1] = 0x90;
    ADDR_NAVMAP2a[2] = 0xBE;
    *(LPVOID*)(ADDR_NAVMAP2a+3) = buffer = new LPVOID[33 + NavMap.size() + 1];
    my_buffer = buffer + 33;
    my_buffer[NavMap.size()] = 0;
  }
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
    Patch();

  return TRUE;
}
