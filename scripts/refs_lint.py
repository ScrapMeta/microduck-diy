#!/usr/bin/env python3
"""仓内引用校验：反引号与 markdown 链接里指向本仓的路径必须存在。

抓的是「指向已改名 / 已删除文件」这类漂移 —— 页面改了名、规则搬了家，
但别处还写着老路径。

判据分两层：

1. **哪些像仓内路径**：反引号片段的首段要命中 `root_entries() ∪ KNOWN_PREFIXES`。
   前者挡掉 `tof/src/sensor.rs`（上游仓内部的相对路径）这类噪声；
   后者收**历史前缀**，让「整个目录被删 / 改名」仍然会被查 —— 否则最该抓的那类漂移反而放行。
2. **缺席是否合法**：只看 `LOCAL_ONLY_PREFIXES` 一张显式表，**刻意不用 `git check-ignore`**
   —— 它的判定随「索引里有没有东西」而变，实测在空仓里会把每条路径都判成 ignored，
   于是所有引用被静默放行（校验形同虚设）。理由详见该常量。

退出码：0 = 通过；1 = 有 error。本脚本自身的正确性由 `scripts/lint_selftest.py` 注入故障验证。
"""

from __future__ import annotations

import fnmatch
import re
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
# 干净克隆里**合法缺席**的路径前缀（镜像 .gitignore —— 新增被 ignore 的目录时**两处一起改**）
#
# 这里**刻意不用 `git check-ignore`** 做判据：它的结果随「索引里有没有东西」而变
# —— 实测在空仓（`git init` + 全 untracked）里它把每条路径都判成 ignored，
# 于是所有引用被静默放行（校验形同虚设）。CRLF 的 `.gitignore` 在 Windows 上还会加剧这点。
# 跨平台确定的判据只有这一张显式表。
LOCAL_ONLY_PREFIXES = (
    "refs",  # 只读参考克隆
    "temp",
    "tmp",
    "microduck_ros2",  # 自有兄弟仓（不是只读，但不在本仓历史里）
    "vms",
    ".tmp",
    ".venv-cad",
    "res",
    "image/out",
    "wiki/raw/assets/press-kit",
    "wiki/raw/assets/microduck-releases",
)

# 「像仓内路径」的首段白名单 = 仓库根的**现存条目** ∪ 这里的**历史前缀**。
# 历史前缀必须在列 —— 否则「整个目录被删 / 改名」这类**最该抓**的漂移反而被放行。
# 本仓实例：`governance/` →（2026-09-19）`wiki/_archive/governance/`。
#
# ⚠️ 只收**无歧义**的旧前缀。`docs` 刻意不收：`docs/…` 在本仓各处指的是**别的仓里**的 docs
# （`imu_to_dxl/docs/` · `refs/microduck-replica/docs/` · 官方 `microduck/docs/robot/`）——
# 收进来会立刻产生 9 处假阳性。
KNOWN_PREFIXES = (
    "governance",  # 2026-09-19 前：治理细则 + 通用模板（现 wiki/_archive/governance/）
    "handoffs",  # 已废止的跨域交接包
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


def is_ignored(relpath: str) -> bool:
    """这个路径是不是「本来就不该存在」（干净克隆里合法缺席）？

    判据只有 LOCAL_ONLY_PREFIXES 一张显式表 —— 理由见该常量上方的注释。
    """
    return any(relpath == p or relpath.startswith(p + "/") for p in LOCAL_ONLY_PREFIXES)


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
    """从反引号片段里挑出「像仓内路径」的。

    首段必须命中 `root_entries() ∪ KNOWN_PREFIXES` —— 前者挡掉 `tof/src/sensor.rs`
    这类上游仓内部的相对路径，后者保证「整个目录被删」仍会被查。
    """
    roots = root_entries() | set(KNOWN_PREFIXES)
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
