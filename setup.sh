#!/usr/bin/env bash

file="requirements.txt"

echo "Downloading python dependencies...."
for item in $(cat "$file"); do
  echo "[+] Installing $item"
  pip install $item >/dev/null
done
