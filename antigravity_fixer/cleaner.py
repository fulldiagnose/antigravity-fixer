"""Clean stale Antigravity credentials and cache."""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

_backup_session = None


class CleanupAborted(Exception):
    """Raised when cleanup is declined or cannot be confirmed."""


def clean_credentials():
    """Remove Antigravity entries from OS credential store."""
    removed = []

    if sys.platform == "win32":
        # Windows: use cmdkey (Credential Manager)
        try:
            result = subprocess.run(
                ["cmdkey", "/list"],
                capture_output=True, text=True, timeout=10
            )
            lines = result.stdout.split("\n")
            for i, line in enumerate(lines):
                target_line = line.strip()
                if target_line.startswith("Target:") and any(
                    kw in target_line.lower()
                    for kw in ["gemini", "antigravity", "agy"]
                ):
                    target = target_line.replace("Target:", "").strip()
                    if any(kw in target.lower() for kw in ["gemini", "antigravity", "agy"]):
                        subprocess.run(["cmdkey", "/delete", target],
                                       capture_output=True, timeout=10)
                        removed.append(target)
        except Exception as e:
            print(f"  Warning: credential cleanup error: {e}")

    elif sys.platform == "darwin":
        # macOS: use security CLI (Keychain)
        for service in ["gemini", "antigravity", "agy", "Antigravity IDE"]:
            try:
                subprocess.run(
                    ["security", "delete-generic-password", "-s", service],
                    capture_output=True, timeout=10
                )
                removed.append(service)
            except Exception:
                pass

    else:
        # Linux: check for secret-tool (GNOME Keyring / libsecret)
        for service in ["gemini", "antigravity", "agy", "Antigravity IDE"]:
            try:
                subprocess.run(
                    ["secret-tool", "clear", "service", service],
                    capture_output=True, timeout=10
                )
                removed.append(service)
            except FileNotFoundError:
                break
            except Exception:
                pass

    return removed


def cache_targets():
    """Return the existing directories that clean_cache() would remove."""
    home = Path.home()
    candidates = []

    # 1. Antigravity CLI state (~/.gemini/antigravity* and ~/.antigravity)
    gemini_home = home / ".gemini"
    if gemini_home.exists():
        for child in gemini_home.iterdir():
            if "antigravity" in child.name.lower():
                candidates.append(child)
    candidates.append(home / ".antigravity")

    # 2. Antigravity Desktop App & IDE state
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        localappdata = os.environ.get("LOCALAPPDATA")
        if appdata:
            candidates.extend([
                Path(appdata) / "Antigravity",
                Path(appdata) / "Antigravity IDE",
            ])
        if localappdata:
            candidates.extend([
                Path(localappdata) / "antigravity",
                Path(localappdata) / "antigravity-updater",
            ])
    elif sys.platform == "darwin":
        candidates.extend([
            home / "Library" / "Application Support" / "Antigravity",
            home / "Library" / "Application Support" / "Antigravity IDE",
            home / "Library" / "Caches" / "Antigravity",
            home / "Library" / "Caches" / "Antigravity IDE",
        ])
    else:
        candidates.extend([
            home / ".config" / "Antigravity",
            home / ".config" / "Antigravity IDE",
            home / ".config" / "antigravity",
            home / ".cache" / "antigravity",
        ])

    return [p for p in candidates if p.exists() or p.is_symlink()]


def _backup_root():
    return Path.home() / ".antigravity-fixer-backup"


def _backup_dir():
    """Return this run's backup directory, creating it (private) on first use."""
    global _backup_session
    if _backup_session is None:
        _backup_session = _backup_root() / time.strftime("%Y%m%d-%H%M%S")
    _backup_session.mkdir(parents=True, exist_ok=True)
    for d in (_backup_root(), _backup_session):
        try:
            os.chmod(d, 0o700)
        except OSError:
            pass
    return _backup_session


def _backup_name(path):
    """Flat, filesystem-safe name that keeps track of where a folder came from."""
    try:
        parts = path.relative_to(Path.home()).parts
    except ValueError:
        parts = path.parts[1:] or path.parts
    return "__".join(
        p.replace(":", "").replace("\\", "").replace("/", "") for p in parts
    )


