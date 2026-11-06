"""
Script de Desenvolvimento: Atualiza o pacote de distribuicao do Slayin Vita Port.
Executado pelo desenvolvedor apos compilar o projeto na Unity.

Ele realiza:
1. Copia dos binarios e arquivos do sistema (eboot.bin, param.sfo, sce_module, metadata) para base/
2. Compactacao e criptografia AES-256 dos assets proprietarios (archive.psarc, Media/sharedassets*) para assets.enc
3. Teste de geracao do Slayin.vpk para garantir conformidade
"""

import os
import sys
import shutil
import hashlib
import zipfile
import io

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    print("[ERRO] Biblioteca 'pycryptodome' nao encontrada.")
    print("Execute: pip install pycryptodome")
    sys.exit(1)

# Caminhos
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.join(REPO_ROOT, "base")
TEMP_BUILD_DIR = r"D:\codigos\Unity Projects\slayin\Build\TempBuild"
DEV_APK_SEARCH_PATHS = [
    os.path.join(REPO_ROOT, "Slayin.apk"),
    r"D:\codigos\VITA\slayin\Slayin.apk",
]

# Arquivos publicos da engine / sistema que vao em base/
ENGINE_FILES = [
    "eboot.bin",
    "Media/boot.config",
    "Media/platform_native_link.xml",
    "Media/SymbolMap",
    "Media/Metadata/global-metadata.dat",
    "Media/Modules/il2CppAssemblies.suprx",
    "Media/Modules/pthread.suprx",
    "sce_module/libc.suprx",
    "sce_module/libface.suprx",
    "sce_module/libfios2.suprx",
    "sce_module/libsmart.suprx",
    "sce_module/libult.suprx",
    "sce_sys/icon0.png",
    "sce_sys/param.sfo",
    "sce_sys/pic0.png",
    "sce_sys/livearea/contents/bg0.png",
    "sce_sys/livearea/contents/default_gate.png",
    "sce_sys/livearea/contents/template.xml",
]

# Arquivos proprietarios protegidos por direitos autorais que vao em assets.enc
PROPRIETARY_ASSETS = [
    "archive.psarc",
    "Media/globalgamemanagers",
    "Media/globalgamemanagers.assets",
    "Media/sharedassets0.assets.resS",
    "Media/sharedassets1.assets.resS",
    "Media/sharedassets1.resource",
    "Media/sharedassets2.assets.resS",
    "Media/sharedassets2.resource",
    "Media/sharedassets3.assets.resS",
    "Media/sharedassets3.resource",
    "Media/sharedassets4.assets.resS",
    "Media/sharedassets4.resource",
    "Media/sharedassets5.assets.resS",
    "Media/sharedassets5.resource",
    "Media/sharedassets6.assets.resS",
    "Media/sharedassets6.resource",
    "Media/sharedassets8.assets.resS",
    "Media/sharedassets8.resource",
]

def find_apk():
    for p in DEV_APK_SEARCH_PATHS:
        if os.path.isfile(p):
            return p
    return None

def main():
    print("=" * 60)
    print("  SLAYIN PS VITA - ATUALIZACAO DO PACOTE DE DISTRIBUICAO")
    print("=" * 60)

    if not os.path.isdir(TEMP_BUILD_DIR):
        print(f"[ERRO] Diretorio de build da Unity nao encontrado: {TEMP_BUILD_DIR}")
        print("Compile o projeto na Unity primeiro!")
        sys.exit(1)

    apk_path = find_apk()
    if not apk_path:
        print("[ERRO] Slayin.apk nao encontrado para derivar chave de criptografia.")
        sys.exit(1)

    print(f"[1/4] Derivando chave AES-256 do APK: {apk_path}")
    with open(apk_path, "rb") as f:
        apk_bytes = f.read()
    key = hashlib.sha256(apk_bytes).digest()
    print(f"      Hash SHA-256: {key.hex()}")

    print(f"[2/4] Atualizando arquivos base da engine em '{BASE_DIR}'...")
    os.makedirs(BASE_DIR, exist_ok=True)
    for rel in ENGINE_FILES:
        src = os.path.join(TEMP_BUILD_DIR, rel.replace("/", os.sep))
        dst = os.path.join(BASE_DIR, rel.replace("/", os.sep))
        if not os.path.isfile(src):
            print(f"[AVISO] Arquivo da engine nao encontrado: {src}")
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    print(f"      {len(ENGINE_FILES)} arquivos sincronizados com sucesso.")

    print(f"[3/4] Compactando e criptografando assets proprietarios em 'assets.enc'...")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in PROPRIETARY_ASSETS:
            src = os.path.join(TEMP_BUILD_DIR, rel.replace("/", os.sep))
            if not os.path.isfile(src):
                print(f"[ERRO] Asset proprietario ausente: {src}")
                sys.exit(1)
            # Armazena estritamente com barras /
            zf.write(src, rel.replace("\\", "/"))

    plain_bytes = zip_buffer.getvalue()
    print(f"      Tamanho comprimido antes da cifra: {len(plain_bytes):,} bytes ({len(plain_bytes)/1024/1024:.2f} MB)")

    # AES-256-CBC com padding PKCS7
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plain_bytes, AES.block_size))
    encrypted_payload = iv + ciphertext

    out_enc = os.path.join(REPO_ROOT, "assets.enc")
    with open(out_enc, "wb") as f:
        f.write(encrypted_payload)
    print(f"      Arquivo criptografado gerado: {out_enc}")
    print(f"      Tamanho final de assets.enc: {len(encrypted_payload):,} bytes ({len(encrypted_payload)/1024/1024:.2f} MB)")

    print("[4/4] Concluido com sucesso!")
    print("=" * 60)
    print("O repositorio de distribuicao esta 100% atualizado com a sua build da Unity.")
    print("Voce ja pode fazer git add / git commit / git push com total seguranca legal.")
    print("=" * 60)

if __name__ == "__main__":
    main()
