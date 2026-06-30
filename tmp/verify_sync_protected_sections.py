#!/usr/bin/env python3
import hashlib
import re
import subprocess
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
SYNC_SCRIPT = ROOT / "script" / "sync_multilingual_readmes.py"

LOCALES = {
    "README_de.md": {"news": "Neuigkeiten", "menu": "Menu"},
    "README_es.md": {"news": "Novedades", "menu": "Menu"},
    "README_fr.md": {"news": "Actualites", "menu": "Menu"},
    "README_ja.md": {"news": "最新情報", "menu": "Menu"},
    "README_ko.md": {"news": "최신 소식", "menu": "Menu"},
    "README_pt.md": {"news": "Novidades", "menu": "Menu"},
    "README_ru.md": {"news": "Новости", "menu": "Menu"},
    "README_tr.md": {"news": "Haberler", "menu": "Menu"},
    "README_zh-CN.md": {"news": "最新动态", "menu": "Menu"},
    "README_zh-TW.md": {"news": "最新動態", "menu": "目錄"},
}


def heading_pattern(title: str, emoji: Optional[str] = None) -> str:
    emoji_part = rf"(?:{re.escape(emoji)}\s+)?" if emoji else ""
    return rf"^##\s+{emoji_part}{re.escape(title)}\s*$"


def extract_section(text: str, title: str, emoji: Optional[str] = None) -> str:
    patterns = [heading_pattern(title, emoji)]
    if title == "Menu":
        patterns.append(heading_pattern("Menu", "📑"))
    for pattern in patterns:
        match = re.search(rf"(?ms)({pattern}\n.*?)(?=^##\s+|\Z)", text)
        if match:
            return match.group(1).rstrip() + "\n"
    raise RuntimeError(f"missing section: {title}")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def snapshot() -> dict:
    data = {}
    for name, titles in LOCALES.items():
        text = (ROOT / name).read_text(encoding="utf-8")
        data[name] = {
            "news": digest(extract_section(text, titles["news"])),
            "menu": digest(extract_section(text, titles["menu"], "📑" if titles["menu"] != "目錄" else None)),
        }
    return data


before = snapshot()
subprocess.run(["python3", str(SYNC_SCRIPT)], cwd=ROOT, check=True)
after = snapshot()

if before != after:
    raise SystemExit(f"Protected section hashes changed:\nBEFORE={before}\nAFTER={after}")

status = subprocess.run(
    ["git", "diff", "--name-only", "--", *LOCALES.keys()],
    cwd=ROOT,
    check=True,
    capture_output=True,
    text=True,
)
changed = [line for line in status.stdout.splitlines() if line.strip()]
if changed:
    raise SystemExit(f"Localized README files changed unexpectedly: {changed}")

print("PASS: localized News/Menu sections remained unchanged and no localized README diff was introduced.")
