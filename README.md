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

[Prerequisites](#prerequisites) · [Install](#install) · [Usage](#usage) · [AI Agent Guide](#ai-agent-integration) · [Uninstallation](#uninstallation) · [Troubleshooting](#troubleshooting)

</div>

<br>

## What Is This?

An open-source CLI tool that diagnoses and fixes the **"Your current account is not eligible for Antigravity"** and **"not eligible for Gemini Code Assist for individuals"** errors that show up when logging into Google Antigravity (IDE or CLI), 9router, or any provider built on top of the same backend.

Designed to be used by humans **and AI coding agents** — clone, run, done.

<br>

## Prerequisites

Before running this tool, ensure you have:
- **Google Antigravity** installed — either the CLI (`agy`) or Antigravity Desktop App / IDE.
- **Python 3.10+** installed on your system.

<br>

## Install

```bash
git clone https://github.com/fulldiagnose/antigravity-fixer.git
cd antigravity-fixer
pip install -r requirements.txt
```

**Dependencies:**
- [`camoufox`](https://github.com/nichochar/camoufox) — stealth headless browser automation
- [`rich`](https://github.com/Textualize/rich) — terminal UI, progress indicators & formatting

<br>

## Usage

Run the interactive fixer:

```bash
python fix.py
```

Follow the guided steps on screen:
1. **Choose Language**: Select 🇮🇩 Bahasa Indonesia or 🇺🇸 English.
2. **Enter Google Account**: Provide your `@gmail.com` email & password (used in-memory only, never saved).
3. **Automated Cleanup**: Kills stuck processes, removes credentials, and clears cache across:
   - Antigravity CLI (`~/.gemini/antigravity*`, `~/.antigravity`)
   - Antigravity Desktop App & IDE (`AppData` / `Application Support` / `.config`)
   - Windows Credential Manager / Keychain / Secret Service
4. **Revoke App Permission**: Automatically revokes stuck OAuth connections in your Google Account.
5. **Selfie Verification**: Automatically launches an Incognito browser to `myaccount.google.com/age-verification`. Complete the selfie check and press Enter.
6. **Automatic Antigravity CLI Login Test**:
   - Immediately after selfie verification, a new terminal opens and runs `agy`.
   - Select **option 1** in the Antigravity CLI login menu.
   - Let `agy` open the official Google sign-in page automatically—this fixer does not open a separate OAuth URL.
   - Sign in with the Google account that just completed selfie verification.
   - Google displays an authorization code (usually starts with `4/0A...`).
   - Copy the code and paste it into the waiting `agy` prompt:
     ```
     Or, paste the authorization code here and press Enter:
     ```
   - Press **ENTER** to complete sign-in.

### Quick Clean Only

If you only want to purge local cache, credentials, and background processes without revoking:

```bash
python fix.py --clean-only
```

Before anything is removed, the tool lists the folders it will touch and asks for confirmation. These folders can hold IDE settings, extensions and chat history, so by default they are **moved** to `~/.antigravity-fixer-backup/<timestamp>/` instead of being deleted. To restore one, move it back to its original location.

| Flag | Effect |
|------|--------|
| `-y`, `--yes` | Skip the confirmation prompt (required in non-interactive sessions) |
| `--no-backup` | Delete folders permanently instead of moving them to the backup folder |

<br>

## AI Agent Integration

This tool is designed to be called by AI coding agents (Hermes, Aider, Cursor, Codex, etc).

**Recommended workflow:**

```
Step 1 → Verify Google Account age verification:
         Instruct user to complete selfie check at https://myaccount.google.com/age-verification

Step 2 → python fix.py --clean-only --yes
         Purge stale credentials, CLI cache, and Desktop App/IDE state
         (folders are backed up to ~/.antigravity-fixer-backup; --yes is
         required when there is no interactive terminal)

Step 3 → agy
         Select option 1, let agy open Google sign-in, then copy the 4/0A... authorization code from the browser and paste it into agy
```

<br>

## Troubleshooting

<details>
<summary><b>Error persists after fix</b></summary>

Most common cause: **age verification not completed.**

1. Open `https://myaccount.google.com/age-verification` in your browser.
2. Choose "Take a selfie" and follow the on-screen instructions.
3. Once approved, run `python fix.py --clean-only` and launch `agy` again.
</details>

<details>
<summary><b>Browser login timeout</b></summary>

- Make sure your internet connection is stable.
- Disable VPN or proxy if active.
</details>

<details>
<summary><b>Credentials not removed</b></summary>

Run terminal as **Administrator** (Windows) or with proper permissions, then run:
```bash
python fix.py --clean-only
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

## Uninstallation

To completely uninstall Antigravity Fixer and all its dependencies, just run:

```bash
python fix.py --uninstall
```

Or manually:
```bash
pip uninstall -r requirements.txt -y
```
Then simply delete the `antigravity-fixer` folder. Done!

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
