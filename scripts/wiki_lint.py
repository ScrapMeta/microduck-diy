#!/usr/bin/env python3
"""wiki 规范校验：frontmatter · 行数 · 死链。

机械执行 `AGENTS.md` 定下的 wiki 硬规范 —— **本脚本的判定即规格**：

  1. 正文页必须有 frontmatter：`title` `created` `updated` `type` `tags`
  2. 正文页 ≤ MAX_LINES 行（超了拆页）
  3. `[[wikilink]]` 与仓内相对 `.md` 链接必须解析得到

豁免：

  * `SKIP_DIRS`（`raw/` `_archive/` `assets/`）整体跳过 —— `raw/` 是时点快照，
    改它的链接等于篡改历史记录；`_archive/` 是停用页，已撤出导航。
  * `META_NAMES`（wiki 根的导航类文件）不要求 frontmatter、不限行数。

退出码：0 = 通过（可以只有 warning）；1 = 有 error。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:  # Windows 控制台默认 cp936，中文报错会炸
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

REPO = Path(__file__).resolve().parent.parent
WIKI = REPO / "wiki"

# --- 可调参数 ---------------------------------------------------------------
META_NAMES = {"index.md", "log.md", "tasks.md"}  # wiki 根的导航类文件
LINK_EXEMPT_NAMES = {"log.md"}  # 只追加的流水：历史链接不该回溯失效
SKIP_DIRS = {"raw", "_archive", "assets"}  # 历史 / 素材，整体豁免
MAX_LINES = 200
# 「已批准例外 · 不拆页」—— Human 2026-09-19 决定：下列页**不拆**（都是「单页件」，拆了就不成一件事），
# 超 200 行属既定状态，不是欠账。**只减不增**：数值是当下账面，页长只能降不能升 —— 要涨先在**这里**改数值
# （= 显式记账）。改规格前先读 AGENTS.md「谁能改什么」。出处：wiki/log.md 2026-09-19 · wiki/tasks.md T-08。
OVERSIZE_ACK = {
    # 对外可发送件：PDF 由本页生成，拆页就不成一封信了
    "queries/rd05t-vendor-inquiry-2026-09-18.md": 203,
    # 对比页：T-10 回函结论还要写进来
    "comparisons/xl330-vs-kpower-rd05t.md": 220,
}
REQUIRED_KEYS = ("title", "created", "updated", "type", "tags")
IGNORE_WIKILINKS = {"...", ""}
# ---------------------------------------------------------------------------

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*)[ \t]*:(.*)$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKIP_LINK_SCHEMES = ("http://", "https://", "mailto:", "tel:", "ftp://", "#")


def rel(p: Path) -> str:
    try:
        return p.relative_to(REPO).as_posix()
    except ValueError:
        return str(p)


def is_skipped(p: Path) -> bool:
    return any(part in SKIP_DIRS for part in p.relative_to(WIKI).parts[:-1])


def parse_frontmatter(text: str) -> dict[str, str] | None:
    m = FM_RE.match(text)
    if not m:
        return None
    keys: dict[str, str] = {}
    for line in m.group(1).splitlines():
        km = KEY_RE.match(line)
        if km:
            keys[km.group(1)] = km.group(2).strip()
    return keys


def build_page_index() -> dict[str, Path]:
    """wikilink 解析表：**含** raw/ 与 _archive/ —— 指向历史页的链接是合法的。"""
    idx: dict[str, Path] = {}
    for p in WIKI.rglob("*.md"):
        idx.setdefault(p.stem.lower(), p)
    return idx


def check_link_resolves(target: str, pages: dict[str, Path], host: Path) -> str | None:
    """返回 None = 通过，否则返回人类可读的原因。"""
    t = target.strip()
    if t in IGNORE_WIKILINKS:
        return None
    if t.lower() in pages:
        return None
    # 允许写成相对路径（[[concepts/foo]]）
    if (WIKI / t).with_suffix(".md").exists() or (WIKI / t).exists():
        return None
    if (host.parent / t).with_suffix(".md").exists():
        return None
    return f"死链 [[{t}]]"


def main() -> int:
    if not WIKI.is_dir():
        print(f"wiki_lint: 找不到 {rel(WIKI)}")
        return 1

    pages = build_page_index()
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0

    for md in sorted(WIKI.rglob("*.md")):
        if is_skipped(md):
            continue
        checked += 1
        text = md.read_text(encoding="utf-8", errors="replace").removeprefix("\ufeff")
        name = rel(md)
        nlines = text.count("\n") + (0 if text.endswith("\n") else 1)
        meta_file = md.name in META_NAMES and md.parent == WIKI

        # 1) frontmatter
        if not meta_file:
            fm = parse_frontmatter(text)
            if fm is None:
                errors.append(f"{name}: 缺 frontmatter（需 {' '.join(REQUIRED_KEYS)}）")
            else:
                for k in REQUIRED_KEYS:
                    if k not in fm:
                        errors.append(f"{name}: frontmatter 缺 `{k}`")
                for k in ("created", "updated"):
                    v = fm.get(k, "")
                    if v and not DATE_RE.match(v):
                        errors.append(f"{name}: `{k}: {v}` 不是 YYYY-MM-DD")
                c, u = fm.get("created", ""), fm.get("updated", "")
                if DATE_RE.match(c) and DATE_RE.match(u) and u < c:
                    warnings.append(f"{name}: `updated`({u}) 早于 `created`({c})")

            # 2) 行数（含「已批准例外 · 只减不增」记账）
            key = md.relative_to(WIKI).as_posix()
            ack = OVERSIZE_ACK.get(key)
            if nlines > MAX_LINES:
                if ack is None:
                    errors.append(f"{name}: {nlines} 行 > {MAX_LINES}，请拆页")
                elif nlines > ack:
                    errors.append(f"{name}: {nlines} 行 > 记账值 {ack} —— 已批准例外 · 只减不增：要涨先在 scripts/wiki_lint.py 改记账值")
                else:
                    warnings.append(f"{name}: {nlines} 行 > {MAX_LINES}（已批准例外 · 不拆页 · 记账 {ack}）")
            elif ack is not None:
                warnings.append(f"{name}: 已降到 {nlines} 行 ≤ {MAX_LINES} —— 请从 wiki_lint.py 的 OVERSIZE_ACK 删掉这一行")

        # 3) 死链（log.md 豁免：只追加的流水，历史链接不该回溯失效）
        if md.name in LINK_EXEMPT_NAMES:
            continue
        for m in WIKILINK_RE.finditer(text):
            reason = check_link_resolves(m.group(1), pages, md)
            if reason:
                errors.append(f"{name}: {reason}")

        for m in MDLINK_RE.finditer(text):
            target = m.group(1)
            if target.startswith(SKIP_LINK_SCHEMES) or "://" in target:
                continue
            if not target.endswith(".md"):
                continue
            pathpart = target.split("#", 1)[0]
            if not (md.parent / pathpart).exists():
                errors.append(f"{name}: 死链 `[{target}]`（相对本页）")

    print(f"wiki_lint: 检查 {checked} 页 · {len(errors)} error · {len(warnings)} warning")
    for w in warnings:
        print(f"  warn  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
