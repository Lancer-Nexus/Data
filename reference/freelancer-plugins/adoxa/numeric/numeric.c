/*
  numeric.c - Display hull and shield hit points numerically.

  Jason Hood, 27 October, 2010 (ripped out of FL Hack).

  Install:
    copy to EXE and add an entry to [Libraries] in EXE\dacom.ini.
*/

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define NAKED	__declspec(naked)
#define STDCALL __stdcall


#define ADDR_DAMAGE1 ((PBYTE)0x4ef771)
#define ADDR_DAMAGE2 ((PBYTE)0x4efd8e)


DWORD dummy;
#define ProtectX( addr, size ) \
  VirtualProtect( addr, size, PAGE_EXECUTE_READWRITE, &dummy );

#define RELOFS( from, to ) \
  *(PDWORD)((DWORD)(from)) = (DWORD)(to) - (DWORD)(from) - 4;

#define JMP( from, to ) \
  *(PBYTE)(from) = 0xE9; \
  RELOFS( (DWORD)(from)+1, to )

#define CALL( from, to ) \
  *(PBYTE)(from) = 0xE8; \
  RELOFS( (DWORD)(from)+1, to )

#define CALL1( from, to ) \
  CALL( from, to ); \
  *((PBYTE)(from)+5) = 0x90


void copy_damage();
void display_damage();


void Patch( void )
{
  ProtectX( ADDR_DAMAGE1, 6 );
  ProtectX( ADDR_DAMAGE2, 5 );

  CALL1( ADDR_DAMAGE1, copy_damage );
  JMP(	 ADDR_DAMAGE2, display_damage );
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
    Patch();

  return TRUE;
}
