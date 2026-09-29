"""Clean stale Antigravity credentials and cache."""

import os
import sys
import subprocess
import shutil
from pathlib import Path


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
                    if any(kw in target.lower() for kw in ["gemini:antigravity", "antigravity", "agy"]):
                        subprocess.run(["cmdkey", "/delete", target],
                                       capture_output=True, timeout=10)
                        removed.append(target)
        except Exception as e:
            print(f"  Warning: credential cleanup error: {e}")

    elif sys.platform == "darwin":
        # macOS: use security CLI (Keychain)
        for service in ["gemini", "antigravity", "agy"]:
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
        for service in ["gemini", "antigravity", "agy"]:
            try:
                subprocess.run(
                    ["secret-tool", "clear", "service", service],
                    capture_output=True, timeout=10
                )
                removed.append(service)
            except FileNotFoundError:
                # secret-tool not installed — skip silently
                break
            except Exception:
                pass

    return removed


def clean_cache():
    """Remove .gemini cache directory."""
    gemini_home = Path.home() / ".gemini"
    if not gemini_home.exists():
        return False

    removed_dirs = []
    for child in gemini_home.iterdir():
        name = child.name.lower()
        if any(k in name for k in ["antigravity", "antigravity-cli", "antigravity-ide"]):
            shutil.rmtree(child, ignore_errors=True)
            removed_dirs.append(str(child))

    # If whole .gemini is now empty or only has non-antigravity stuff, keep it
    return removed_dirs


def kill_processes():
    """Kill running Antigravity/agy processes."""
    killed = []

    if sys.platform == "win32":
        # Windows: tasklist + taskkill + PowerShell fallback
        for name in ["agy.exe", "Antigravity.exe"]:
            try:
                result = subprocess.run(
                    ["tasklist", "/FI", f"IMAGENAME eq {name}"],
                    capture_output=True, text=True, timeout=5
                )
                if name.replace(".exe", "") in result.stdout.lower():
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
                 "Stop-Process -Name agy -Force -ErrorAction SilentlyContinue;"
                 "Stop-Process -Name Antigravity -Force -ErrorAction SilentlyContinue"],
                capture_output=True, timeout=10
            )
        except Exception:
            pass

    else:
        # Linux / macOS: pkill
        for name in ["agy", "Antigravity"]:
            try:
                result = subprocess.run(
                    ["pkill", "-f", name],
                    capture_output=True, timeout=5
                )
                if result.returncode == 0:
                    killed.append(name)
            except FileNotFoundError:
                pass
            except Exception:
                pass

    return killed


def clean_all():
    """Full cleanup: kill processes, remove credentials, clear cache."""
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
    dirs = clean_cache()
    if dirs:
        for d in dirs:
            print(f"      Removed: {d}")
    else:
        print("      No cache to clear")

    return len(removed) > 0 or len(dirs) > 0
