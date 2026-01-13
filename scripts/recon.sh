#!/bin/bash
# Quick reconnaissance script
# Usage: ./recon.sh <target_domain>

set -e

TARGET="$1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$PROJECT_DIR/results/recon_${TIMESTAMP}"

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target_domain>"
    exit 1
fi

# Check if toolkit is activated
if [ -z "$WORDLISTS" ]; then
    echo "Error: Pentesting toolkit not activated."
    echo "Run: source /Users/bash/Documents/Projects/pentesting/tools/activate.sh"
    exit 1
fi

echo "═══════════════════════════════════════════════════════════════"
echo "  Reconnaissance: $TARGET"
echo "  Output: $OUTPUT_DIR"
echo "═══════════════════════════════════════════════════════════════"

mkdir -p "$OUTPUT_DIR"

echo ""
echo "[*] Running whatweb..."
whatweb -v "$TARGET" 2>&1 | tee "$OUTPUT_DIR/whatweb.txt"

echo ""
echo "[*] Checking for WAF..."
wafw00f "$TARGET" 2>&1 | tee "$OUTPUT_DIR/wafw00f.txt"

echo ""
echo "[*] Running subfinder..."
subfinder -d "$TARGET" -silent 2>&1 | tee "$OUTPUT_DIR/subdomains.txt"

echo ""
echo "[*] Probing with httpx..."
cat "$OUTPUT_DIR/subdomains.txt" | httpx -silent 2>&1 | tee "$OUTPUT_DIR/live_hosts.txt"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Recon complete. Results in: $OUTPUT_DIR"
echo "═══════════════════════════════════════════════════════════════"
