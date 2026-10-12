/*
  Hail.c - Implement the key for Hail.

  Jason Hood, 22 May, 2013.

  Install:
    Copy HAIL.DLL to the EXE directory and add it to the [Libraries] section of
    EXE\dacom.ini.  Add an entry for USER_RADIO (after USER_STATUS) in
    DATA\INTERFACE\keylist.ini to see it in the options (as "RADIO").
*/

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#define NAKED	__declspec(naked)
#define STDCALL __stdcall


#define ADDR_TIP	((PBYTE)(0x4e13ad+1))
#define ADDR_BUTTON	((PDWORD)(0x4e1415+1))
#define ADDR_KEY	((PDWORD)(0x51d7f6+1))


DWORD dummy;
#define ProtectX( addr, size ) \
  VirtualProtect( addr, size, PAGE_EXECUTE_READWRITE, &dummy );

#define RELOFS( from, to ) \
  *(PDWORD)(from) = (DWORD)(to) - (DWORD)(from) - 4

#define REL2ABS( addr ) ((DWORD)(addr) + *(PDWORD)(addr) + 4)

#define NEWOFS( from, to ) \
  to##_Old = REL2ABS( from ); \
  RELOFS( from, to##_Hook )


DWORD Button_Old, Key_Old;
DWORD button_ptr, button_this;


NAKED
void Button_Hook( void )
{
  __asm {
	pop	ebp
	call	Button_Old
	mov	button_ptr, eax
	mov	button_this, esi
	jmp	ebp
	align	16
  }
}


NAKED
void Key_Hook( void )
{
  __asm {
	cmp	[esp+0x28+4+4+4], 0x5c	// USER_RADIO
	jne	done
	push	0
	push	button_ptr
	push	0x26
	mov	ecx, button_this
	mov	eax, 0x4e19e0
	call	eax
  done:
	jmp	Key_Old
	align	16
  }
}


void Patch()
{
    ProtectX( ADDR_TIP,    1 );
  //ProtectX( ADDR_BUTTON, 4 );
    ProtectX( ADDR_KEY,    4 );

  // Add the key to the button creation, so it shows up in brackets.
  *ADDR_TIP = 0x5c;

  NEWOFS( ADDR_BUTTON, Button );
  NEWOFS( ADDR_KEY,    Key );
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
    Patch();

  return TRUE;
}
