/*
  WheelScroll.cpp - Scroll some windows using the mouse wheel.

  Jason Hood, 16 & 17 February, 2016.

  v1.10, 4 July, 2021:
  + scroll in space, when the cursor is the arrow;
  + support reputation, contact list, weapon list.

  v1.11, 5 July, 2021:
  - actually scroll in space (fixed the code, didn't compile it);
  + support trade routes, scanner and repair.

  v1.12, 6 December, 2024:
  + support chat history & player list.

  Install:
	Copy WheelScroll.dll to your EXE directory and add it to the
	[Libraries] section of dacom.ini.
*/

#include "patch.h"


#define ADDR_CHATCONTROL_WHEEL	0x5CFB0C    // Chat history
#define ADDR_LOADSAVE_WHEEL	0x5D1DA4    // Load or Save Game
#define ADDR_NAVMAP_WHEEL	0x5D2FCC    // waypoints
#define ADDR_KEY_WHEEL		0x5D4AA4    // key list
#define ADDR_TEXT_WHEEL 	0x5E47B4    // info, stats, log
#define ADDR_CTRL_WHEEL 	0x5E4F6C    // text control
#define ADDR_SERVER_WHEEL	0x5E5164    // servers
#define ADDR_UISCROLLTABLE_WHEEL 0x5E5294   // broadcast & private chat lists
#define ADDR_SCROLL_WHEEL	0x5E55F4    // scroll bar
#define ADDR_DESC_WHEEL 	0x5E591C    // server description
#define ADDR_LOAD_WHEEL 	0x5E5CFC    // Load Game (from the main menu)
#define ADDR_LIST_WHEEL 	0x5E6194    // inventory, jobs, news
#define ADDR_WHEEL		((PDWORD)0x4d845c)  // in space

#define CURRENT_CURSOR		((LPCSTR)0x616858)  // pointer to length & string


struct Scroll
{
  BYTE	x1[0x6C];
  BYTE	flags;
  BYTE	x2[0x3B8-0x6D];
  int	dir;
  float delay;
};

#define VISIBLE 2


struct Window
{
  PVOID   vftable;
  Window* parent;
  Window* win1;
  Window* win2; 	// next/prev/sibling/something...
  char*   type;
  int	  name_len;
  char	  name[32];

  bool	  Wheel( int dir );
};

struct
{
  LPCSTR name;
  DWORD  offset;
}
windows[] =
{
  { "HUD_ContactList",    0x3D4 },
  { "HUD_Status",         0x58C },
  { "NeuroNetNavMap",     0xAE0 },
  { "NN_CommodityByBase", 0x348 },
  { "NN_Dealer",          0x3D0 },
  { "NN_Inventory",       0x3D0 },
  { "NN_LoadSave",        0x1758 },
  { "NN_MissionVendor",   0x428 },
  { "NN_News",            0x648 },
  { "NN_PlayerInfo",      0x394 },
  { "NN_Preferences",     0x4B8 },
  { "NN_Repair",          0x46C },
  { "NN_Scanner",         0x3D0 },
};

#define Text_Scroll	0x3F0
#define Load_Scroll	0xD4
#define Server_Scroll	0xC8
#define Base_Scroll	0xFC4


typedef void (FASTCALL *ScrollUpdate)( Scroll* );


