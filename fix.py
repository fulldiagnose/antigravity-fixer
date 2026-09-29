#!/usr/bin/env python3
"""Antigravity Fixer — resolves 'not eligible' errors for Google Antigravity & 9router.

Interactive mode:
    python fix.py

CLI mode:
    python fix.py --clean-only

No passwords or tokens are stored. All browser sessions are ephemeral.
"""

import argparse
import getpass
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich.align import Align
from rich import box

from antigravity_fixer.cleaner import clean_all
from antigravity_fixer.browser import revoke_antigravity_app, open_in_incognito

console = Console()

BANNER = r"""
     ___          __  _                       _ __         _______
    /   |  ____  / /_(_)___ __________ __   __(_) /___  __/ ____(_)  _____  _____
   / /| | / __ \/ __/ / __ `/ ___/ __ `/ | / / / __/ / / / /_  / / |/ / _ \/ ___/
  / ___ |/ / / / /_/ / /_/ / /  / /_/ /| |/ / / /_/ /_/ / __/ / />  </  __/ /
 /_/  |_/_/ /_/\__/_/\__, /_/   \__,_/ |___/_/\__/\__, /_/   /_/_/|_|\___/_/
                    /____/                        /____/
"""

# ─── BILINGUAL STRINGS ──────────────────────────────────────────────────────

STRINGS = {
    "id": {
        "subtitle": "Tool otomatis perbaiki error 403 / Not Eligible Google Antigravity & 9router",
        "email_title": "Email Akun Google",
        "email_hint": "Gunakan akun personal @gmail.com (bukan Google Workspace / kampus)",
        "email_label": "Email",
        "pass_title": "Password Akun",
        "pass_hint": "Password aman: hanya diproses di memori sesi ini, tidak pernah disimpan",
        "pass_label": "Password",
        "step1_title": "Langkah 1/3: Bersihkan Cache & Kredensial Stale",
        "cleaning": "Menutup proses dan membersihkan cache .gemini serta credential manager...",
        "clean_done": "[green]✓[/green] Cache lokal dan token lama berhasil dibersihkan.",
        "step2_title": "Langkah 2/3: Cabut Izin App Antigravity Lama (Revoke)",
        "revoking": "Mencabut koneksi OAuth Antigravity lama di akun Google...",
        "revoke_success": "[green]✓[/green] Izin app lama berhasil dicabut.",
        "revoke_skipped": "[yellow]⚠[/yellow] Izin app sudah bersih atau tidak ditemukan.",
        "step3_title": "Langkah 3/3: Verifikasi Umur Akun Google (Selfie)",
        "step3_desc": "Google memblokir Antigravity (403) jika akun belum terverifikasi usia.\nBrowser Incognito otomatis dibuka ke halaman verifikasi resmi Google.",
        "step3_instruction": "1. Login dengan akun Google kamu di jendela browser yang terbuka.\n2. Pilih opsi [bold]'Ambil selfie'[/bold] (biasanya langsung disetujui dalam 1 menit).\n3. Selesaikan selfie, lalu kembali ke terminal ini.",
        "press_enter_step3": "Tekan ENTER jika sudah menyelesaikan verifikasi selfie...",
        "final_title": "Langkah Terakhir: Login & Tempel Token Otorisasi",
        "final_desc": (
            "1. Jendela terminal baru otomatis dibuka untuk menjalankan: [bold cyan]agy -p \"halo\"[/bold cyan]\n"
            "2. Di browser resmi Google yang terbuka, login dengan akun yang sudah diverifikasi.\n"
            "3. Setelah login berhasil, halaman Google akan menampilkan [bold yellow]kode token otorisasi[/bold yellow] (berawalan [bold]4/0A...[/bold]).\n"
            "4. [bold green]Salin (Copy)[/bold green] kode token tersebut dari halaman web.\n"
            "5. [bold green]Tempel (Paste)[/bold green] ke jendela terminal [bold cyan]agy[/bold cyan] pada baris:\n"
            "   [dim]'Or, paste the authorization code here and press Enter:'[/dim]\n"
            "6. Tekan [bold]ENTER[/bold] — Akun langsung aktif tanpa error 403!"
        ),
        "launching_terminal": "Membuka jendela terminal baru untuk menjalankan agy...",
        "manual_cmd_hint": "Jika jendela terminal tidak otomatis terbuka, buka terminal baru lalu jalankan manual:\n  [bold cyan]agy -p \"halo\"[/bold cyan]",
        "clean_only_done": "[bold green]Selesai![/bold green] Cache lokal dan kredensial lama berhasil dibersihkan.",
    },
    "en": {
        "subtitle": "Automated fix for Google Antigravity & 9router 403 / Not Eligible errors",
        "email_title": "Google Account Email",
        "email_hint": "Must be a personal @gmail.com account (not Google Workspace)",
        "email_label": "Email",
        "pass_title": "Account Password",
        "pass_hint": "Secure: only used in-memory during this session, never saved",
        "pass_label": "Password",
        "step1_title": "Step 1/3: Purge Stale Cache & Credentials",
        "cleaning": "Stopping background processes and purging .gemini cache & credentials...",
        "clean_done": "[green]✓[/green] Local cache and stale tokens successfully cleared.",
        "step2_title": "Step 2/3: Revoke Stale Antigravity OAuth App Connection",
        "revoking": "Revoking old Antigravity OAuth connection from Google account...",
        "revoke_success": "[green]✓[/green] Old OAuth permissions revoked successfully.",
        "revoke_skipped": "[yellow]⚠[/yellow] Old OAuth permissions already clean or not found.",
        "step3_title": "Step 3/3: Google Account Age Verification (Selfie)",
        "step3_desc": "Google blocks Antigravity (403) if your account lacks age verification.\nAn Incognito browser is opening to the official Google verification page.",
        "step3_instruction": "1. Sign in with your Google account in the opened browser window.\n2. Choose [bold]'Take a selfie'[/bold] (approval is usually instant within 1 min).\n3. Finish selfie verification, then return to this terminal.",
        "press_enter_step3": "Press ENTER after completing selfie verification...",
        "final_title": "Final Step: Sign In & Paste Authorization Token",
        "final_desc": (
            "1. A new terminal window is automatically opened running: [bold cyan]agy -p \"hello\"[/bold cyan]\n"
            "2. Complete the Google sign-in on the official browser window that opens.\n"
            "3. Upon successful sign-in, Google will display an [bold yellow]authorization code / token[/bold yellow] (starts with [bold]4/0A...[/bold]).\n"
            "4. [bold green]Copy[/bold green] that token code from the webpage.\n"
            "5. [bold green]Paste[/bold green] it into the [bold cyan]agy[/bold cyan] terminal prompt at:\n"
            "   [dim]'Or, paste the authorization code here and press Enter:'[/dim]\n"
            "6. Press [bold]ENTER[/bold] — Account authorized with zero 403 errors!"
        ),
        "launching_terminal": "Opening a new terminal window to run agy...",
        "manual_cmd_hint": "If the terminal window does not open automatically, run this command in a new terminal:\n  [bold cyan]agy -p \"hello\"[/bold cyan]",
        "clean_only_done": "[bold green]Done![/bold green] Local cache and stale credentials purged.",
    }
}

