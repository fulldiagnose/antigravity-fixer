<div align="center">

<img src="https://raw.githubusercontent.com/fulldiagnose/antigravity-fixer/main/assets/logo.png" width="140" alt="Antigravity Fixer">

# Antigravity Fixer

**Diagnose and fix Google Antigravity & 9router eligibility errors in seconds.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20·%20Linux%20·%20macOS-0078D4?style=flat-square)](https://github.com/fulldiagnose/antigravity-fixer)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](https://github.com/fulldiagnose/antigravity-fixer/pulls)

<br>

```
Eligibility check failed: Your current account is not eligible for Antigravity.
```
```
There was an unexpected issue setting up your account.
Your current account is not eligible for gemini code assist for individuals at this time.
```
```
403 Forbidden — VALIDATION_REQUIRED
```

**Sound familiar?** This tool fixes it.

Resolves: **9router 403 errors** · **Antigravity account not eligible** · **Gemini Code Assist login failures** · **Phone number verification stuck on smartphone** · **Stale OAuth credentials**

Also works for **9router** and other providers that use Google Antigravity / Gemini Code Assist as their backend.

---

### How It Works

<img src="https://raw.githubusercontent.com/fulldiagnose/antigravity-fixer/main/assets/how-it-works.png" alt="How It Works" width="800">

---

[Why This Happens](#why-this-happens) · [Install](#install) · [Usage](#usage) · [AI Agent Guide](#ai-agent-integration) · [Troubleshooting](#troubleshooting)

</div>

<br>

## What Is This?

An open-source CLI tool that diagnoses and fixes the **"Your current account is not eligible for Antigravity"** and **"not eligible for Gemini Code Assist for individuals"** errors that show up when logging into Google Antigravity (IDE or CLI), 9router, or any provider built on top of the same backend.

Designed to be used by humans **and AI coding agents** — clone, run, done.

<br>


## Install

```bash
git clone https://github.com/fulldiagnose/antigravity-fixer.git
cd antigravity-fixer
pip install -r requirements.txt
```

**Dependencies:** only [`camoufox`](https://github.com/nichochar/camoufox) — stealth browser automation based on Firefox.

<br>

## Usage

### Diagnose account

```bash
python fix.py diagnose --email you@gmail.com
```

Checks account status: age verification, country, subscription, connected apps.  
Password is prompted interactively and never stored.

<details>
<summary>Example output</summary>

```
Diagnosing you@gmail.com...
[1/5] Logging in...
[2/5] Checking age verification...
       Age verification: NOT VERIFIED
[3/5] Checking country...
       Country: Indonesia
[4/5] Checking subscription...
       Plan: Google AI Pro
[5/5] Checking connected apps...
       Antigravity app: connected

==================================================
DIAGNOSIS RESULTS
==================================================

  [!!]  Age verification: NOT COMPLETED
        → Go to https://myaccount.google.com/age-verification
        → Choose 'Take a selfie' and follow instructions

  [OK]  Country: Indonesia
  [OK]  Subscription: Google AI Pro
  [--]  Antigravity app connected: yes
```
</details>

### Clean stale credentials

```bash
python fix.py clean
```

Removes expired tokens from Windows Credential Manager + `.gemini` folder.  
No password required, no internet needed.

### Full fix (automated)

```bash
python fix.py fix --email you@gmail.com
```

Runs every step at once: kill processes → clear credentials → revoke app → open browser for fresh login.

### Open age verification page

```bash
python fix.py open-age-url --email you@gmail.com
```

Opens `myaccount.google.com/age-verification` in your default browser.  
If the browser can't be opened automatically, the URL is printed to terminal.

<br>

## AI Agent Integration

This tool is designed to be called by AI coding agents (Hermes, Aider, Cursor, Codex, etc).

**Recommended workflow:**

```
Step 1 → python fix.py diagnose --email <email>
         Read output, identify the problem

Step 2 → If age verification is incomplete:
         Instruct user to open https://myaccount.google.com/age-verification
         Verify via selfie/ID (± 1 minute, auto-approved)

Step 3 → python fix.py clean
         Clear stale credentials

Step 4 → If still failing:
         python fix.py fix --email <email>
         Full reset: clean + revoke + re-auth

Step 5 → Test: agy -p "say ok"
         If output is normal, account is fixed
```

**Exit codes:**
| Code | Meaning |
|------|---------|
| `0` | Success / account OK |
| `1` | Problem found (check output) |

<br>

## Troubleshooting

<details>
<summary><b>Error persists after fix</b></summary>

Most common cause: **age verification not completed.**

```bash
python fix.py open-age-url --email you@gmail.com
```

Open the link, choose "Take a selfie", follow the instructions. Approval is usually instant.  
After that, run `python fix.py clean` and test again.
</details>

<details>
<summary><b>Browser login timeout</b></summary>

- Make sure your internet connection is stable
- Disable VPN if active
- Google sometimes asks for QR code verification → click **"Try another way"** → choose SMS
</details>

<details>
<summary><b>Credentials not removed</b></summary>

Run terminal as **Administrator**, then:
```bash
python fix.py clean
```
</details>

<details>
<summary><b>Workspace / G Suite account</b></summary>

Antigravity only supports **personal `@gmail.com` accounts**.  
Google Workspace accounts (work/school email) are **not eligible** — this is a Google limitation, not a bug.
</details>

<details>
<summary><b>9router / third-party provider errors</b></summary>

9router and similar providers route requests through Google Antigravity / Gemini Code Assist.  
The same root causes apply — run `python fix.py diagnose` to identify the issue,  
then follow the same fix steps. The error message might differ slightly, but the solution is identical.
</details>

<br>

## Project Structure

```
antigravity-fixer/
├── fix.py                       # CLI entry point
├── requirements.txt             # Dependencies
├── LICENSE                      # MIT
└── antigravity_fixer/
    ├── __init__.py
    ├── checker.py               # Account diagnosis (age, country, subscription)
    ├── cleaner.py               # Credential & cache cleanup
    ├── browser.py               # OAuth revoke & re-auth
    └── constants.py             # Supported countries, URLs, paths
```

<br>

## Security

- **Passwords** are only prompted at runtime via `getpass` — never written to disk or logs
- **Browser sessions** are ephemeral (headless, no persistent state)
- This tool **does not send data to any external server** — all operations are local or directed at official Google account pages
- Source code is open — audit it yourself if in doubt

<br>

## Supported Countries

Antigravity is available in **190+ countries** including Indonesia, Malaysia, Singapore, and more.  
Full list: [`constants.py`](antigravity_fixer/constants.py) or [official Google docs](https://developers.google.com/gemini-code-assist/resources/available-locations).

<br>

## License

[MIT](LICENSE) — free to use, modify, and distribute.

<br>

<div align="center">

---

**Built because Google doesn't give you a clear error message** 🙃

[Report Bug](https://github.com/fulldiagnose/antigravity-fixer/issues) · [Request Feature](https://github.com/fulldiagnose/antigravity-fixer/issues)

</div>
