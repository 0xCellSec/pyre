#!/bin/bash

set -e

# stores the aboslute path where this bash script is at
PYRE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE="requirements.txt"

echo "[+] Creating virtual enviornment..."
python3 -m venv "$PYRE_DIR/.venv"

echo "[+] Installing python dependencies..."
"$PYRE_DIR/.venv/bin/python" -m pip install --upgrade pip
"$PYRE_DIR/.venv/bin/python" -m pip install -r "$PYRE_DIR/requirements.txt"

echo "[+] Creating Pyre Launched"
mkdir -p "$HOME/.local/bin"

cat >"$HOME/.local/bin/pyre" <<EOF
#!/bin/bash
exec "$PYRE_DIR/.venv/bin/python" "$PYRE_DIR/pyre.py" "\$@"
EOF

chmod +x "$HOME/.local/bin/pyre"

echo "[+] PYRE has been installed!"
echo "[+] To get started run: pyre --help"
