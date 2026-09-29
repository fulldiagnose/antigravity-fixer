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


def handle_google_prompt_challenge(page, timeout=90):
    """Detect if Google prompts for 2-step verification (2-digit number challenge) on phone,
    print the number in the terminal, and wait for the user to tap it."""
    import re
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich import box
        console = Console()
    except ImportError:
        console = None

    time.sleep(4)

    url = page.url.lower()
    try:
        body_text = page.inner_text("body")
    except Exception:
        body_text = ""

    is_challenge = any(k in url for k in ["challenge", "signinoptions", "rejected"]) or any(
        k in body_text.lower() for k in [
            "check your phone", "buka ponsel", "tap yes", "ketuk ya",
            "verify it's you", "verifikasi bahwa ini memang anda",
            "google sent a notification", "google mengirimkan notifikasi",
            "periksa ponsel"
        ]
    )

    if not is_challenge:
        return True

    # Try to find the 1-2 digit number
    challenge_number = None

    # 1. Regex on page text
    patterns = [
        r'(?:then\s+tap|lalu\s+ketuk)\s+["\']?(\d{1,2})["\']?',
        r'(?:tap|ketuk)\s+["\']?(\d{1,2})["\']?\s+(?:on your phone|di ponsel)',
        r'(?:number|angka)\s*[:\s]*["\']?(\d{1,2})["\']?',
        r'\b(?:tap|ketuk)\s+["\']?(\d{1,2})["\']?\b',
    ]
    for pat in patterns:
        m = re.search(pat, body_text, re.IGNORECASE)
        if m:
            challenge_number = m.group(1)
            break

    # 2. Check DOM elements that specifically hold the challenge number
    if not challenge_number:
        selectors = [
            '[data-sign-in-number]',
            '[data-number]',
            'div[jsname="N6Elbf"]',
            'div.s54Xce',
            'span.s54Xce',
        ]
        for sel in selectors:
            try:
                for el in page.query_selector_all(sel):
                    t = el.inner_text().strip()
                    if t.isdigit() and 1 <= len(t) <= 2:
                        challenge_number = t
                        break
            except Exception:
                pass
            if challenge_number:
                break

    # 3. Check standalone 1-2 digit elements
    if not challenge_number:
        try:
            for el in page.query_selector_all('div, span, b, strong, h1, h2'):
                t = el.inner_text().strip()
                if t.isdigit() and 1 <= len(t) <= 2 and t == el.text_content().strip():
                    challenge_number = t
                    break
        except Exception:
            pass

    # Display to terminal
    if challenge_number:
        msg = (
            f"[bold white]📲 VERIFIKASI GOOGLE PROMPT (2FA DI HP)[/bold white]\n\n"
            f"  Google mengirimkan notifikasi ke ponsel Anda:\n"
            f"  1. Buka HP Anda & ketuk notifikasi dari Google\n"
            f"  2. Ketuk [bold]'Ya' / 'Yes'[/bold]\n"
            f"  3. [bold yellow]PILIH / KETUK ANGKA INI DI HP ANDA:[/bold yellow]\n\n"
            f"        👉  [bold green blink on black]  {challenge_number}  [/bold green blink on black]  👈\n\n"
            f"  [dim]Menunggu kamu memilih angka {challenge_number} di HP Anda...[/dim]"
        )
    else:
        msg = (
            f"[bold white]📲 VERIFIKASI GOOGLE PROMPT (2FA DI HP)[/bold white]\n\n"
            f"  Google mengirimkan notifikasi verifikasi ke ponsel Anda.\n"
            f"  Silakan buka HP Anda dan ketuk [bold]'Ya' / 'Yes'[/bold] untuk mengizinkan login.\n\n"
            f"  [dim]Menunggu konfirmasi dari HP Anda...[/dim]"
        )

    if console:
        console.print()
        console.print(Panel(msg, title="[bold yellow]Google 2FA Challenge[/bold yellow]", border_style="yellow", box=box.DOUBLE, padding=(1, 2)))
    else:
        print("\n" + "="*50)
        print(f"GOOGLE 2FA PROMPT: PILIH ANGKA >>> {challenge_number or 'YES'} <<< DI HP ANDA")
        print("="*50 + "\n")

    # Wait for user to confirm on phone
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(2)
        cur_url = page.url.lower()
        if "challenge" not in cur_url and "signin" not in cur_url:
            if console:
                console.print("  [bold green]✓ Verifikasi di HP berhasil![/bold green]\n")
            else:
                print("  ✓ Verifikasi di HP berhasil!")
            return True
        try:
            if "myaccount.google.com" in cur_url or "connections" in cur_url:
                if console:
                    console.print("  [bold green]✓ Verifikasi di HP berhasil![/bold green]\n")
                else:
                    print("  ✓ Verifikasi di HP berhasil!")
                return True
        except Exception:
            pass

    return False


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
        time.sleep(5)

        # Check for 2FA prompt challenge and show the 2-digit number to user
        handle_google_prompt_challenge(page, timeout=90)

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
