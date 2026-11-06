#!/usr/bin/env python3
"""
Slayin PS Vita - Cross-platform VPK Builder (Python version)
Generates Slayin.vpk from Slayin.apk + assets.enc + base/
"""

import os
import sys
import hashlib
import zipfile
import io

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ImportError:
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        def decrypt_aes(key, iv, ciphertext):
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded = decryptor.update(ciphertext) + decryptor.finalize()
            pad_len = padded[-1]
            return padded[:-pad_len]
    except ImportError:
        print("[ERROR] Required cryptographic library not found.")
        print("Please install pycryptodome: pip install pycryptodome")
        sys.exit(1)
else:
    def decrypt_aes(key, iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def find_apk():
    for name in ["Slayin.apk", "slayin.apk", "Slayin_v1.0.apk"]:
        p = os.path.join(SCRIPT_DIR, name)
        if os.path.isfile(p):
            return p
    for f in os.listdir(SCRIPT_DIR):
        if f.lower().endswith(".apk"):
            return os.path.join(SCRIPT_DIR, f)
    return None

def main():
    print("=" * 60)
    print("       SLAYIN PS VITA - CROSS-PLATFORM VPK BUILDER")
    print("=" * 60)

    apk_path = find_apk()
    if not apk_path:
        print("[ERROR] Slayin.apk not found in this directory!")
        print("Please place your original Slayin.apk here and run again.")
        sys.exit(1)

    enc_path = os.path.join(SCRIPT_DIR, "assets.enc")
    base_dir = os.path.join(SCRIPT_DIR, "base")
    out_vpk = os.path.join(SCRIPT_DIR, "Slayin.vpk")

    if not os.path.isfile(enc_path):
        print(f"[ERROR] assets.enc not found: {enc_path}")
        sys.exit(1)

    if not os.path.isdir(base_dir):
        print(f"[ERROR] base directory not found: {base_dir}")
        sys.exit(1)

    print(f"[1/4] Deriving AES-256 key from: {os.path.basename(apk_path)}")
    with open(apk_path, "rb") as f:
        apk_bytes = f.read()
    key = hashlib.sha256(apk_bytes).digest()
    print(f"      SHA-256 Key: {key.hex()}")

    print("[2/4] Decrypting assets.enc...")
    with open(enc_path, "rb") as f:
        all_enc = f.read()

    iv = all_enc[:16]
    ciphertext = all_enc[16:]

    try:
        decrypted_zip_bytes = decrypt_aes(key, iv, ciphertext)
    except Exception as e:
        print(f"\n[ERROR] Decryption failed: {e}")
        print("Your Slayin.apk does not match the expected version.")
        sys.exit(1)

    print(f"      Assets successfully decrypted ({len(decrypted_zip_bytes) / 1024 / 1024:.2f} MB)")

    print(f"[3/4] Assembling {os.path.basename(out_vpk)} with POSIX forward slashes...")
    if os.path.exists(out_vpk):
        os.remove(out_vpk)

    with zipfile.ZipFile(out_vpk, "w", zipfile.ZIP_DEFLATED) as vpk:
        # Add base files
        for root, _, files in os.walk(base_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")
                vpk.write(full_path, rel_path)

        # Add decrypted asset files
        with zipfile.ZipFile(io.BytesIO(decrypted_zip_bytes), "r") as assets_zip:
            for item in assets_zip.infolist():
                if not item.is_dir():
                    content = assets_zip.read(item.filename)
                    # Normalize to forward slashes
                    clean_name = item.filename.replace("\\", "/")
                    vpk.writestr(clean_name, content)

    final_size = os.path.getsize(out_vpk)
    print(f"[4/4] Slayin.vpk successfully created ({final_size / 1024 / 1024:.2f} MB)!")
    print("=" * 60)
    print("DONE! Copy Slayin.vpk to your PS Vita and install with VitaShell.")
    print("=" * 60)

if __name__ == "__main__":
    main()
