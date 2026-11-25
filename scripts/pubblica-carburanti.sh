#!/usr/bin/env bash
# GalleggiApp · pubblica i prezzi ufficiali dei carburanti dal PC di casa.
# Scarica gli open data MIMIT (raggiungibili da una connessione italiana, non dai server di GitHub),
# li divide in zone e li pubblica nel ramo "dati-carburanti" del repo, che viene sostituito ogni volta.
set -euo pipefail
DIR="$HOME/.local/share/galleggiapp-carburanti"
TOKEN_FILE="$HOME/.config/galleggiapp/github-token"
REPO="galimbertip/GalleggiApp"
mkdir -p "$DIR"; cd "$DIR"
exec > >(tee "$DIR/ultimo.log") 2>&1
echo "== $(date '+%d/%m/%Y %H:%M') avvio"
# usa sempre l'ultima versione dello script dal repo (se non c'è rete per GitHub, quella già scaricata)
curl -fsSL -m 30 "https://raw.githubusercontent.com/$REPO/main/scripts/carburanti.py" -o carburanti.py.new && mv carburanti.py.new carburanti.py || echo "uso lo script già presente"
rm -rf out
python3 carburanti.py out
cd out
git init -q -b dati-carburanti
git add -A
git -c user.name="GalleggiApp (PC di casa)" -c user.email="galimbertip@users.noreply.github.com" commit -q -m "Prezzi carburanti $(date -u +%Y-%m-%dT%H:%MZ)"
git push -q -f "https://galimbertip:$(cat "$TOKEN_FILE")@github.com/$REPO.git" HEAD:dati-carburanti
echo "== $(date '+%H:%M') pubblicato: $(grep -o '"distributori": [0-9]*' meta.json)"
