#!/usr/bin/env python3
"""Reproduziert fehlende Datei-Verweise aus SDK-INIs gegen Freelancer-Daten."""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SDK = REPO / "SDK"
NAP = REPO / "NAP"

# Dateitypen, die in den Data-Konfigurationen als Datei-Verweise vorkommen.
REFERENCE_EXTENSIONS = (
    "ini", "3db", "cmp", "sur", "mat", "txm", "tga", "bmp", "wav", "utf",
    "thn", "ale", "pte", "anm", "vms", "sph", "dfm", "wmv", "page", "db",
)
REFERENCE_RE = re.compile(
    r"(?i)([^\s,=;]+\.(?:" + "|".join(REFERENCE_EXTENSIONS) + r"))\b"
)
WINDOWS_ABSOLUTE_RE = re.compile(r"(?i)^(?:[a-z]:/|//)")


def canonical(path: str) -> str | None:
    """Normalize an INI path without allowing traversal above the virtual root."""
    path = path.strip().strip("\"'").replace("\\", "/")
    if WINDOWS_ABSOLUTE_RE.match(path) or path.startswith("/"):
        return None
    normalized = posixpath.normpath(path).casefold()
    if normalized == ".." or normalized.startswith("../"):
        return None
    return normalized.removeprefix("./")


def sdk_ini_files() -> list[Path]:
    return sorted(
        path for path in SDK.rglob("*")
        if path.is_file()
        and path.suffix.casefold() == ".ini"
        and path.relative_to(SDK).parts[0].casefold() != "exe"
    )


def retail_asset_path(path: Path, data_root: Path) -> str:
    """Mirror build_nap.py's destination naming for one unpacked CD asset."""
    rel = path.relative_to(data_root).as_posix().casefold()
    match = re.fullmatch(r"solar/planets/(planet_[^/]+)/\1\.mat", rel)
    if match:
        return f"solar/planets/{match.group(1)}.mat"
    match = re.fullmatch(r"solar/planets/detailmaps/(detailmap_[^/]+\.txm)", rel)
    if match:
        return f"solar/planets/{match.group(1)}"
    parent, _, name = rel.rpartition("/")
    name = name.replace(" ", "_")
    return f"{parent}/{name}" if parent else name


def virtual_files(*, nap_root: Path | None, data_root: Path | None) -> set[str]:
    files: set[str] = set()
    if nap_root is not None:
        if not nap_root.is_dir():
            raise ValueError(f"NAP-Verzeichnis nicht gefunden: {nap_root}")
        # NAP/<Klasse> ist je ein Container; der Klassenname gehört nicht zum
        # virtuellen Pfad, daher werden die Klassenordner als separate Roots gelesen.
        for class_dir in sorted(p for p in nap_root.iterdir() if p.is_dir()):
            for path in class_dir.rglob("*"):
                if path.is_file() and path.name != ".gitkeep":
                    files.add(path.relative_to(class_dir).as_posix().casefold())
    if data_root is not None:
        if not data_root.is_dir():
            raise ValueError(f"DATA-Verzeichnis nicht gefunden: {data_root}")
        for path in data_root.rglob("*"):
            if path.is_file() and path.suffix.casefold() != ".ini":
                files.add(retail_asset_path(path, data_root))
    # SDK-INIs werden von sync_inis_to_nap.py zusätzlich in den virtuellen
    # Root kopiert; sie sind deshalb auch ohne Inhalte im ignorierten NAP/ bekannt.
    for path in sdk_ini_files():
        files.add(path.relative_to(SDK).as_posix().casefold())
    return files


