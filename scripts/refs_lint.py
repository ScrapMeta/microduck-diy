#!/usr/bin/env python3
"""仓内引用校验：反引号与 markdown 链接里指向本仓的路径必须存在。

抓的是「指向已改名 / 已删除文件」这类漂移 —— 页面改了名、规则搬了家，
但别处还写着老路径。

**关键机制：用 `git check-ignore` 自己判断「这个路径是不是本来就不该存在」。**
`refs/` `temp/` `microduck_ros2/` 这些被 ignore 的本地件，在干净克隆里**合法缺席**；
不这么做 CI 会天天报假错。

判据（宁缺勿滥）：只有**首段命中仓库根的真实条目**的反引号片段才当作仓内路径 ——
`scripts/dxl_ping.py` 会查，`tof/src/sensor.rs`（上游仓内部相对路径）不查。

退出码：0 = 通过；1 = 有 error。
"""

from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
from pathlib import Path

try:  # Windows 控制台默认 cp936，中文报错会炸
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

REPO = Path(__file__).resolve().parent.parent

# --- 可调参数 ---------------------------------------------------------------
# 扫哪些文件
TARGETS = ["AGENTS.md", "README.md"]
TARGET_GLOBS = [
    "wiki/**/*.md",
    "scripts/**/*.md",
    ".cursor/skills/**/*.md",
    "imu_to_dxl/**/*.md",
    "image/**/*.md",
    "cad/**/*.md",
]
# 这些文件/目录不扫
EXCLUDE_GLOBS = [
    "wiki/_archive/*",  # 归档 = 冻结历史，不回溯校验（与 wiki_lint 的 SKIP_DIRS 一致）
    "wiki/raw/*",  # 不可变 ingest
    "wiki/log.md",  # 只追加的流水：历史引用不该回溯失效
    "refs/*",
    "temp/*",
    "vms/*",
    ".venv-cad/*",
    ".tmp/*",
]
# 干净克隆里**合法缺席**的路径前缀（镜像 .gitignore；check-ignore 不可用时兜底）
LOCAL_ONLY_PREFIXES = (
    "refs",
    "temp",
    "tmp",
    "microduck_ros2",
    "vms",
    ".tmp",
    ".venv-cad",
    "res",
    "image/out",
)
# 「像仓内路径」的判据：只允许 词字符 / `.` / `-` / `/`（**排除 `…` `*` `<` 这类省略与占位符**）
PATHLIKE_RE = re.compile(r"\w[\w.\-/]*")
# ---------------------------------------------------------------------------

BACKTICK_RE = re.compile(r"`([^`\n]+)`")
MDLINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
LINE_SUFFIX_RE = re.compile(r":\d+(-\d+)?$")
SKIP_LINK_SCHEMES = ("http://", "https://", "mailto:", "tel:", "ftp://", "#")


def rel(p: Path) -> str:
    try:
        return p.relative_to(REPO).as_posix()
    except ValueError:
        return str(p)


def root_entries() -> set[str]:
    """仓库根的真实条目 —— 反引号路径的「首段白名单」。"""
    return {p.name for p in REPO.iterdir() if p.name != ".git"}


_IGNORE_CACHE: dict[str, bool] = {}


def _git_ignores(relpath: str) -> bool:
    if relpath not in _IGNORE_CACHE:
        try:
            r = subprocess.run(
                ["git", "check-ignore", "-q", relpath],
                cwd=REPO,
                capture_output=True,
            )
        except (OSError, subprocess.SubprocessError):
            _IGNORE_CACHE[relpath] = False
        else:
            _IGNORE_CACHE[relpath] = r.returncode == 0
    return _IGNORE_CACHE[relpath]


def is_ignored(relpath: str) -> bool:
    """这个路径是不是「本来就不该存在」？

    **逐级向上**判断：只要任何一级祖先被 ignore，整条路径在干净克隆里就合法缺席。
    必须逐级 —— `image/out/foo.img` 的忽略规则是 `image/out/`（带尾斜杠的目录规则），
    而干净克隆里 `image/out` 本身不存在，`git check-ignore image/out/foo.img` 不一定命中。
    """
    if any(relpath == p or relpath.startswith(p + "/") for p in LOCAL_ONLY_PREFIXES):
        return True
    parts = relpath.split("/")
    for i in range(len(parts), 0, -1):
        cand = "/".join(parts[:i])
        if _git_ignores(cand) or _git_ignores(cand + "/"):
            return True
    return False


def targets() -> list[Path]:
    out: list[Path] = []
    for t in TARGETS:
        p = REPO / t
        if p.is_file():
            out.append(p)
    for g in TARGET_GLOBS:
        out.extend(sorted(REPO.glob(g)))
    keep: list[Path] = []
    seen: set[Path] = set()
    for p in out:
        if p in seen:
            continue
        seen.add(p)
        r = rel(p)
        if any(fnmatch.fnmatch(r, pat) for pat in EXCLUDE_GLOBS):
            continue
        keep.append(p)
    return keep


def backtick_candidates(text: str) -> list[str]:
    """从反引号片段里挑出「像仓内路径」的。"""
    roots = root_entries()
    found: list[str] = []
    for raw in BACKTICK_RE.findall(text):
        cand = raw.strip()
        if not cand or cand.startswith(("./", "../", "~/", "/", "-")):
            continue
        if "://" in cand:
            continue
        cand = LINE_SUFFIX_RE.sub("", cand).rstrip("/")
        if not cand or not PATHLIKE_RE.fullmatch(cand):
            continue
        head = cand.split("/", 1)[0]
        if head not in roots:
            continue
        found.append(cand)
    return found


def main() -> int:
    files = targets()
    errors: list[str] = []
    n_refs = 0

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        name = rel(f)

        for cand in backtick_candidates(text):
            n_refs += 1
            if (REPO / cand).exists():
                continue
            if is_ignored(cand):
                continue
            errors.append(f"{name}: 反引号路径不存在  `{cand}`")

        for target in MDLINK_RE.findall(text):
            if target.startswith(SKIP_LINK_SCHEMES) or "://" in target:
                continue
            pathpart = target.split("#", 1)[0]
            if not pathpart:
                continue
            n_refs += 1
            if (f.parent / pathpart).exists():
                continue
            repo_rel = rel((f.parent / pathpart).resolve())
            if is_ignored(repo_rel):
                continue
            errors.append(f"{name}: 链接不存在  [{target}]")

    print(f"refs_lint: 扫描 {len(files)} 文件 · {n_refs} 引用 · {len(errors)} error")
    for e in errors:
        print(f"  ERROR {e}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
