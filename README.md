# takedownsecondsons

Pentesting project integrated with the local pentesting toolkit.

## Project Structure

```
takedownsecondsons/
├── scripts/        # Custom scripts and automation
├── modules/        # Reusable Python/Ruby modules
├── data/           # Input data (target lists, etc.)
├── results/        # Scan results and outputs (gitignored)
├── reports/        # Generated reports (gitignored)
├── configs/        # Configuration files
├── wordlists/      # Custom wordlists (gitignored - use $WORDLISTS)
├── exploits/       # Custom exploits (gitignored)
├── payloads/       # Custom payloads (gitignored)
└── logs/           # Log files (gitignored)
```

## Setup

1. Activate the pentesting toolkit environment:
   ```bash
   source /Users/bash/Documents/Projects/pentesting/tools/activate.sh
   ```

2. Copy the example config:
   ```bash
   cp configs/config.example.yaml configs/config.yaml
   ```

3. Edit the config with your settings.

## Environment Variables

After activating the toolkit:
- `$WORDLISTS` - Path to wordlists
- `$SECLISTS` - Path to SecLists
- `$PENTEST_OUTPUT` - Default output directory

## Usage

```bash
# Run scripts from the scripts/ directory
./scripts/your_script.sh

# Results are saved to results/ (gitignored)
# Reports go to reports/ (gitignored)
```

## Security Notes

- **Never commit sensitive data** - The .gitignore is configured to exclude credentials, results, and target data
- **Review before pushing** - Always check `git status` before committing
- **Use example configs** - Keep `config.example.yaml` updated, never commit `config.yaml`

## License

Private - Authorized use only
