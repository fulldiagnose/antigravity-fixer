"""Browser automation for Antigravity OAuth re-authentication."""

import time
import re
from camoufox.sync_api import Camoufox


def open_in_incognito(url):
    """Open URL in an incognito / private browser window across OS platforms."""
    import subprocess
    import sys
    import os
    import shutil

    if sys.platform == "win32":
        # Windows: direct binary paths bypass cmd.exe shell & parsing bugs
        browser_targets = [
            # (path, flag)
            (os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"), "--incognito"),
            (os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"), "--incognito"),
            (os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"), "--incognito"),
            (os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"), "--inprivate"),
            (os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"), "--inprivate"),
            (os.path.expandvars(r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe"), "--incognito"),
            (os.path.expandvars(r"%ProgramFiles%\Mozilla Firefox\firefox.exe"), "-private-window"),
        ]

        for exe_path, flag in browser_targets:
            if os.path.isfile(exe_path):
                try:
                    subprocess.Popen([exe_path, flag, url])
                    return True
                except Exception:
                    continue

        # Fallback via python webbrowser if direct path not found
        import webbrowser
        try:
            webbrowser.open(url)
            return True
        except Exception:
            return False

    elif sys.platform == "darwin":
        # macOS: try open with app args
        candidates = [
            ["open", "-na", "Google Chrome", "--args", "--incognito", url],
            ["open", "-na", "Microsoft Edge", "--args", "--inprivate", url],
            ["open", "-na", "Brave Browser", "--args", "--incognito", url],
            ["open", "-na", "Firefox", "--args", "-private-window", url],
        ]
        for cmd in candidates:
            try:
                res = subprocess.run(cmd, capture_output=True, timeout=3)
                if res.returncode == 0:
                    opened = True
                    break
            except Exception:
                continue

        if not opened:
            try:
                subprocess.Popen(["open", url])
                opened = True
            except Exception:
                pass

    else:
        # Linux
        candidates = [
            ["google-chrome", "--incognito", url],
            ["chromium", "--incognito", url],
            ["chromium-browser", "--incognito", url],
            ["brave-browser", "--incognito", url],
            ["firefox", "-private-window", url],
        ]
        for cmd in candidates:
            try:
                subprocess.Popen(cmd)
                opened = True
                break
            except FileNotFoundError:
                continue
            except Exception:
                continue

        if not opened:
            try:
                subprocess.Popen(["xdg-open", url])
                opened = True
            except Exception:
                pass

    return opened


def revoke_antigravity_app(email, password):
    """Remove Google Antigravity from connected apps."""
    print("[1/3] Logging in to revoke Antigravity app...")

    with Camoufox(headless=True) as browser:
        page = browser.new_page()

        # Login
        page.goto(
            "https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn",
            timeout=20000
        )
        time.sleep(4)
        page.fill('input[name="identifier"]', email)
        time.sleep(0.5)
        page.click("#identifierNext")
        time.sleep(5)
        page.fill('input[name="Passwd"]', password)
        time.sleep(0.5)
        page.click("#passwordNext")
        time.sleep(10)

        # Go to connected apps
        print("[2/3] Finding Antigravity in connected apps...")
        page.goto("https://myaccount.google.com/connections", timeout=15000)
        time.sleep(5)

        # Find and click Antigravity
        ag_link = page.query_selector("text=Google Antigravity")
        if not ag_link:
            print("       Antigravity not found in connected apps (already removed?)")
            return True

        ag_link.click()
        time.sleep(3)

        # Click "Delete all"
        print("[3/3] Removing Antigravity app connection...")
        delete_btn = page.query_selector("text=Delete all")
        if not delete_btn:
            print("       Could not find delete button")
            return False

        delete_btn.click()
        time.sleep(3)

        # Confirm
        for sel in [
            'button:has-text("Confirm")',
            'button:has-text("OK")',
            'button:has-text("Delete")',
        ]:
            btn = page.query_selector(sel)
            if btn:
                btn.click()
                time.sleep(3)
                print("       Antigravity app removed successfully")
                return True

        print("       Could not confirm deletion")
        return False