bool Window::Wheel( int dir )
{
  for (Window* win = this; win != NULL; win = win->parent)
  {
    int ofs = -1;

    if (win->type != NULL &&
	strcmp( win->type, "UIScroll" ) == 0)
    {
      ofs = 0;
    }
    else if (win->type != NULL &&
	     (strcmp( win->type, "RichTextWin" ) == 0 ||
	      strcmp( win->type, "UIRichTextWin" ) == 0))
    {
      ofs = Text_Scroll;
    }
    else if (strcmp( win->name, "CharSelDesc" ) == 0 ||
	     strcmp( win->name, "CharSelTime" ) == 0)
    {
      win = win->parent;
      ofs = Load_Scroll;
    }
    else if (strcmp( win->name, "ServerTable" ) == 0)
    {
      win = win->parent;
      ofs = Server_Scroll;
    }
    else if (strncmp( win->name, "NavMapBase", 10 ) == 0 ||
	     strcmp( win->name, "NavMapSystemTitleText" ) == 0)
    {
      win = win->parent;
      ofs = Base_Scroll;
    }
    else if (strcmp( win->name, "ChatControl" ) == 0)
    {
      win = win->win2->win2;	// MsgWin, UIScroll
      if (win == NULL)
	return false;
      ofs = 0;
    }
    else if (win->type != NULL && strcmp( win->type, "UIScrollTable" ) == 0)
    {
      win = win->win2;	// UIScroll
      if (win == NULL)
	return false;
      ofs = 0;
    }
    else
    {
      for (int i = 0; i < sizeof(windows) / sizeof(*windows); ++i)
      {
	if (strcmp( win->name, windows[i].name ) == 0)
	{
	  ofs = windows[i].offset;
	  break;
	}
      }
    }
    if (ofs >= 0)
    {
      Scroll* scroll = (ofs == 0) ? (Scroll*)win : ((Scroll**)win)[ofs / 4];
      if (scroll != NULL && (scroll->flags & VISIBLE))
      {
	scroll->dir = (dir < 0) ? 1 : 0;
	scroll->delay = -1;
	((ScrollUpdate)0x597560)( scroll );
	scroll->delay = -1;
	((ScrollUpdate)0x597560)( scroll );
	scroll->dir = -1;
	return true;
      }
      if (ofs == 0)
	break;
    }
  }

  return false;
}


DWORD Wheel_Old;

NAKED
void Wheel_Hook( void )
{
  __asm {
	mov	eax, ds:[0x616858]	// current cursor
	test	eax, eax
	jz	thrust
	cmp	dword ptr [eax], 5	// length of "arrow"
	jne	thrust
	mov	eax, [eax+4]
	or	eax, 0x20202020
	cmp	eax, 'orra'             // I'll assume the 'w'
	jne	thrust
	pop	edi			// it's the arrow cursor, pass the
	pop	esi			//  wheel along
	mov	al, 0
	pop	ebx
	ret	4
  thrust:
	jmp	Wheel_Old
	align	16
  }
}


void Patch()
{
  ProtectW( (PDWORD)ADDR_CHATCONTROL_WHEEL, 4 );
  ProtectW( (PDWORD)ADDR_LOADSAVE_WHEEL,    4 );
  ProtectW( (PDWORD)ADDR_NAVMAP_WHEEL,	    4 );
  ProtectW( (PDWORD)ADDR_KEY_WHEEL,	    4 );
  ProtectW( (PDWORD)ADDR_TEXT_WHEEL,	    4 );
  //ProtectW( (PDWORD)ADDR_CTRL_WHEEL,	    4 );
  ProtectW( (PDWORD)ADDR_SERVER_WHEEL,	    4 );
  //ProtectW( (PDWORD)ADDR_UISCROLLTABLE_WHEEL, 4 );
  //ProtectW( (PDWORD)ADDR_SCROLL_WHEEL,    4 );
  //ProtectW( (PDWORD)ADDR_DESC_WHEEL,	    4 );
  //ProtectW( (PDWORD)ADDR_LOAD_WHEEL,	    4 );
  ProtectW( (PDWORD)ADDR_LIST_WHEEL,	    4 );

  typedef bool (Window::*FWheel)( int );
  *(FWheel*)ADDR_CHATCONTROL_WHEEL =
  *(FWheel*)ADDR_LOADSAVE_WHEEL    =
  *(FWheel*)ADDR_NAVMAP_WHEEL	   =
  *(FWheel*)ADDR_KEY_WHEEL	   =
  *(FWheel*)ADDR_TEXT_WHEEL	   =
  *(FWheel*)ADDR_CTRL_WHEEL	   =
  *(FWheel*)ADDR_SERVER_WHEEL	   =
  *(FWheel*)ADDR_UISCROLLTABLE_WHEEL =
  *(FWheel*)ADDR_SCROLL_WHEEL	   =
  *(FWheel*)ADDR_DESC_WHEEL	   =
  *(FWheel*)ADDR_LOAD_WHEEL	   =
  *(FWheel*)ADDR_LIST_WHEEL	   = Window::Wheel;

  ProtectX( ADDR_WHEEL, 4 );
  NEWABS( ADDR_WHEEL, Wheel );
}


BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
{
  if (fdwReason == DLL_PROCESS_ATTACH)
    Patch();

  return TRUE;
}
