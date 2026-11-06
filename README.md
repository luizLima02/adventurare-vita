# Slayin - PlayStation Vita Port

Port não-oficial do clássico **Slayin** (desenvolvido originalmente pela PixelCount Studios / FDG Entertainment) para o **PlayStation Vita**.

Recompilado em **Unity 2018.2 (PSP2 IL2CPP)** com controles físicos completos, travamento suave a **60 FPS** e renderização nativa na GPU SGX543 do PS Vita.

---

## ⚖️ Aviso Legal & Direitos Autorais

Este repositório **NÃO contém nenhum sprite, arquivo de áudio ou fase proprietária do jogo original**. 
Todos os recursos comerciais protegidos por direitos autorais estão criptografados matematicamente com **AES-256** (`assets.enc`).

A chave de descriptografia é derivada diretamente do arquivo `Slayin.apk` legítimo fornecido pelo próprio usuário via hash criptográfico SHA-256. Sem possuir o jogo original, é matematicamente impossível descriptografar e jogar o port.

---

## 🎮 Recursos Deste Port
- **Controles Nacionais do PS Vita:**
  - **D-Pad / Analógico Esquerdo:** Movimentação (Esquerda / Direita).
  - **Botão Cruz (X) / R:** Pular.
  - **Botão Start:** Pausar o jogo.
  - **Touchscreen:** Suporte opcional a toques na tela nos menus e lojas.
- **Física Ajustada:** Correção de colisão de moedas e alinhamento de sprites.
- **Zero Anúncios:** Todas as rotinas de propagandas e Google Play Services removidas.

---

## 📦 Instruções de Instalação (Para Jogadores)

### Pré-requisitos:
- Um PlayStation Vita com desbloqueio (HENkaku / Ensō) e **VitaShell** instalado.
- O arquivo **`Slayin.apk`** original (v2.0.13 para Android).

### Passo a Passo no Windows (1 Clique):
1. Baixe o pacote compactado deste repositório (ou clone com Git).
2. Coloque o seu arquivo **`Slayin.apk`** dentro da pasta raiz deste projeto.
3. Dê dois cliques no arquivo **`Gerar_VPK.bat`**.
4. O script gerará automaticamente o arquivo **`Slayin.vpk`** em 2 segundos.
5. Conecte o PS Vita ao PC pelo VitaShell (USB ou FTP) e envie o `Slayin.vpk`.
6. No VitaShell, navegue até o arquivo e aperte **X** para instalar.
7. Divirta-se!

*(Usuários Linux / macOS / Steam Deck podem rodar `python patcher.py` no terminal).*
