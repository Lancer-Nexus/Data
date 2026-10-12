/*
  storyfactions.cpp - Patch Freelancer to define the story factions.

  Jason Hood, 23 March, 2010.

  The story factions are those that are excluded from the reputation list.  This
  plugin overrides the defaults and reads them from DATA\storyfactions.ini.

  v1.01, 25 April, 2026:
  - get Common.dll's base address (thanks BC46).
*/


#include "Common.h"
#include <vector>

#define NAKED	__declspec(naked)
#define STDCALL __stdcall


std::vector<LPCSTR> factions;


// Read in ..\DATA\storyfactions.ini and make the necessary patches to
// the memory of common.dll.
void Patch()
{
  #define OFFSET10 (0x631f800 - 0x6260000 + common)
  #define OFFSET11 (0x631f930 - 0x6260000 + common)

  #define OFFSET10_VALUE (0x63ec5d8 - 0x6260000 + common)
  #define OFFSET11_VALUE (0x63ed5d8 - 0x6260000 + common)

  DWORD offset;
  DWORD common = (DWORD)GetModuleHandle( "common.dll" );

  if (*(DWORD*)(OFFSET11+1) == OFFSET11_VALUE)
    offset = OFFSET11;
  else if (*(DWORD*)(OFFSET10+1) == OFFSET10_VALUE)
    offset = OFFSET10;
  else
    return;

  INI_Reader ini;
  // Let's just assume "data path = ..\data".
  if (!ini.open( "..\\data\\storyfactions.ini" ))
    return;

  ini.read_header();
  while (ini.read_value())
    factions.push_back( strdup( ini.get_name_ptr() ) );

  ini.close();

  if (!factions.empty())
  {
    DWORD dummy;
    VirtualProtect( (LPVOID)offset, 0x575, PAGE_EXECUTE_READWRITE, &dummy );
    factions.push_back( NULL );
    *(DWORD*)(offset+0x001) =
    *(DWORD*)(offset+0x00a) =
    *(DWORD*)(offset+0x4e2) =
    *(DWORD*)(offset+0x530) =
    *(DWORD*)(offset+0x571) = (DWORD)factions.begin();
  }
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
    Patch();

  return TRUE;
}
