"""Check Google account eligibility status for Antigravity."""

import time
from camoufox.sync_api import Camoufox


def _login(page, email, password):
    """Login to Google account. Returns True if successful."""
    page.goto(
        "https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn",
        timeout=20000
    )
    time.sleep(4)

    email_input = page.query_selector('input[name="identifier"]')
    if not email_input:
        return False

    email_input.fill(email)
    time.sleep(0.5)
    page.click("#identifierNext")
    time.sleep(5)

    pwd_input = page.query_selector('input[name="Passwd"]')
    if not pwd_input:
        return False

    pwd_input.fill(password)
    time.sleep(0.5)
    page.click("#passwordNext")
    time.sleep(8)

    # Check if login succeeded (URL should not be on sign-in page)
    return "signin" not in page.url.lower() or "challenge" in page.url.lower()


def check_age_verification(page):
    """Check if age verification is completed."""
    page.goto("https://myaccount.google.com/age-verification", timeout=15000)
    time.sleep(4)
    text = page.inner_text("body")
    return {
        "verified": "verify your age" not in text.lower() and "pilih cara" not in text.lower(),
        "needs_action": "choose how to verify" in text.lower() or "pilih cara memverifikasi" in text.lower(),
        "raw": text[:500],
    }


def check_country(page):
    """Check Google account country association."""
    page.goto("https://policies.google.com/terms?hl=en", timeout=15000)
    time.sleep(3)
    text = page.inner_text("body")
    for line in text.split("\n"):
        if "country version" in line.lower():
            country = line.strip().replace("Country version:", "").strip()
            return {"country": country}
    return {"country": "unknown"}


def check_subscription(page):
    """Check Google One / AI Pro subscription status."""
    page.goto("https://one.google.com/", timeout=15000)
    time.sleep(5)
    text = page.inner_text("body")[:1500]

    has_pro = "pro" in text.lower() and ("google ai" in text.lower() or "one" in text.lower())
    has_plus = "plus" in text.lower() and "google ai" in text.lower()

    plan = "free"
    if has_pro:
        plan = "Google AI Pro"
    elif has_plus:
        plan = "Google AI Plus"

    return {"plan": plan}


def check_connected_apps(page):
    """Check if Google Antigravity is in connected apps."""
    page.goto("https://myaccount.google.com/connections", timeout=15000)
    time.sleep(4)
    text = page.inner_text("body")
    return {"antigravity_connected": "antigravity" in text.lower()}


def diagnose(email, password):
    """Full diagnosis of account eligibility. Returns dict with all checks."""
    results = {
        "email": email,
        "age_verification": None,
        "country": None,
        "subscription": None,
        "connected_apps": None,
        "error": None,
    }

    print(f"Diagnosing {email}...")

    try:
        with Camoufox(headless=True) as browser:
            page = browser.new_page()

            print("[1/5] Logging in...")
            login_ok = _login(page, email, password)
            if not login_ok:
                results["error"] = "Login failed. Check email/password."
                return results

            print("[2/5] Checking age verification...")
            results["age_verification"] = check_age_verification(page)
            status = "OK" if results["age_verification"]["verified"] else "NOT VERIFIED"
            print(f"       Age verification: {status}")

            print("[3/5] Checking country...")
            results["country"] = check_country(page)
            print(f"       Country: {results['country']['country']}")

            print("[4/5] Checking subscription...")
            results["subscription"] = check_subscription(page)
            print(f"       Plan: {results['subscription']['plan']}")

            print("[5/5] Checking connected apps...")
            results["connected_apps"] = check_connected_apps(page)
            ag_status = "connected" if results["connected_apps"]["antigravity_connected"] else "not connected"
            print(f"       Antigravity app: {ag_status}")

    except Exception as e:
        results["error"] = str(e)
        print(f"Error: {e}")

    return results
