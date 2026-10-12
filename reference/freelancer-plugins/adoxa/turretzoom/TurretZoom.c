/*
  TurretZoom.c - Use the wheel to change the Turret View's camera position.

  Jason Hood, 21 May, 2011.

  v1.10, 24 May, 2011:
  * toggle the sign when going below 10 (or above -10).

  v1.20, 28 May, 2011:
  * multiply by 1.1 (originally 1.5);
  * max out at 200k (originally intended to be 500k, but was actually 500,000k);
  + hold Shift to move 10k,
	 Ctrl to move 1000,
	 Alt to move 100,
	 Shift+Ctrl to move 10;
  + reset on entering Turret View.

  v1.30, 30 May, 2011:
  + hold Ctrl+Alt to move 1;
  + hold Shift+Alt to switch between y (move wheel down) & z (move wheel up);
  + hold all three to change zoom-in camera speed.

  v1.40, 31 May, 2011:
  + hook the update function for smoother movement (thanks w0dk4);
  + allow configuration via dacom.ini.

  v1.41, 5 June, 2011:
  - better routine to find the options.
*/

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <math.h>
#include <stdlib.h>

#define NAKED	__declspec( naked )
#define STDCALL __stdcall


#define ADDR_WHEEL  ((PDWORD)0x4d845c)
#define ADDR_TURRET ((PDWORD)0x54a880)
#define ADDR_UPDATE ((PDWORD)0x5dbd30)


DWORD dummy;
#define ProtectX( addr, size ) \
  VirtualProtect( addr, size, PAGE_EXECUTE_READWRITE, &dummy )
#define ProtectW( addr, size ) \
  VirtualProtect( addr, size, PAGE_READWRITE, &dummy )

#define NEWABS( from, to, org ) \
  org = *(PDWORD)(from); \
  *(PDWORD)(from) = (DWORD)(to)


#define wheel_state  (*(int*)0x61684c)

#define TurretCamera ((float*)0x679064)
#define Y      0				// tether.y
#define Z      1				// tether.z
#define YAW    9				// yaw_rotate_speed
#define PITCH 10				// pitch_rotate_speed
#define ACCEL 11				// accel_speed

#define key_state    (*(int*)0x67c280)
#define SHIFT	     1
#define CTRL	     4
#define ALT	     16

char  options[256] = { 0 };

float ZOOM_MAX	  = 200000;
float ZOOM_SHIFT  = 10000;
float ZOOM_CTRL   = 1000;
float ZOOM_ALT	  = 100;
float ZOOM_S_C	  = 10;
float ZOOM_C_A	  = 1;
float ZOOM_FACTOR_SMALL = 1.1f;
float ZOOM_FACTOR_LARGE = 1.5f;
float ZOOM_FACTOR_SWITCH = 5000;
float SPEED_ADJUST = 0.5f;
int   SPEED_INTERVAL = 10000;
BOOL  SMOOTH = TRUE;
BOOL  INVERSE = TRUE;

float tether_new[2];
float tether_y_org, tether_z_org, yaw_org, pitch_org;
int   speed = 0;
int   tether = 1;


void STDCALL update( float interval )
{
  TurretCamera[Y] += (tether_new[Y] - TurretCamera[Y]) * interval * TurretCamera[ACCEL];
  TurretCamera[Z] += (tether_new[Z] - TurretCamera[Z]) * interval * TurretCamera[ACCEL];
}


NAKED
void update_hook()
{
  __asm {
	push	ecx
	push	edi
	call	update
	pop	ecx
	push	0x51a730
	ret
  }
}


void Adjust_Zoom( int dir )
{
  float dist, factor;
  BOOL	neg;

  switch (key_state)
  {
    default:
      factor = (fabs( tether_new[tether] ) < ZOOM_FACTOR_SWITCH)
	       ? ZOOM_FACTOR_LARGE : ZOOM_FACTOR_SMALL;
      if (dir < 0)
	tether_new[tether] /= factor;
      else
	tether_new[tether] *= factor;
      neg = FALSE;
      goto test_speed;

    case SHIFT:      dist = ZOOM_SHIFT; break;
    case CTRL:	     dist = ZOOM_CTRL;	break;
    case ALT:	     dist = ZOOM_ALT;	break;
    case SHIFT+CTRL: dist = ZOOM_S_C;	break;
    case CTRL+ALT:   dist = ZOOM_C_A;	break;
  }

  neg = (tether_new[tether] < 0);
  if (neg)
    dir *= -1;
  tether_new[tether] += dist * dir;

test_speed:
  if (tether == Y)
    return;

  if (tether_new[Z] < 0)
  {
    // Keep adjusting the speed as you zoom in.
    int spd = -(int)tether_new[Z] / SPEED_INTERVAL + 1;
    if (spd != speed)
    {
      factor = (float)pow( SPEED_ADJUST, spd );
      TurretCamera[YAW]   = yaw_org * factor;
      TurretCamera[PITCH] = pitch_org * factor;
      speed = spd;
    }
  }
  else if (neg)
  {
    TurretCamera[YAW]	= yaw_org;
    TurretCamera[PITCH] = pitch_org;
    speed = 0;
  }
}