def _remove_target(path, backup):
    """Move `path` into the backup directory, or delete it when backup is off.

    Returns the backup destination (str) or None. Raises OSError on failure.
    """
    if backup:
        name = _backup_name(path)
        dest = _backup_dir() / name
        n = 1
        while dest.exists():  # same folder removed again within one run
            n += 1
            dest = dest.with_name(f"{name}.{n}")
        shutil.move(str(path), str(dest))
        return str(dest)

    if path.is_symlink():
        path.unlink()
    else:
        shutil.rmtree(path)
    return None


def confirm_cleanup(backup=True):
    """List what cleanup will remove and ask the user to confirm.

    Returns normally when there is nothing to remove or the user agrees.
    Raises CleanupAborted otherwise, including in non-interactive sessions.
    """
    targets = cache_targets()
    if not targets:
        return

    print("The following Antigravity data will be removed:")
    for t in targets:
        print(f"  - {t}")
    print("  - matching entries in the OS credential store")
    print("These folders can hold IDE settings, extensions and chat history,")
    print("not just cache.")
    if backup:
        print(f"Folders are moved to {_backup_root()}{os.sep}<timestamp> so you can restore them.")
    else:
        print("WARNING: --no-backup is set. This cannot be undone.")

    if not sys.stdin.isatty():
        raise CleanupAborted("Non-interactive session: re-run with --yes to confirm.")
    try:
        answer = input("Continue? [y/N] ").strip().lower()
    except EOFError:
        answer = ""
    if answer not in ("y", "yes"):
        raise CleanupAborted("Cancelled. Nothing was removed.")


def clean_cache(backup=True):
    """Remove Antigravity CLI and Desktop App / IDE state directories.

    With backup=True (default) folders are moved to ~/.antigravity-fixer-backup
    instead of being deleted. Only folders that were actually removed are
    reported; failures are printed as warnings.
    """
    removed_dirs = []
    for path in cache_targets():
        try:
            dest = _remove_target(path, backup)
        except OSError as e:
            print(f"      Warning: could not remove {path}: {e}")
            continue
        if dest:
            print(f"      Backup: {path} -> {dest}")
        removed_dirs.append(str(path))
    return removed_dirs


def kill_processes():
    """Kill running Antigravity CLI and IDE processes."""
    killed = []

    if sys.platform == "win32":
        for name in ["agy.exe", "Antigravity.exe", "Antigravity IDE.exe"]:
            try:
                result = subprocess.run(
                    ["tasklist", "/FI", f"IMAGENAME eq {name}"],
                    capture_output=True, text=True, timeout=5
                )
                if name.replace(".exe", "").lower() in result.stdout.lower():
                    subprocess.run(
                        ["taskkill", "/F", "/IM", name],
                        capture_output=True, timeout=10
                    )
                    killed.append(name)
            except Exception:
                pass

        try:
            subprocess.run(
                ["powershell", "-Command",
                 "Stop-Process -Name agy,Antigravity,'Antigravity IDE' -Force -ErrorAction SilentlyContinue"],
                capture_output=True, timeout=10
            )
        except Exception:
            pass

    else:
        for name in ["agy", "Antigravity", "Antigravity IDE"]:
            try:
                result = subprocess.run(
                    ["pkill", "-f", name],
                    capture_output=True, timeout=5
                )
                if result.returncode == 0:
                    killed.append(name)
            except Exception:
                pass

    return killed


def clean_all(assume_yes=False, backup=True):
    """Full cleanup: kill processes, remove credentials, clear cache.

    Asks for confirmation first unless assume_yes is set. Raises
    CleanupAborted (before touching anything) if the user declines.
    """
    if not assume_yes:
        confirm_cleanup(backup)

    print("[1/3] Killing running processes...")
    killed = kill_processes()
    if killed:
        print(f"      Killed: {', '.join(killed)}")
    else:
        print("      No processes to kill")

    print("[2/3] Removing credentials...")
    removed = clean_credentials()
    if removed:
        for r in removed:
            print(f"      Removed: {r}")
    else:
        print("      No credentials to remove")

    print("[3/3] Clearing cache...")
    dirs = clean_cache(backup=backup)
    if dirs:
        for d in dirs:
            print(f"      Removed: {d}")
    else:
        print("      No cache to clear")

    return len(removed) > 0 or len(dirs) > 0
