#!/usr/bin/env python3
"""Development script for documentation management."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str]) -> None:
    """Run a command and handle errors."""
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(cmd)}: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python docs-dev.py <command>")
        print("Commands:")
        print("  serve     - Serve docs locally")
        print("  build     - Build docs")
        print("  deploy    - Deploy docs (requires version)")
        print("  version   - Show current version")
        sys.exit(1)

    command = sys.argv[1]

    if command == "serve":
        run_command(["mkdocs", "serve"])
    elif command == "build":
        run_command(["mkdocs", "build"])
    elif command == "deploy":
        if len(sys.argv) < 3:
            print("Usage: python docs-dev.py deploy <version>")
            sys.exit(1)
        version = sys.argv[2]
        run_command(["mike", "deploy", "--push", "--update-aliases", version, "latest"])
    elif command == "version":
        # Read version from _version.py
        version_file = Path("src/marvelpy/_version.py")
        if version_file.exists():
            with open(version_file) as f:
                content = f.read()
                # Extract version from __version__ = "0.1.0"
                for line in content.split("\n"):
                    if line.startswith("__version__"):
                        version = line.split('"')[1]
                        print(f"Current version: {version}")
                        break
        else:
            print("Version file not found")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
