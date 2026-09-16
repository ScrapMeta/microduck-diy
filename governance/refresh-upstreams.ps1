# refresh-upstreams.ps1 - regenerate governance/upstreams.lock
#
# Purpose: record each clone in the workspace (dir / remote / branch / HEAD /
#          dirty count / behind-ahead) so "which upstream version are we on"
#          stays reviewable without git submodules (governance section 10.3).
#
# Usage (from anywhere):
#   powershell -ExecutionPolicy Bypass -File microduck-diy\governance\refresh-upstreams.ps1
#
# Read-only: never modifies any repository.
# ASCII-only on purpose: Windows PowerShell 5.1 reads BOM-less .ps1 as ANSI,
# so non-ASCII source breaks parsing. Keep this file ASCII.

$ErrorActionPreference = 'Stop'

$governanceDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path $MyInvocation.MyCommand.Path -Parent }
$baseRepoDir   = Split-Path $governanceDir -Parent          # microduck-diy/
$workspaceRoot = Split-Path $baseRepoDir -Parent            # workspace root

# Repos owned by this project (writable). Everything else is read-only upstream.
$owned = @('microduck-diy', 'microduck_ros2')
$out   = Join-Path $governanceDir 'upstreams.lock'

function Get-GitValue {
    param([string]$Dir, [string[]]$GitArgs)
    Push-Location $Dir
    try { return (& git @GitArgs 2>$null) } finally { Pop-Location }
}

$rows = @()
foreach ($d in Get-ChildItem $workspaceRoot -Directory | Sort-Object Name) {
    if (-not (Test-Path (Join-Path $d.FullName '.git'))) { continue }

    $remote = Get-GitValue $d.FullName @('remote', 'get-url', 'origin')
    $branch = Get-GitValue $d.FullName @('rev-parse', '--abbrev-ref', 'HEAD')
    $head   = Get-GitValue $d.FullName @('rev-parse', '--short', 'HEAD')
    $dirty  = @(Get-GitValue $d.FullName @('status', '--porcelain')).Count

    # Behind / ahead of upstream. Left count = commits in origin not in HEAD (behind);
    # right count = commits in HEAD not in origin (ahead). Blank when unmatchable.
    $lr = Get-GitValue $d.FullName @('rev-list', '--left-right', '--count', "origin/$branch...HEAD")
    $behind = ''; $ahead = ''
    if ($lr -match '^(\d+)\s+(\d+)$') { $behind = $Matches[1]; $ahead = $Matches[2] }

    $kind = if ($owned -contains $d.Name) { 'owned' } else { 'readonly' }
    $rows += [PSCustomObject]@{
        Dir = $d.Name; Kind = $kind; Remote = $remote; Branch = $branch
        Head = $head; Dirty = $dirty; Behind = $behind; Ahead = $ahead
    }
}

$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'
$bt = [char]96

$md = New-Object System.Collections.Generic.List[string]
$md.Add('# Upstream version lock (upstreams.lock)')
$md.Add('')
$md.Add('> Generated: ' + $stamp + ' by ' + $bt + 'refresh-upstreams.ps1' + $bt + ' - do not hand-edit.')
$md.Add('> Replaces git submodules for pinning upstream versions (governance 10.3).')
$md.Add('> A non-zero ' + $bt + 'Dirty' + $bt + ' on a ' + $bt + 'readonly' + $bt + ' row is a violation: upstream clones must stay clean (governance 11).')
$md.Add('')
$md.Add('| Dir | Kind | Remote | Branch | HEAD | Dirty | Behind | Ahead |')
$md.Add('|-----|------|--------|--------|------|-------|--------|-------|')
foreach ($r in $rows) {
    $line = '| ' + $bt + $r.Dir + '/' + $bt + ' | ' + $r.Kind + ' | ' + $r.Remote + ' | ' + $r.Branch +
            ' | ' + $bt + $r.Head + $bt + ' | ' + $r.Dirty + ' | ' + $r.Behind + ' | ' + $r.Ahead + ' |'
    $md.Add($line)
}
$md.Add('')
$md.Add('## Checks')
$md.Add('')
$md.Add('- Owned dirs must have a .git and a remote; if missing, create the repo first.')
$md.Add('- Every readonly row must show Dirty = 0. If not, clean it or export the work into an owned repo.')
$md.Add('- Non-zero Behind means the reference clone lags upstream; decide whether to update.')
$md.Add('')

[System.IO.File]::WriteAllText($out, ($md -join "`n"), (New-Object System.Text.UTF8Encoding $false))
Write-Host ("Wrote {0} ({1} clones)" -f $out, $rows.Count)
