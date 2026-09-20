#!/usr/bin/env python3
"""两台 linter 的自检：**注入故障，断言它们真的报错**。

理由很直接 —— 一台永远 exit 0 的 linter 和没有 linter 一样，但看起来更有保障。
2026-09-19 首次跑这种自检时，`refs_lint` 的两个真 bug 才暴露出来：
「整个目录被删」的引用被放行；`git check-ignore` 的判定让所有引用在空仓里静默通过。
**这两条在正常使用中都不会报错，只会悄悄地什么都不查。**

做法：把仓库克隆到临时目录（**绝不碰工作树**），在里面种下已知故障，跑两台 linter，
断言每条故障都出现在输出里；再删掉种下的文件，断言两台都回到 exit 0（无假阳性）。

跑法：`python scripts/lint_selftest.py`（CI 里紧跟两台 linter 之后）。

退出码：0 = 每条故障都被抓到且干净克隆全绿；1 = 有漏报或假阳性。
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:  # Windows 控制台默认 cp936，中文报错会炸
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent

sys.path.insert(0, str(SCRIPTS))
from wiki_lint import OVERSIZE_ACK  # noqa: E402  （拿记账表，自检跟着它走）

# 合法 frontmatter —— 探针页除了被测的那一项，其余都要合规，否则分不清是哪个规则在报错
FM_OK = """---
title: selftest probe
created: 2000-01-01
updated: 2000-01-01
type: concept
tags: []
---

"""

# wiki_lint 探针：wiki 内相对路径 -> (内容, 期望出现在输出里的片段)
WIKI_PROBES: dict[str, tuple[str, str]] = {
    "concepts/_selftest-nofm.md": ("# 故意不写 frontmatter\n", "缺 frontmatter"),
    "concepts/_selftest-oversize.md": (
        FM_OK + "填充行\n" * 260,
        "> 200，请拆页",
    ),
    "concepts/_selftest-deadlink.md": (
        FM_OK + "见 [[绝对不存在的页]]。\n",
        "死链 [[绝对不存在的页]]",
    ),
}

# BOM 探针**单独拿**出来：它是唯一必须用 `utf-8-sig` 写下的故障（其余探针都是无 BOM 的）
BOM_PROBE = "concepts/_selftest-bom.md"
BOM_PROBE_BODY = FM_OK + "一个带 BOM 的页。\n"
BOM_PROBE_EXPECT = "带 UTF-8 BOM"

# refs_lint 探针：每行一个已知故障，期望片段与之一一对应
REFS_PROBE = "scripts/_selftest-refs.md"
REFS_PROBE_BODY = (
    "已删的整棵目录 `governance/agent-governance.md`\n"
    "已删的单文件 `wiki/SCHEMA.md`\n"
    "死链 [老页](concepts/早就删了.md)\n"
)
REFS_PROBE_EXPECT = [
    "反引号路径不存在  `governance/agent-governance.md`",
    "反引号路径不存在  `wiki/SCHEMA.md`",
    "链接不存在  [concepts/早就删了.md]",
]


def rmtree(path: Path) -> None:
    """Windows 上 .git 里的只读文件会让 rmtree 半途而废 —— 先清只读位。"""

    def on_error(func, target, _exc):  # noqa: ANN001
        try:
            Path(target).chmod(0o777)
            func(target)
        except Exception:  # pragma: no cover
            pass

    shutil.rmtree(path, onerror=on_error)


def run(script: str, cwd: Path) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, str(cwd / "scripts" / script)],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main() -> int:
    tmp_root = REPO / "temp"
    tmp_root.mkdir(exist_ok=True)
    clone = Path(tempfile.mkdtemp(prefix="lint-selftest-", dir=tmp_root))
    rmtree(clone)
    failures: list[str] = []
    try:
        subprocess.run(
            ["git", "clone", "-q", "--no-hardlinks", str(REPO), str(clone)],
            check=True,
            capture_output=True,
        )
        # 克隆带的是**已提交**的 linter；覆盖成工作区的，测的才是你正要提交的那版
        for s in ("wiki_lint.py", "refs_lint.py"):
            shutil.copy2(SCRIPTS / s, clone / "scripts" / s)

        # ---- 种下故障 --------------------------------------------------
        for relp, (body, _) in WIKI_PROBES.items():
            (clone / "wiki" / relp).write_text(body, encoding="utf-8")
        (clone / REFS_PROBE).write_text(REFS_PROBE_BODY, encoding="utf-8")
        (clone / "wiki" / BOM_PROBE).write_text(BOM_PROBE_BODY, encoding="utf-8-sig")

        # 「只减不增」探针：给记账表里的第一页加一行，页长就超了记账值
        ack_target = next(
            (k for k in OVERSIZE_ACK if (clone / "wiki" / k).is_file()), None
        )
        ack_original = None
        if ack_target:
            p = clone / "wiki" / ack_target
            ack_original = p.read_text(encoding="utf-8")
            p.write_text(ack_original + "多出来的一行\n", encoding="utf-8")

        wiki_rc, wiki_out = run("wiki_lint.py", clone)
        refs_rc, refs_out = run("refs_lint.py", clone)

        # ---- 断言每条故障都被抓到 --------------------------------------
        cases: list[tuple[str, str, str]] = [
            (f"wiki_lint 抓到 {label}", wiki_out, needle)
            for label, (_, needle) in WIKI_PROBES.items()
        ]
        cases.append((f"wiki_lint 抓到 BOM（{BOM_PROBE}）", wiki_out, BOM_PROBE_EXPECT))
        if ack_target:
            cases.append(
                (f"wiki_lint 抓到 超记账值（{ack_target}）", wiki_out, "只减不增")
            )
        cases += [
            (f"refs_lint 抓到 {needle}", refs_out, needle)
            for needle in REFS_PROBE_EXPECT
        ]

        caught = 0
        for label, output, needle in cases:
            ok = needle in output
            caught += ok
            print(f"  {'抓到  ' if ok else '漏掉!!'} {label}")
            if not ok:
                failures.append(label)
        if wiki_rc == 0:
            failures.append("wiki_lint 种了故障仍 exit 0")
        if refs_rc == 0:
            failures.append("refs_lint 种了故障仍 exit 0")

        # ---- 撤掉故障：干净克隆必须全绿（假阳性检查）-------------------
        for relp in WIKI_PROBES:
            (clone / "wiki" / relp).unlink()
        (clone / "wiki" / BOM_PROBE).unlink()
        (clone / REFS_PROBE).unlink()
        if ack_target and ack_original is not None:
            (clone / "wiki" / ack_target).write_text(ack_original, encoding="utf-8")

        print()
        for script in ("wiki_lint.py", "refs_lint.py"):
            rc, out = run(script, clone)
            head = out.strip().splitlines()[0] if out.strip() else ""
            ok = rc == 0
            print(f"  {'干净  ' if ok else '假阳性!!'} {script}: {head}")
            if not ok:
                failures.append(f"{script} 干净克隆报假阳性")

        print(f"\nlint_selftest: {len(cases)} 条故障抓到 {caught} 条")
        for f in failures:
            print(f"  FAIL {f}")
        return 1 if failures else 0
    finally:
        rmtree(clone)


if __name__ == "__main__":
    raise SystemExit(main())
