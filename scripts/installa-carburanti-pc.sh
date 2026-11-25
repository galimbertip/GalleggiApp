#!/usr/bin/env bash
# GalleggiApp · installa sul PC Linux (es. Linux Mint) l'aggiornamento automatico dei prezzi carburanti.
# Uso:  curl -fsSL https://raw.githubusercontent.com/galimbertip/GalleggiApp/main/scripts/installa-carburanti-pc.sh | bash
# Cosa fa: ogni giorno alle 8:40 e alle 13:40 (e all'accensione, se a quell'ora il PC era spento)
# scarica i prezzi ufficiali MIMIT e li pubblica per GalleggiApp. Serve un token GitHub (vedi sotto).
set -euo pipefail
REPO="galimbertip/GalleggiApp"
DIR="$HOME/.local/share/galleggiapp-carburanti"; CONF="$HOME/.config/galleggiapp"; UNIT="$HOME/.config/systemd/user"
echo "🛢️  GalleggiApp · prezzi carburanti dal PC di casa"
for c in python3 git curl systemctl; do
  command -v "$c" >/dev/null || { echo "❌ Manca '$c'. Installalo con:  sudo apt install $c   e rilancia."; exit 1; }
done
mkdir -p "$DIR" "$CONF" "$UNIT"
curl -fsSL "https://raw.githubusercontent.com/$REPO/main/scripts/pubblica-carburanti.sh" -o "$DIR/pubblica-carburanti.sh"
chmod +x "$DIR/pubblica-carburanti.sh"
if [ ! -s "$CONF/github-token" ]; then
  echo
  echo "Serve un token GitHub che possa scrivere SOLO nel repo GalleggiApp:"
  echo "  github.com → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token"
  echo "  · Repository access: Only select repositories → GalleggiApp"
  echo "  · Permissions → Contents: Read and write   · Scadenza: 1 anno"
  printf "Incolla qui il token (non si vede mentre scrivi) e premi Invio: "
  read -rs TOKEN </dev/tty; echo
  [ -n "$TOKEN" ] || { echo "❌ Token vuoto."; exit 1; }
  umask 077; printf '%s' "$TOKEN" > "$CONF/github-token"
fi
chmod 600 "$CONF/github-token"
cat > "$UNIT/galleggiapp-carburanti.service" <<UNITEOF
[Unit]
Description=GalleggiApp: pubblica i prezzi ufficiali dei carburanti
Wants=network-online.target
After=network-online.target
[Service]
Type=oneshot
ExecStartPre=/bin/sleep 30
ExecStart=$DIR/pubblica-carburanti.sh
UNITEOF
cat > "$UNIT/galleggiapp-carburanti.timer" <<'UNITEOF'
[Unit]
Description=GalleggiApp: prezzi carburanti ogni giorno
[Timer]
OnCalendar=*-*-* 08:40:00
OnCalendar=*-*-* 13:40:00
Persistent=true
RandomizedDelaySec=300
[Install]
WantedBy=timers.target
UNITEOF
systemctl --user daemon-reload
systemctl --user enable --now galleggiapp-carburanti.timer
echo "▶️  Prima pubblicazione adesso (1–3 minuti)…"
if "$DIR/pubblica-carburanti.sh"; then echo "✅ Fatto! In GalleggiApp → Benzina → Benzinai vicino a te."; else echo "⚠️ Qualcosa non è andato: guarda $DIR/ultimo.log"; fi
echo "Prossimi aggiornamenti:"; systemctl --user list-timers galleggiapp-carburanti.timer --no-pager | head -3
