# Weapon muzzle-light runtime A/B — 2026-10-20

## Fixture and package

The QA mission package is built from
`../../../../NAP/QA/weapon-muzzle-mission-qa-20261020/Mission/`, entirely under
`Data/NAP/QA/`. It is NAP content version 7 and contains 159 entries. The
archive was reopened and `VerifyAll()` passed; the active NAP manifest was also
loaded through `NexusPackageFileProvider.LoadActive()` successfully. Runtime
used the staged application at
`Data/NAP/.runtime-test-stage/weapon-muzzle-ab-20261020/application` with no
loose `DATA` directory.

The QA attacker now uses the existing `MSN11_Nomad_Liberty_Light_Fighter`
loadout instead of the cinematic `no_fighter` template. That loadout has three
`li_gun01_mark06` guns. The weapon definition has `flash_radius = 15` and
`light_anim = l_gun01_flash`. The original firing binding is
`USER_FIRE_WEAPONS = -2`, which maps to the right mouse button; that button was
held during the captures.

## Run setup

Both runs used the same NAP package and these settings:

- `--new-game --invulnerable=on --render-dynamic-lighting=on`
- `--render-weapon-muzzle-lights=off` or `on`
- 1280×720, SDL3/OpenGL with Mesa llvmpipe software rendering
- isolated XDG state, data, and config directories for each run

The ignored local NAP source and archive remain at
`NAP/QA/weapon-muzzle-mission-qa-20261020/`; Data intentionally excludes NAP
container contents from Git. The run logs show `Game: Entering system FP7_system`. The automatic
600-second QA explosion trigger did not fire. Laser beams are visible in both captures.

## Captures and debug counters

| Mode | World time at capture | Accepted frame lights | Persistent lights | Effect-light candidates / accepted |
|---|---:|---:|---:|---:|
| Off | 13.85 | 11 / 32 | 3 | 1 / 1 |
| On | 13.03 | 12 / 32 | 3 | 0 / 0 |

Images:

- [Muzzle lights off](muzzle-lights-off.png)
- [Muzzle lights on](muzzle-lights-on.png)

The on capture has one more accepted frame light, but the runs are not
frame-synchronized: world time differs by 0.82 seconds and the off capture has
one accepted effect light while the on capture has none. This moving mission
scene and the low llvmpipe frame rate do not isolate the muzzle-light
contribution. The result supports that both modes launch and that laser fire
was present; it is not a conclusive visual or per-source lighting acceptance.
Repeat with a deterministic firing fixture or source-tagged light counters on
hardware rendering before claiming the muzzle-light runtime path visually
verified.

### Current-build source-counter comparison

A fresh Release build was launched from the same verified NAP app root in two
isolated states. Both used `--new-game --invulnerable=on`, held the right mouse
fire input, and captured after 120 non-cutscene space frames; only
`--render-weapon-muzzle-lights` changed. The scene was Hi02 on llvmpipe. The
Debug overlay reports **0 accepted weapon muzzle lights with the option off**
and **3 with it on**. World time at the post-capture debug screenshots was
19.62 versus 20.28, and player positions differed by about 6 units. The
low-rate software renderer still produces moving, non-pixel-matched views, so
these images verify option gating and accepted source counts, not a calibrated
per-pixel brightness difference.

- [Current build, muzzle lights off](muzzle-lights-budget-off.png)
- [Current build, muzzle lights on](muzzle-lights-budget-on.png)

The clean frame captures and full logs remain in the ignored NAP runtime stage
as `newgame-off2.png`, `newgame-on.png`, `run-newgame-ab-off2.log`, and
`run-newgame-ab-on.log`.

## Explicit-configuration startup check (2026-10-20)

A fresh Release build was launched with an explicit INI path as the first
argument. Its `freelancer_path` points to the isolated app root under
`Data/NAP/.runtime-test-stage/weapon-muzzle-ab-20261020/application-renderer-current`;
`nexus-pack verify-active` passed before launch, and the app root contains no
loose `DATA` directory. With the weapon muzzle-light option off, the log reached
`Finished loading game data`, `UI: Interface loaded`, and `Game: Entering system
Hi02` without the empty-`freelancer_path` error. The log is
`Data/NAP/.runtime-test-stage/weapon-muzzle-ab-20261020/run-explicit-off.log`.
This confirms the explicit-config startup path only; it is not a muzzle-light
visual comparison. The earlier `state-repeat-off` log is from a different,
older run than the later-edited `client-repeat-off.ini` and does not contain the
reported failure.

An attempted capture using `data-on4/Librelancer/AutoSave.fl` restored the
Citiscape base-room scene and its THN cutscene, rather than FP7 space gameplay.
It produced no `--capture-space-frame` image and is excluded from the muzzle
light A/B. That autosave is not a valid space-scene fixture; the A/B still needs
a save or deterministic startup path that enters FP7 directly.

### Long-animation QA fixture (2026-10-20)

To keep the muzzle animation visible during a slow live-toggle capture, a
test-only `fx/Lightanim.ini` was packaged from
`Data/NAP/QA/weapon-light-long-anim-qa-20261020/`. It overrides
`l_gun01_flash` with a constant 60-second frame. The one-entry NAP and the
15-package active snapshot both passed `nexus-pack verify` / `verify-active`;
all package inputs remain under `Data/NAP/`.

The Release client loaded this NAP-only root, reached Hi02, and showed
`render_weapon_muzzle_lights = true`. The Debug counter remained at zero after
the attempted firing input. The run therefore does **not** verify that the
long animation was attached to a fired weapon or that its lighting appeared;
the scene did not provide a deterministic firing trigger. The screenshot is
retained as a negative/inconclusive diagnostic, not as an ON/OFF comparison:
[Hi02 counter remained zero](muzzle-lights-long-anim-qa-hi02-counter-zero.png).

Next, use a deterministic mission/save that spawns the configured QA attacker
and fires its `MSN11_Nomad_Liberty_Light_Fighter` loadout while the Debug overlay
is hidden. Reopen the overlay only after the shot to capture the accepted-light
counter. A fixed-camera A/B and hardware-GPU calibration remain open.

## Artifact hashes

- `mission.nap` v7: `4017494e4379fe90e3aacf476a821d06e0385fe7c21d3b72581e2a26f9511f6e`
- Off image: `23f394bddd5cf6c3fda5029ea7c3cab705d04128dd3b4dc23d94f110729d31dc`
- On image: `bdc4beda0d26d0b5fb7924b5ae79e7014b9eead20b20cad51e31812257ec4b02`
