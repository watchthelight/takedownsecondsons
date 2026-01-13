#!/usr/bin/env python3
"""
Utility functions for takedownsecondsons
"""

import os
import yaml
import subprocess
from pathlib import Path
from datetime import datetime


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def load_config(config_path=None):
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = get_project_root() / "configs" / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config not found: {config_path}\n"
            "Copy configs/config.example.yaml to configs/config.yaml"
        )

    with open(config_path) as f:
        return yaml.safe_load(f)


def get_output_path(filename, subdir=""):
    """Get path for output file with timestamp."""
    root = get_project_root()
    output_dir = root / "results" / subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return output_dir / f"{timestamp}_{filename}"


def run_tool(cmd, capture=True, timeout=300):
    """Run an external tool and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            capture_output=capture,
            text=True,
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        return None


def get_wordlist(name="common"):
    """Get path to a wordlist from the toolkit."""
    wordlists_dir = os.environ.get("WORDLISTS", "")
    seclists_dir = os.environ.get("SECLISTS", "")

    common_lists = {
        "common": f"{seclists_dir}/Discovery/Web-Content/common.txt",
        "directories": f"{seclists_dir}/Discovery/Web-Content/directory-list-2.3-medium.txt",
        "subdomains": f"{seclists_dir}/Discovery/DNS/subdomains-top1million-5000.txt",
        "passwords": f"{seclists_dir}/Passwords/Common-Credentials/10k-most-common.txt",
    }

    if name in common_lists:
        return common_lists[name]

    return None