void Zoom( void )
{
  if (wheel_state == 0)
    return;

  if (key_state == SHIFT+ALT)
  {
    tether = (wheel_state < 0) ? Y : Z;
    return;
  }

  if (key_state == SHIFT+CTRL+ALT)
  {
    if (tether == Z && tether_new[Z] < 0)
    {
      if (wheel_state < 0)
      {
	TurretCamera[YAW]   *= SPEED_ADJUST;
	TurretCamera[PITCH] *= SPEED_ADJUST;
      }
      else
      {
	TurretCamera[YAW]   /= SPEED_ADJUST;
	TurretCamera[PITCH] /= SPEED_ADJUST;
      }
    }
    return;
  }

  if ((wheel_state < 0) == INVERSE)
  {
    if (tether_new[tether] < 0)
    {
      if (tether_new[tether] > -ZOOM_MAX)
	Adjust_Zoom( 1 );
    }
    else if (key_state == 0 && tether_new[tether] < 1)
    {
      tether_new[tether] *= -1;
      if (tether == Z)
      {
	TurretCamera[YAW]   *= SPEED_ADJUST;
	TurretCamera[PITCH] *= SPEED_ADJUST;
	speed = 1;
      }
    }
    else
    {
      Adjust_Zoom( -1 );
    }
  }
  else
  {
    if (tether_new[tether] >= 0)
    {
      if (tether_new[tether] < ZOOM_MAX)
	Adjust_Zoom( 1 );
    }
    else if (key_state == 0 && tether_new[tether] > -1)
    {
      tether_new[tether] *= -1;
      if (tether == Z)
      {
	TurretCamera[YAW]   = yaw_org;
	TurretCamera[PITCH] = pitch_org;
	speed = 0;
      }
    }
    else
    {
      Adjust_Zoom( -1 );
    }
  }

  if (!SMOOTH)
    TurretCamera[tether] = tether_new[tether];
}


DWORD Wheel_Org, Turret_Org;


NAKED
void Wheel_Hook( void )
{
  __asm {
	mov	eax, ds:[0x674aa0]
	cmp	byte ptr [eax+0x5b9], 0
	jne	turret
	jmp	Wheel_Org
  turret:
	call	Zoom
	pop	edi
	pop	esi
	mov	al, 1
	pop	ebx
	ret	4
  }
}


NAKED
void Turret_Hook( void )
{
  __asm {
	mov	eax, 0x45a740
	call	eax
	test	al, al
	jnz	done
	mov	eax, ds:[0x674aa0]
	cmp	byte ptr [eax+0x5b9], 0
	jne	restore
	mov	esi, ds:[0x679064]
	mov	eax, ds:[0x679068]
	mov	ecx, ds:[0x679088]
	mov	edx, ds:[0x67908c]
	mov	tether_new, esi
	mov	tether_new[4], eax
	mov	tether_y_org, esi
	mov	tether_z_org, eax
	mov	yaw_org, ecx
	mov	pitch_org, edx
	mov	speed, 0
	mov	tether, Z
	jmp	Turret_Org
  restore:
	mov	esi, tether_y_org
	mov	eax, tether_z_org
	mov	ecx, yaw_org
	mov	edx, pitch_org
	mov	ds:[0x679064], esi
	mov	ds:[0x679068], eax
	mov	ds:[0x679088], ecx
	mov	ds:[0x67908c], edx
  done:
	jmp	Turret_Org
  }
}


void Patch( LPSTR opt )
{
  ProtectX( ADDR_WHEEL,  4 );
  ProtectX( ADDR_TURRET, 4 );

  NEWABS( ADDR_WHEEL,  Wheel_Hook,  Wheel_Org );
  NEWABS( ADDR_TURRET, Turret_Hook, Turret_Org );

  if (*opt)
  {
    LPSTR val;
    _strlwr( opt );
    if (strstr( opt, "fast" ))
      SMOOTH = FALSE;
    if (strstr( opt, "inverse" ))
      INVERSE = FALSE;
    if (val = strstr( opt, "max =" ))
      ZOOM_MAX = (float)atof( val+5 );
    if (val = strstr( opt, "shift =" ))
      ZOOM_SHIFT = (float)atof( val+7 );
    if (val = strstr( opt, "ctrl =" ))
      ZOOM_CTRL = (float)atof( val+6 );
    if (val = strstr( opt, "alt =" ))
      ZOOM_ALT	= (float)atof( val+5 );
    if (val = strstr( opt, "s+c =" ))
      ZOOM_S_C	= (float)atof( val+5 );
    if (val = strstr( opt, "c+a =" ))
      ZOOM_C_A	= (float)atof( val+5 );
    if (val = strstr( opt, "small =" ))
      ZOOM_FACTOR_SMALL = (float)atof( val+7 );
    if (val = strstr( opt, "large =" ))
      ZOOM_FACTOR_LARGE = (float)atof( val+7 );
    if (val = strstr( opt, "switch =" ))
      ZOOM_FACTOR_SWITCH = (float)atof( val+8 );
    if (val = strstr( opt, "adjust =" ))
      SPEED_ADJUST = (float)atof( val+8 );
    if (val = strstr( opt, "interval =" ))
      SPEED_INTERVAL = atoi( val+10 );
  }

  if (SMOOTH)
  {
    ProtectW( ADDR_UPDATE, 4 );
    *ADDR_UPDATE = (DWORD)update_hook; // no org, have only one hook
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
    LPSTR opt = options;
    if (!*opt)				// only if nothing was patched in
    {
      // Find the LoadLibrary return address in the stack.
      PDWORD esp = (PDWORD)&hinstDLL + 0x730/4;
      int i = 0, d = 1;
      for (;;)
      {
	if (esp[i] == 0x65b2689)
	{
	  opt = (LPSTR)(esp+i) + 0x2254;
	  opt += strlen( opt ) + 1;	// skip the DLL and its NUL
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
    }
    Patch( opt );
  }

  return TRUE;
}
