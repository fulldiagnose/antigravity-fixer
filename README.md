<div align="center">

<img src="https://raw.githubusercontent.com/fulldiagnose/antigravity-fixer/main/assets/logo.svg" width="120" alt="Antigravity Fixer">

# Antigravity Fixer

**Diagnose and fix Google Antigravity eligibility errors in seconds.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)](https://github.com/fulldiagnose/antigravity-fixer)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](https://github.com/fulldiagnose/antigravity-fixer/pulls)

<br>

```
Eligibility check failed: Your current account is not eligible for Antigravity.
```

**Sound familiar?** This tool fixes it.

---

[Kenapa Error](#-kenapa-error-ini-muncul) · [Instalasi](#-instalasi) · [Cara Pakai](#-cara-pakai) · [AI Agent Guide](#-ai-agent-integration) · [Troubleshooting](#-troubleshooting)

</div>

<br>

## Apa Ini?

Tool CLI open-source untuk mendiagnosa dan memperbaiki error **"Your current account is not eligible for Antigravity"** atau **"not eligible for Gemini Code Assist for individuals"** yang muncul saat login Google Antigravity (IDE maupun CLI).

Didesain supaya bisa dipakai langsung oleh manusia **maupun AI coding agent** — tinggal clone, jalankan, selesai.

<br>

## 🔍 Kenapa Error Ini Muncul?

Berdasarkan investigasi langsung ke Google account backend, ada **3 penyebab utama:**

| &nbsp; | Penyebab | Dampak | Solusi |
|:---:|----------|--------|--------|
| **1** | Verifikasi umur belum selesai | Google backend return `VALIDATION_REQUIRED` (403) | Verifikasi via selfie di myaccount.google.com |
| **2** | Credential cache expired/corrupt | OAuth token lama masih dipakai, tapi sudah ditolak server | Hapus `.gemini/` + Windows Credential Manager |
| **3** | Koneksi app OAuth macet | Antigravity app permission stuck di akun Google | Revoke app connection, login ulang |

> Tool ini handle **penyebab #2 dan #3 secara otomatis.** Untuk #1, perlu verifikasi manual (upload selfie/KTP) karena Google mengharuskan interaksi langsung.

<br>

## 📦 Instalasi

```bash
git clone https://github.com/fulldiagnose/antigravity-fixer.git
cd antigravity-fixer
pip install -r requirements.txt
```

**Dependencies:** hanya [`camoufox`](https://github.com/nichochar/camoufox) — stealth browser automation berbasis Firefox.

<br>

## 🚀 Cara Pakai

### Diagnosa akun

```bash
python fix.py diagnose --email you@gmail.com
```

Cek status akun: age verification, country, subscription, connected apps.  
Password diminta secara interaktif (tidak tersimpan).

<details>
<summary>Contoh output</summary>

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

### Bersihin credential yang expired

```bash
python fix.py clean
```

Hapus token lama dari Windows Credential Manager + folder `.gemini`.  
Tidak butuh password, tidak butuh internet.

### Full fix (otomatis)

```bash
python fix.py fix --email you@gmail.com
```

Jalankan semua step sekaligus: kill proses → hapus credential → revoke app → buka browser untuk login ulang.

### Buka halaman verifikasi umur

```bash
python fix.py open-age-url --email you@gmail.com
```

Buka `myaccount.google.com/age-verification` di browser default.  
Kalau browser tidak bisa dibuka otomatis, URL ditampilkan di terminal.

<br>

## 🤖 AI Agent Integration

Tool ini didesain untuk dipanggil oleh AI coding agent (Hermes, Aider, Cursor, Codex, dll).

**Recommended workflow:**

```
Step 1 → python fix.py diagnose --email <email>
         Baca output, identifikasi masalah

Step 2 → Kalau age verification belum:
         Instruksikan user buka https://myaccount.google.com/age-verification
         Verifikasi pakai selfie/KTP (± 1 menit, auto-approved)

Step 3 → python fix.py clean
         Hapus credential stale

Step 4 → Kalau masih error:
         python fix.py fix --email <email>
         Full reset: clean + revoke + re-auth

Step 5 → Test: agy -p "say ok"
         Kalau output normal, akun sudah fix
```

**Exit codes:**
| Code | Artinya |
|------|---------|
| `0` | Berhasil / akun OK |
| `1` | Ada masalah ditemukan (lihat output) |

<br>

## 🛠 Troubleshooting

<details>
<summary><b>Error masih muncul setelah fix</b></summary>

Penyebab paling umum: **verifikasi umur belum selesai.**

```bash
python fix.py open-age-url --email you@gmail.com
```

Buka link, pilih "Take a selfie", ikuti instruksi. Approval biasanya instan.  
Setelah itu, jalankan `python fix.py clean` lalu test ulang.
</details>

<details>
<summary><b>Login timeout di browser</b></summary>

- Pastikan koneksi internet stabil
- Matikan VPN kalau aktif
- Google kadang minta QR code verification → klik **"Try another way"** → pilih SMS
</details>

<details>
<summary><b>Credential tidak terhapus</b></summary>

Jalankan terminal sebagai **Administrator**, lalu:
```bash
python fix.py clean
```
</details>

<details>
<summary><b>Workspace / G Suite account</b></summary>

Antigravity hanya support **akun personal `@gmail.com`**.  
Akun Google Workspace (email kantor/sekolah) **tidak eligible** — ini limitasi dari Google, bukan bug.
</details>

<br>

## 📁 Struktur Project

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

## ⚠️ Catatan Keamanan

- **Password** hanya diminta saat runtime via `getpass` — tidak pernah disimpan ke file/log
- **Browser session** bersifat ephemeral (headless, tidak menyimpan state)
- Tool ini **tidak mengirim data ke server manapun** — semua operasi lokal atau ke Google account resmi
- Source code terbuka — audit sendiri kalau ragu

<br>

## 🌍 Supported Countries

Antigravity tersedia di **190+ negara** termasuk Indonesia, Malaysia, Singapore, dll.  
Daftar lengkap: [`constants.py`](antigravity_fixer/constants.py) atau [dokumentasi resmi Google](https://developers.google.com/gemini-code-assist/resources/available-locations).

<br>

## 📄 License

[MIT](LICENSE) — bebas dipakai, dimodifikasi, didistribusikan.

<br>

<div align="center">

---

**Dibuat karena Google gak kasih error message yang jelas** 🙃

[Report Bug](https://github.com/fulldiagnose/antigravity-fixer/issues) · [Request Feature](https://github.com/fulldiagnose/antigravity-fixer/issues)

</div>
