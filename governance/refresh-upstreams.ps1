# refresh-upstreams.ps1 - regenerate governance/upstreams.lock
#
# Purpose: record every reference clone (dir / remote / branch / HEAD / dirty count /
#          behind-ahead) so "which upstream version are we on" stays reviewable
#          without git submodules (governance section 10.3).
#
# Usage (from anywhere):
#   powershell -ExecutionPolicy Bypass -File governance\refresh-upstreams.ps1
#   powershell -ExecutionPolicy Bypass -File governance\refresh-upstreams.ps1 -Fetch
#
# -Fetch contacts every remote first (network). Without it the Behind / Ahead columns are
# only as fresh as each clone's LAST fetch - which may be its clone date, so they can read
# 0 while upstream has moved on. The generated header records which mode produced it.
#
# Layout it assumes (governance section 10): the workspace root IS this repository's
# worktree, so read-only clones live under refs/ and are .gitignored. Owned sibling
# repos sit at the root and are .gitignored too, but are NOT read-only.
#
# Read-only: never modifies any repository.
# ASCII-only on purpose: Windows PowerShell 5.1 reads BOM-less .ps1 as ANSI,
# so non-ASCII source breaks parsing. Keep this file ASCII.

param(
    [switch]$Fetch
)

$ErrorActionPreference = 'Stop'

$governanceDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path $MyInvocation.MyCommand.Path -Parent }
$repoRoot      = Split-Path $governanceDir -Parent          # workspace root = this repo's worktree
$refsDir       = Join-Path $repoRoot 'refs'

# Owned sibling repos: writable, pushed separately, ignored like the clones.
$ownedSiblings = @('microduck_ros2')
$out = Join-Path $governanceDir 'upstreams.lock'

function Get-GitValue {
    param([string]$Dir, [string[]]$GitArgs)
    # Local error preference so a missing remote / unborn HEAD cannot abort the run.
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    Push-Location $Dir
    try { return (& git @GitArgs 2>$null) } catch { return $null }
    finally { Pop-Location; $ErrorActionPreference = $prev }
}

# This repo first, then owned siblings, then every clone under refs/.
$targets = @([PSCustomObject]@{ Label = '(this repo)'; Dir = $repoRoot; Kind = 'owned' })
foreach ($n in $ownedSiblings) {
    $p = Join-Path $repoRoot $n
    if (Test-Path (Join-Path $p '.git')) {
        $targets += [PSCustomObject]@{ Label = $n; Dir = $p; Kind = 'owned' }
    } else {
        Write-Warning ("owned sibling '{0}' has no .git; create the repo first" -f $n)
    }
}
if (Test-Path $refsDir) {
    foreach ($d in Get-ChildItem $refsDir -Directory | Sort-Object Name) {
        if (-not (Test-Path (Join-Path $d.FullName '.git'))) { continue }
        $targets += [PSCustomObject]@{ Label = 'refs/' + $d.Name; Dir = $d.FullName; Kind = 'readonly' }
    }
} else {
    Write-Warning ("no {0} directory; no reference clones recorded" -f $refsDir)
}

$rows = @()
foreach ($t in $targets) {
    # Off by default: the script stays offline and instant. Behind/Ahead are then only as
    # fresh as the last fetch in that clone, which for a clone nobody has touched since is
    # its clone date - hence the header this run writes.
    if ($Fetch) { Get-GitValue $t.Dir @('fetch', '--quiet', 'origin') | Out-Null }
    $remote = Get-GitValue $t.Dir @('remote', 'get-url', 'origin')
    if ([string]::IsNullOrWhiteSpace($remote)) { $remote = '(none)' }
    $branch = Get-GitValue $t.Dir @('rev-parse', '--abbrev-ref', 'HEAD')
    if ([string]::IsNullOrWhiteSpace($branch)) { $branch = '(none)' }
    $head   = Get-GitValue $t.Dir @('rev-parse', '--short', 'HEAD')
    if ([string]::IsNullOrWhiteSpace($head)) { $head = '(none)' }
    $dirty  = @(Get-GitValue $t.Dir @('status', '--porcelain')).Count

    # Behind / ahead of upstream. Left count = commits in origin not in HEAD (behind);
    # right count = commits in HEAD not in origin (ahead). Blank when unmatchable.
    $behind = ''; $ahead = ''
    if ($branch -ne '(none)') {
        $lr = Get-GitValue $t.Dir @('rev-list', '--left-right', '--count', "origin/$branch...HEAD")
        if ($lr -match '^(\d+)\s+(\d+)$') { $behind = $Matches[1]; $ahead = $Matches[2] }
    }

    $rows += [PSCustomObject]@{
        Dir = $t.Label; Kind = $t.Kind; Remote = $remote; Branch = $branch
        Head = $head; Dirty = $dirty; Behind = $behind; Ahead = $ahead
    }
}

$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'
$bt = [char]96
if ($Fetch) {
    $fetchNote = 'remotes contacted by this run (-Fetch): Behind/Ahead are current'
} else {
    $fetchNote = 'NO fetch by this run: Behind/Ahead are only as fresh as each clone last was'
}

$md = New-Object System.Collections.Generic.List[string]
$md.Add('# Upstream version lock (upstreams.lock)')
$md.Add('')
$md.Add('> Generated: ' + $stamp + ' by ' + $bt + 'refresh-upstreams.ps1' + $bt + ' - do not hand-edit.')
$md.Add('> Remote state: ' + $fetchNote + '.')
$md.Add('> Replaces git submodules for pinning reference-clone versions (governance 10.3).')
$md.Add('> ' + $bt + '(this repo)' + $bt + ' is the base repository: the workspace root IS its worktree (governance 10).')
$md.Add('> A non-zero ' + $bt + 'Dirty' + $bt + ' on a ' + $bt + 'readonly' + $bt + ' row is a violation: reference clones must stay clean (governance 11).')
$md.Add('')
$md.Add('| Dir | Kind | Remote | Branch | HEAD | Dirty | Behind | Ahead |')
$md.Add('|-----|------|--------|--------|------|-------|--------|-------|')
foreach ($r in $rows) {
    $line = '| ' + $bt + $r.Dir + $bt + ' | ' + $r.Kind + ' | ' + $r.Remote + ' | ' + $r.Branch +
            ' | ' + $bt + $r.Head + $bt + ' | ' + $r.Dirty + ' | ' + $r.Behind + ' | ' + $r.Ahead + ' |'
    $md.Add($line)
}
$md.Add('')
$md.Add('## Checks')
$md.Add('')
$md.Add('- Owned rows must have a remote; if one is missing, create the GitHub repo first.')
$md.Add('- Every readonly row must show Dirty = 0. If not, clean it or export the work into an owned repo.')
$md.Add('- Non-zero Behind means a reference clone lags upstream; decide whether to update.')
$md.Add('- A zero Behind proves nothing unless this run used ' + $bt + '-Fetch' + $bt + ': it may only mean nobody fetched since the clone.')
$md.Add('- New clones belong in ' + $bt + 'refs/' + $bt + ', which is .gitignored. Never run ' + $bt + 'git clean -x' + $bt + ' (governance 10.4).')
$md.Add('')

[System.IO.File]::WriteAllText($out, ($md -join "`n"), (New-Object System.Text.UTF8Encoding $false))
Write-Host ("Wrote {0} ({1} repos)" -f $out, $rows.Count)
