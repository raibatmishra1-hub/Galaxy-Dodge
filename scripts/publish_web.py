"""Build the web version with pygbag and copy it into docs/ for GitHub Pages.

Usage (from anywhere):
    python scripts/publish_web.py

Afterwards, commit and push docs/ to update the live game.
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / 'build' / 'web'
DOCS_DIR = REPO_ROOT / 'docs'


def main():
    # 1. Build with the same Python that runs this script (so it uses your conda env)
    print("Building with pygbag...")
    result = subprocess.run([sys.executable, '-m', 'pygbag', '--build', str(REPO_ROOT)])
    if result.returncode != 0:
        sys.exit("pygbag build failed, docs/ was not changed.")

    if not (BUILD_DIR / 'index.html').exists():
        sys.exit(f"Build finished but {BUILD_DIR / 'index.html'} is missing, docs/ was not changed.")

    # 2. Replace docs/ with a fresh copy of build/web
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    shutil.copytree(BUILD_DIR, DOCS_DIR, ignore=shutil.ignore_patterns('*.zip'))

    # 3. Tell GitHub Pages to serve files as-is
    (DOCS_DIR / '.nojekyll').touch()

    print(f"\nCopied build to {DOCS_DIR}:")
    for f in sorted(DOCS_DIR.iterdir()):
        print(f"  {f.name:25} {f.stat().st_size / 1024:>10,.0f} KB")
    print("\nNext: git add docs && git commit -m \"Update web build\" && git push")


if __name__ == "__main__":
    main()