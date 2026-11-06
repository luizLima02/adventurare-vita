# Slayin - PlayStation Vita Port

🌐 **Idioma / Language:** [🇧🇷 Português](#-português-pt-br) | [🇺🇸 English](#-english-en)

---

<a id="-português-pt-br"></a>
## 🇧🇷 Português (PT-BR)

Port não-oficial do clássico **Slayin** (desenvolvido originalmente pela PixelCount Studios / FDG Entertainment) para o **PlayStation Vita**.

Recompilado em **Unity 2018.2 (PSP2 IL2CPP)** com controles físicos completos, travamento suave a **60 FPS** e renderização nativa na GPU SGX543 do PS Vita.

---

### ⚖️ Aviso Legal & Direitos Autorais

Este repositório **NÃO contém nenhum sprite, arquivo de áudio ou fase proprietária do jogo original**. 
Todos os recursos comerciais protegidos por direitos autorais estão criptografados matematicamente com **AES-256** (`assets.enc`).

A chave de descriptografia é derivada diretamente do arquivo `Slayin.apk` legítimo fornecido pelo próprio usuário via hash criptográfico SHA-256. Sem possuir o jogo original, é matematicamente impossível descriptografar e jogar o port.

---

### 🎮 Recursos Deste Port
- **Controles Nativos do PS Vita:**
  - **D-Pad / Analógico Esquerdo:** Movimentação (Esquerda / Direita).
  - **Botão Cruz (X) / R:** Pular.
  - **Botão Start:** Pausar o jogo.
  - **Touchscreen:** Suporte opcional a toques na tela nos menus e lojas.
- **Física Ajustada:** Correção de colisão de moedas e alinhamento de sprites.
- **Zero Anúncios:** Todas as rotinas de propagandas e Google Play Services removidas.

---

### 📦 Instruções de Instalação (Para Jogadores)

#### Pré-requisitos:
- Um PlayStation Vita com desbloqueio (HENkaku / Ensō) e **VitaShell** instalado.
- O arquivo **`Slayin.apk`** original (v2.0.13 para Android).

#### Passo a Passo no Windows (1 Clique):
1. Baixe o pacote compactado deste repositório (ou clone com Git).
2. Coloque o seu arquivo **`Slayin.apk`** dentro da pasta raiz deste projeto.
3. Dê dois cliques no arquivo **`Gerar_VPK.bat`**.
4. O script gerará automaticamente o arquivo **`Slayin.vpk`** em 2 segundos.
5. Conecte o PS Vita ao PC pelo VitaShell (USB ou FTP) e envie o `Slayin.vpk`.
6. No VitaShell, navegue até o arquivo e aperte **X** para instalar.
7. Divirta-se!

*(Usuários Linux / macOS / Steam Deck podem rodar `python patcher.py` no terminal).*

---
---

<a id="-english-en"></a>
## 🇺🇸 English (EN)

Unofficial port of the classic **Slayin** (originally developed by PixelCount Studios / FDG Entertainment) for the **PlayStation Vita**.

Recompiled in **Unity 2018.2 (PSP2 IL2CPP)** featuring full physical button controls, a smooth **60 FPS** lock, and native rendering on the PS Vita's SGX543 GPU.

---

### ⚖️ Legal Notice & Copyright

This repository **DOES NOT contain any proprietary sprites, audio files, or levels from the original game**. 
All copyrighted commercial assets are mathematically encrypted using **AES-256** (`assets.enc`).

The decryption key is derived directly from the legitimate `Slayin.apk` file provided by the user via a SHA-256 cryptographic hash. Without owning the original game, it is mathematically impossible to decrypt and play this port.

---

### 🎮 Port Features
- **Native PS Vita Controls:**
  - **D-Pad / Left Analog Stick:** Movement (Left / Right).
  - **Cross Button (X) / R Trigger:** Jump.
  - **Start Button:** Pause the game.
  - **Touchscreen:** Optional touch support in menus and shops.
- **Tuned Physics:** Fixed coin collision and sprite alignment issues.
- **Zero Ads:** All advertisement routines and Google Play Services have been completely removed.

---

### 📦 Installation Instructions (For Players)

#### Prerequisites:
- A jailbroken PlayStation Vita (HENkaku / Ensō) with **VitaShell** installed.
- The original **`Slayin.apk`** file (v2.0.13 for Android).

#### Step-by-Step on Windows (1-Click):
1. Download the archive from this repository (or clone it via Git).
2. Place your **`Slayin.apk`** file inside the root folder of this project.
3. Double-click the **`Gerar_VPK.bat`** file.
4. The script will automatically generate the **`Slayin.vpk`** file in 2 seconds.
5. Connect your PS Vita to your PC via VitaShell (USB or FTP) and transfer `Slayin.vpk`.
6. In VitaShell, navigate to the file and press **X** to install it.
7. Enjoy!

*(Linux / macOS / Steam Deck users can run `python patcher.py` in the terminal).*