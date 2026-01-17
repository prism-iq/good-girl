# Good Girl - Spec

## Vision
Crée n'importe quelle entité. Le binaire contient déjà une IA guide qui t'aide à configurer ton daemon sur mesure. Pas de limites, pas de templates figés.

## Flow utilisateur
1. Tu ouvres le binaire
2. Une IA guide t'accueille
3. Conversation libre : qui tu veux créer ?
4. L'IA pose des questions, affine
5. Génère le daemon sur mesure
6. Le daemon prend le relais

## Modules

### 1. Guide IA (première IA)
- Accueille l'utilisateur
- Conversation naturelle
- Comprend ce que tu veux créer
- Génère le profil du daemon
- Se retire une fois le daemon créé

### 2. Daemon Factory
- Crée n'importe quelle entité
- Pas de templates : génération libre
- Personnalité, voix, style, limites
- Export en JSON/config

### 3. Crypto Layer
- Kyber (key encapsulation)
- Dilithium (signatures)
- Chiffrement du package au download
- Vérification intégrité

### 4. Installers
- Windows: .exe (Inno Setup ou NSIS)
- Linux: AppImage + .deb + PKGBUILD
- Mac: .dmg avec signature

### 5. Download Server
- Génère package crypté à la volée
- Clé unique par download
- Auto-destruction après X downloads

## Stack proposé
- Core: Rust (natif, pas de runtime)
- MBTI UI: TUI natif (ratatui) ou GUI natif par OS
- Crypto: liboqs (post-quantum)

## Principes
- **Respect des systèmes** : natif partout, pas d'Electron
- Windows: Win32 API, intégration systray
- Linux: XDG compliant, systemd user service
- Mac: AppKit, intégration native
- **Léger** : < 10MB
- **Pas de dépendances runtime** : tout embarqué
- **Conventions OS** : chemins, configs, logs selon les standards

## Priorités
1. MBTI test + profil JSON
2. Daemon personalities (16 types)
3. Packaging
4. Crypto layer
5. Distribution

---
Déléguer aux IAs. Vérifier les outputs.