def scan(files: set[str]) -> tuple[dict[str, list[tuple[str, int]]], int, int]:
    unresolved: dict[str, list[tuple[str, int]]] = defaultdict(list)
    reference_count = 0
    external_count = 0
    for ini in sdk_ini_files():
        source = ini.relative_to(SDK).as_posix()
        for line_number, raw_line in enumerate(ini.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            # Freelancer-INI-Kommentare beginnen mit Semikolon.
            line = raw_line.split(";", 1)[0]
            if "=" not in line:
                continue
            value = line.split("=", 1)[1]
            for match in REFERENCE_RE.finditer(value):
                raw_path = match.group(1).strip("\"'")
                reference_count += 1
                if WINDOWS_ABSOLUTE_RE.match(raw_path.replace("\\", "/")):
                    external_count += 1
                    continue
                root_path = canonical(raw_path)
                local_path = canonical(posixpath.join(posixpath.dirname(source), raw_path.replace("\\", "/")))
                if (root_path is not None and root_path in files) or (local_path is not None and local_path in files):
                    continue
                target = root_path if root_path is not None else raw_path.replace("\\", "/").casefold()
                unresolved[target].append((source, line_number))
    return unresolved, reference_count, external_count


def render(unresolved: dict[str, list[tuple[str, int]]], reference_count: int, external_count: int, source_description: str) -> str:
    locations = sum(len(sites) for sites in unresolved.values())
    rows = [
        "# Fehlende Dateien",
        "",
        f"Quelle: {source_description}.",
        "Dateiverweise aus `SDK/**/*.ini` (ohne `SDK/exe/`) wurden mit dem",
        "virtuellen Root abgeglichen. Geprüft werden Rootpfade und Pfade relativ",
        "zur verweisenden INI; Groß-/Kleinschreibung wird ignoriert. Absolute",
        "Entwicklerpfade werden separat gezählt und nicht als Paketdateien gewertet.",
        "",
        f"**{len(unresolved)} fehlende Ziele**, **{locations} Fundstellen** von",
        f"{reference_count} Dateiverweisen; {external_count} absolute Entwicklerpfade ausgelassen.",
        "",
        "| Ziel | Verwendet in (INI:Zeile) |",
        "|---|---|",
    ]
    for target, sites in sorted(unresolved.items()):
        uses = ", ".join(f"`{source}:{line}`" for source, line in sites)
        rows.append(f"| `{target}` | {uses} |")
    rows.extend(["", "## Grenzen", "", "- Verweise ohne Ordner werden als fehlend ausgewiesen; ein Treffer desselben", "  Dateinamens an anderer Stelle beweist keine gültige Auflösung.", "- Interne Verweise in Binärdateien wie `.mat`, `.3db` und `.thn` werden nicht geprüft.", ""])
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--nap", type=Path, default=NAP, help="NAP-Klassencontainer (Standard: %(default)s)")
    source.add_argument("--data-root", type=Path, help="lokaler entpackter DATA-Ordner; wird nur lesend ausgewertet")
    parser.add_argument("--output", type=Path, help="Datei für den Markdown-Bericht (Standard: stdout)")
    args = parser.parse_args()
    nap_root = args.nap if args.data_root is None else None
    data_root = args.data_root
    try:
        files = virtual_files(nap_root=nap_root, data_root=data_root)
        non_ini_count = sum(not path.endswith(".ini") for path in files)
        if not non_ini_count:
            raise ValueError("Keine Asset-Dateien gefunden; NAP nicht aufgebaut? Verhindere einen irreführenden Voll-Fehlbericht.")
        unresolved, reference_count, external_count = scan(files)
        source_description = (
            "lokaler DATA-Rohdatenbaum mit build_nap.py-Namensregeln und SDK-INI-Overlay"
            if data_root is not None else "NAP-Klassencontainer mit SDK-INI-Overlay"
        )
        report = render(unresolved, reference_count, external_count, source_description)
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report, end="")
        print(
            f"Inventar: {len(files)} virtuelle Dateien, {reference_count} Dateiverweise, "
            f"{external_count} externe Pfade, {len(unresolved)} fehlende Ziele / "
            f"{sum(map(len, unresolved.values()))} Fundstellen.",
            file=sys.stderr,
        )
        return 0
    except (OSError, ValueError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
