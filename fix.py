#!/usr/bin/env python3
"""Antigravity Fixer — resolves 'not eligible' errors for Google Antigravity.

Usage:
    python fix.py diagnose --email YOUR@gmail.com
    python fix.py clean
    python fix.py fix --email YOUR@gmail.com
    python fix.py open-age-url --email YOUR@gmail.com

No passwords or tokens are stored. All browser sessions are ephemeral.
"""

import argparse
import getpass
import sys

from antigravity_fixer.cleaner import clean_all
from antigravity_fixer.checker import diagnose
from antigravity_fixer.browser import revoke_antigravity_app, open_auth_in_browser


def cmd_diagnose(args):
    """Run full account diagnosis."""
    password = args.password or getpass.getpass(f"Password for {args.email}: ")
    results = diagnose(args.email, password)

    print("\n" + "=" * 50)
    print("DIAGNOSIS RESULTS")
    print("=" * 50)

    if results["error"]:
        print(f"\nERROR: {results['error']}")
        return 1

    age = results["age_verification"]
    if age:
        if age["verified"]:
            print("\n  [OK]  Age verification: completed")
        else:
            print("\n  [!!]  Age verification: NOT COMPLETED")
            print("        → Go to https://myaccount.google.com/age-verification")
            print("        → Choose 'Take a selfie' and follow instructions")
            print("        → This is required before Antigravity will work")

    country = results["country"]
    if country:
        print(f"\n  [OK]  Country: {country['country']}")

    sub = results["subscription"]
    if sub:
        print(f"\n  [OK]  Subscription: {sub['plan']}")

    apps = results["connected_apps"]
    if apps:
        status = "yes" if apps["antigravity_connected"] else "no"
        print(f"\n  [--]  Antigravity app connected: {status}")

    print("\n" + "=" * 50)

    # Recommend next steps
    if age and not age["verified"]:
        print("\nNext steps:")
        print("  1. Complete age verification (link above)")
        print("  2. Run: python fix.py clean")
        print("  3. Run: agy (to test login)")
        return 1
    else:
        print("\nAccount looks good. Run: python fix.py clean")
        print("Then test with: agy")
        return 0


def cmd_clean(args):
    """Clear all stale credentials and cache."""
    changed = clean_all()
    print("\nDone. Run 'agy' to test login.")
    return 0


def cmd_fix(args):
    """Full fix: clean + revoke + guide re-auth."""
    password = args.password or getpass.getpass(f"Password for {args.email}: ")

    # Step 1: Clean
    print("=" * 50)
    print("STEP 1: Cleaning credentials")
    print("=" * 50)
    clean_all()

    # Step 2: Revoke old connection
    print("\n" + "=" * 50)
    print("STEP 2: Revoking old Antigravity app connection")
    print("=" * 50)
    try:
        revoke_antigravity_app(args.email, password)
    except Exception as e:
        print(f"  Warning: could not revoke app connection: {e}")
        print("  This is OK if the connection was already removed.")

    # Step 3: Open browser for fresh login
    print("\n" + "=" * 50)
    print("STEP 3: Re-authenticate")
    print("=" * 50)
    print("A browser will open for fresh Antigravity login.")
    print("Complete the login, then run 'agy' to verify.\n")
    open_auth_in_browser()

    return 0


def cmd_open_age_url(args):
    """Open age verification page in the default browser."""
    import subprocess
    import sys

    url = "https://myaccount.google.com/age-verification"
    print(f"Opening age verification page...")
    print(f"URL: {url}")
    print(f"Login with: {args.email}\n")

    try:
        if sys.platform == "win32":
            subprocess.Popen(["cmd", "/c", "start", url], shell=False)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", url])
        else:
            subprocess.Popen(["xdg-open", url])
    except Exception:
        print(f"Open this URL in your browser:\n{url}")

    print("\nAfter verification, run: python fix.py clean")
    print("Then test with: agy")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Fix 'not eligible' errors for Google Antigravity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fix.py diagnose --email me@gmail.com
  python fix.py clean
  python fix.py fix --email me@gmail.com
  python fix.py open-age-url --email me@gmail.com

Root causes of the 403 error:
  1. Age verification not completed → use open-age-url
  2. Stale credentials → use clean
  3. All of the above → use fix
        """,
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # diagnose
    p_diag = sub.add_parser("diagnose", help="Check account eligibility status")
    p_diag.add_argument("--email", required=True, help="Google account email")
    p_diag.add_argument("--password", help="Password (will prompt if not provided)")

    # clean
    sub.add_parser("clean", help="Clear stale credentials and cache")

    # fix
    p_fix = sub.add_parser("fix", help="Full fix: clean + revoke + re-auth")
    p_fix.add_argument("--email", required=True, help="Google account email")
    p_fix.add_argument("--password", help="Password (will prompt if not provided)")

    # open-age-url
    p_age = sub.add_parser("open-age-url", help="Open age verification page in browser")
    p_age.add_argument("--email", required=True, help="Google account email")

    args = parser.parse_args()

    commands = {
        "diagnose": cmd_diagnose,
        "clean": cmd_clean,
        "fix": cmd_fix,
        "open-age-url": cmd_open_age_url,
    }

    sys.exit(commands[args.command](args))


if __name__ == "__main__":
    main()
