"""Browser automation for Antigravity OAuth re-authentication."""

import time
import re
from camoufox.sync_api import Camoufox


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


def open_auth_in_browser():
    """Open Antigravity OAuth page in the default system browser.

    Returns the auth URL for manual pasting if browser doesn't open.
    This is the fallback for environments without camoufox.
    """
    import subprocess
    import sys

    # Generate a fresh auth URL (user needs to complete in their real browser)
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?client_id=1071006060591-tmhssin2h21lcre235vtolojh4g403ep.apps.googleusercontent.com"
        "&redirect_uri=https%3A%2F%2Fantigravity.google%2Foauth-callback"
        "&response_type=code"
        "&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform"
        "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email"
        "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile"
        "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcclog"
        "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fexperimentsandconfigs"
        "+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Faicode"
        "+openid"
        "&access_type=offline"
        "&prompt=consent"
        "&code_challenge_method=S256"
    )

    # Try to open in default browser
    try:
        if sys.platform == "win32":
            subprocess.Popen(["cmd", "/c", "start", auth_url], shell=False)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", auth_url])
        else:
            subprocess.Popen(["xdg-open", auth_url])
        print("Opened browser. Complete login and paste the authorization code.")
    except Exception:
        print(f"Could not open browser automatically.\nOpen this URL manually:\n{auth_url}")

    return auth_url
