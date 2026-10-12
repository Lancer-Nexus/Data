/*
  Freelancer uses the "advanced" MP3 codec from Fraunhofer, which comes with 9X
  and XP, but Vista/7 install with the "decode only" version, resulting in
  numerous "missing MP3 codec" spew warnings.  However, Vista/7 include the
  "professional" version (also available for XP via WMP11), which can be
  installed manually (e.g.: http://www.looprecorder.de/tut_l3codec.php).  This
  plugin tests for a custom codec via environment variable "FL_MP3", then any
  of the Fraunhofer ones.

  Jason Hood, 30 January, 2011.

  v1.10, 5 March, 2014:
  * hook the enumerator, test all Fraunhofer variations;
  - hook SoundStreamer.dll, too.

  v1.11, 14 March, 2022:
  - get base addresses.

  v1.12, 31 May, 2023:
  - use base address in JMP.

  Install:
    Copy MP3CODEC.DLL to the EXE directory and add it to the [Libraries]
    section of EXE\dacom.ini.
*/


#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define NAKED	 __declspec(naked)
#define FASTCALL __fastcall

#define ADDR_SM (0x6ee8ca0 - 0x6ee0000) 	// SoundManager
#define ADDR_SS (0x6ef3f50 - 0x6ef0000) 	// SoundStreamer


DWORD dummy;
#define ProtectX( addr, size ) \
  VirtualProtect( addr, size, PAGE_EXECUTE_READWRITE, &dummy )

#define RELOFS( from, to ) \
  *(PDWORD)(from) = (DWORD)(to) - (DWORD)(from) - 4

#define JMP( from, to ) \
  *(PBYTE)(from) = 0xe9; \
  RELOFS( (DWORD)from+1, to )


static int priority;
static PBYTE retaddr;


int FASTCALL Enum( const char* desc )
{
  static char name[/*ACMDRIVERDETAILS_LONGNAME_CHARS*/460];
  static int  user_codec = -1;

  if (user_codec == -1)
    user_codec = GetEnvironmentVariable( "FL_MP3", name, sizeof(name) );

  if (user_codec)
    if (memcmp( desc, name, user_codec + 1 ) == 0)
      return 0;

  if (memcmp( desc, "Fraunhofer IIS MPEG Layer-3 Codec", 33 ) == 0)
  {
    // There's probably only one installed, but just in case.
    if (memcmp( desc + 33, " (professional)", 16 ) == 0)
      return 1;
    if (memcmp( desc + 33, " (advanced plus)", 17 ) == 0)
      return 2;
    if (memcmp( desc + 33, " (advanced)", 12 ) == 0)
      return 3;
    if (memcmp( desc + 33, " (basic)", 9 ) == 0)
      return 4;
    if (memcmp( desc + 33, " (lite)", 8 ) == 0)
      return 5;
    if (memcmp( desc + 33, " (decode only)", 15 ) == 0)
      return 6;
    return 7;
  }

  return 999;
}


NAKED
void Enum_Hook( void )
{
  __asm {
	cmp	dword ptr [edi+4], 0
	jne	e1
	inc	dword ptr [edi+4]
	mov	priority, 999
  e1:
	mov	ecx, esi
	call	Enum
	cmp	eax, priority
	jae	done
	mov	priority, eax
	mov	[edi+4], ebp
  done:
	jmp	retaddr
	align	16
  }
}


void Patch( void )
{
  PBYTE addr_sm, addr_ss;

  addr_sm = (PBYTE)GetModuleHandle( "SoundManager.dll" ) + ADDR_SM;
  addr_ss = (PBYTE)GetModuleHandle( "SoundStreamer.dll" ) + ADDR_SS;

  retaddr = addr_sm + 0x2d;	// also works for SS

  ProtectX( addr_sm, 5 );
  ProtectX( addr_ss, 5 );

  JMP( addr_sm, Enum_Hook );
  JMP( addr_ss, Enum_Hook );
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
    Patch();

  return TRUE;
}