# ─── HELPERS ────────────────────────────────────────────────────────────────

def show_banner(s):
    console.print(BANNER, style="bold cyan", highlight=False)
    console.print(Align.center(f"[dim]{s['subtitle']}[/dim]"))
    console.print()


def step_spinner(text, duration=1.5):
    with Live(Spinner("dots", text=text, style="cyan"), console=console, refresh_per_second=12):
        time.sleep(duration)


def pick_language():
    console.print(BANNER, style="bold cyan", highlight=False)
    console.print(Panel(
        "  [bold cyan]1[/bold cyan]  🇮🇩  Bahasa Indonesia\n"
        "  [bold cyan]2[/bold cyan]  🇺🇸  English",
        title="[bold white]Pilih Bahasa / Select Language[/bold white]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    lang = Prompt.ask("  [bold cyan]›[/bold cyan]", choices=["1", "2"], default="1")
    console.clear()
    return STRINGS["id"] if lang == "1" else STRINGS["en"]


def launch_agy_terminal():
    """Launch a new terminal window running agy -p in parallel."""
    import subprocess
    import shutil

    if sys.platform == "win32":
        try:
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", 'agy -p "halo"'], shell=False)
            return True
        except Exception:
            return False
    elif sys.platform == "darwin":
        try:
            subprocess.Popen(["osascript", "-e", 'tell app "Terminal" to do script "agy -p \\"hello\\""'])
            return True
        except Exception:
            return False
    else:
        for term in ["x-terminal-emulator", "gnome-terminal", "konsole", "xfce4-terminal", "alacritty", "kitty", "xterm"]:
            if shutil.which(term):
                try:
                    if term == "gnome-terminal":
                        subprocess.Popen([term, "--", "agy", "-p", "hello"])
                    else:
                        subprocess.Popen([term, "-e", "agy -p 'hello'"])
                    return True
                except Exception:
                    continue
        return False


# ─── MAIN PIPELINE ──────────────────────────────────────────────────────────

def run_pipeline(email, password, s):
    show_banner(s)

    # ── LANGKAH 1: Bersihkan cache & kredensial lokal
    console.print(Panel(f"[bold white]{s['step1_title']}[/bold white]", border_style="cyan", box=box.ROUNDED))
    step_spinner(s["cleaning"], 1.5)
    clean_all()
    console.print(f"  {s['clean_done']}\n")

    # ── LANGKAH 2: Otomatis Cabut Izin OAuth Lama (Revoke)
    console.print(Panel(f"[bold white]{s['step2_title']}[/bold white]", border_style="cyan", box=box.ROUNDED))
    step_spinner(s["revoking"], 2.0)
    try:
        ok = revoke_antigravity_app(email, password)
        if ok:
            console.print(f"  {s['revoke_success']}\n")
        else:
            console.print(f"  {s['revoke_skipped']}\n")
    except Exception as e:
        console.print(f"  {s['revoke_skipped']}: {e}\n")

    # Bersihkan sekali lagi setelah revoke
    clean_all()

    # ── LANGKAH 3 (DI AKHIR): Minta Verifikasi Umur (Selfie)
    console.print()
    age_url = "https://myaccount.google.com/age-verification"
    console.print(Panel(
        f"[bold white]{s['step3_title']}[/bold white]\n\n"
        f"{s['step3_desc']}\n\n"
        f"Link: [bold cyan underline]{age_url}[/bold cyan underline]\n\n"
        f"{s['step3_instruction']}",
        border_style="yellow",
        box=box.ROUNDED,
        padding=(1, 2)
    ))
    step_spinner("Opening Incognito browser...", 1.0)
    open_in_incognito(age_url)
    Prompt.ask(f"\n[bold yellow]👉 {s['press_enter_step3']}[/bold yellow]")

    # Bersihkan cache terakhir kali agar fresh setelah verifikasi selfie
    clean_all()

    # ── SELESAI & INSTRUKSI LOGIN
    console.print()
    console.print(Panel(
        f"[bold green]{s['final_title']}[/bold green]\n\n"
        f"{s['final_desc']}\n\n"
        f"[dim]{s['manual_cmd_hint']}[/dim]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2)
    ))

    step_spinner(s["launching_terminal"], 1.5)
    launch_agy_terminal()
    return 0


# ─── ENTRY POINT ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fix 403 / Not Eligible errors for Google Antigravity & 9router")
    parser.add_argument("--clean-only", action="store_true", help="Only clean local cache and processes")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall all dependencies and clean up")
    parser.add_argument("--lang", choices=["id", "en"], default="id", help="Language choice for CLI mode")

    args = parser.parse_args()

    if args.uninstall:
        import subprocess
        show_banner(STRINGS[args.lang])
        console.print("[yellow]Uninstalling dependencies...[/yellow]")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-r", "requirements.txt", "-y"])
        console.print(Panel(
            "[bold green]Uninstalled successfully![/bold green]\n\n"
            "Dependencies (camoufox, rich) have been removed.\n"
            "You can now safely delete the [bold cyan]antigravity-fixer[/bold cyan] folder.",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        sys.exit(0)

    if args.clean_only:
        s = STRINGS[args.lang]
        show_banner(s)
        clean_all()
        console.print(Panel(s["clean_only_done"], border_style="green"))
        sys.exit(0)

    s = pick_language()
    show_banner(s)

    console.print(Panel(
        f"[bold white]{s['email_title']}[/bold white]\n[dim]{s['email_hint']}[/dim]",
        border_style="cyan", box=box.ROUNDED, padding=(1, 2),
    ))
    email = Prompt.ask(f"  [bold cyan]{s['email_label']}[/bold cyan]").strip()

    console.print()
    console.print(Panel(
        f"[bold white]{s['pass_title']}[/bold white] [bold yellow]{email}[/bold yellow]\n"
        f"[dim]{s['pass_hint']}[/dim]",
        border_style="cyan", box=box.ROUNDED, padding=(1, 2),
    ))
    password = getpass.getpass(f"  {s['pass_label']}: ")

    console.clear()
    sys.exit(run_pipeline(email, password, s))


if __name__ == "__main__":
    main()
