# 🔧 Antigravity Fixer

**Tool untuk memperbaiki error "Your current account is not eligible for Antigravity"**

Kalau lo pakai Google Antigravity (IDE atau CLI) dan dapet error:
```
Eligibility check failed: Your current account is not eligible for Antigravity.
Your current account is not eligible for gemini code assist for individuals at this time.
```

Tool ini bantu fix masalah tersebut. Cocok dipakai langsung atau oleh AI coding agent.

## Penyebab Umum

| # | Penyebab | Solusi |
|---|----------|--------|
| 1 | **Verifikasi umur belum selesai** | Verifikasi pakai selfie/ID di myaccount.google.com/age-verification |
| 2 | **Credential cache stale** | Hapus credential + cache `.gemini` |
| 3 | **Koneksi app Antigravity macet** | Revoke + login ulang |

Tool ini otomatis handle #2 dan #3. Untuk #1, lo perlu verifikasi manual (upload selfie/ID).

## Instalasi

```bash
git clone https://github.com/fulldiagnose/antigravity-fixer.git
cd antigravity-fixer
pip install -r requirements.txt
```

## Cara Pakai

### Cek Status Akun
```bash
python fix.py diagnose --email EMAIL@gmail.com
```
Cek apakah akun lo udah age verified, country supported, dll.

### Bersihin Credential Stale
```bash
python fix.py clean
```
Hapus token lama dari Windows Credential Manager + folder `.gemini`.

### Full Fix (Otomatis)
```bash
python fix.py fix --email EMAIL@gmail.com
```
Bersihin credential → revoke koneksi app lama → buka browser buat login ulang.

### Buka Halaman Verifikasi Umur
```bash
python fix.py open-age-url --email EMAIL@gmail.com
```
Buka halaman age verification di browser default.

## Syarat

- Windows 10/11
- Python 3.10+
- `camoufox` (auto-install via `pip install -r requirements.txt`)
- Akun Google personal `@gmail.com` (bukan Workspace)
- Negara akun harus di [daftar supported countries](https://developers.google.com/gemini-code-assist/resources/available-locations)

## Cara Kerja untuk AI Agent

Tool ini dirancang bisa dipanggil oleh AI coding agent. Workflow yang disarankan:

```
1. python fix.py diagnose --email <email>  → cek status akun
2. Kalau age verification belum → kasih tau user buat verifikasi manual
3. Kalau credential stale → python fix.py clean
4. Kalau masih stuck → python fix.py fix --email <email> buat full reset
5. Setelah fix, user tinggal jalankan agy buat test login
```

## Tips

- **Jangan scan QR code** kalau diminta verifikasi → klik "Try another way" → pakai SMS
- Credential stale itu penyebab paling umum setelah age verification
- Kalau pakai VPN, matikan dulu sebelum login Antigravity

## Troubleshooting

| Error | Solusi |
|-------|--------|
| "not eligible" muncul lagi setelah fix | Verifikasi umur belum selesai, cek `open-age-url` |
| Login timeout di browser | Pastikan koneksi internet stabil, coba lagi |
| Credential gak kehapus | Jalankan script sebagai administrator |

## Lisensi

MIT
