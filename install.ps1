<#
.SYNOPSIS
  br-web-seo installer for Windows (PowerShell 5.1+ / PowerShell 7).

.DESCRIPTION
  Installs the br-web-seo Agent Skill (a folder with SKILL.md) into the skills
  directory of one or more AI coding agents, at project or user (global) scope,
  or packages it for chat apps (ChatGPT, Claude.ai, Gemini).

  One-liner (no clone needed), defaults = all agents, project scope:
    irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1 | iex

  One-liner with options:
    & ([scriptblock]::Create((irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1))) -Agent all -Scope user

.PARAMETER Agent
  Comma-separated: claude, codex, gemini, copilot, cursor, agents, all.
  all (default) = claude + agents, which covers Claude Code, Codex, Gemini CLI
  and other tools that read .agents/skills.

.PARAMETER Scope
  project (default) = the current directory; user = your home folder (every project).

.PARAMETER Dir
  Install into an exact skills directory instead (any other tool).

.PARAMETER Package
  Build br-web-seo.zip + br-web-seo-bundle.md in the current directory, for
  uploading to ChatGPT / Claude.ai / Gemini.

.PARAMETER Uninstall
  Remove the skill from the selected locations.

.PARAMETER Force
  Overwrite without asking.
#>
[CmdletBinding()]
param(
  [string[]]$Agent = @("all"),
  [ValidateSet("project", "user")][string]$Scope = "project",
  [string]$Dir = "",
  [switch]$Package,
  [switch]$Uninstall,
  [switch]$Force
)

$ErrorActionPreference = "Stop"
$RepoUrl = "https://github.com/burhanriaz/BR-SEO-Skill"
$Skill = "br-web-seo"

# ---------- locate the skill source (local checkout, or download) ----------
$tmp = $null
$src = $null
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "$Skill\SKILL.md"))) {
  $src = Join-Path $PSScriptRoot $Skill
}
elseif (-not $Uninstall) {
  $tmp = Join-Path ([IO.Path]::GetTempPath()) ("br-seo-skill-" + [guid]::NewGuid().ToString("N"))
  New-Item -ItemType Directory -Force $tmp | Out-Null
  Write-Host "Downloading $Skill from $RepoUrl ..."
  if (Get-Command git -ErrorAction SilentlyContinue) {
    & git clone --quiet --depth 1 "$RepoUrl.git" (Join-Path $tmp "repo")
    if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
  }
  else {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $zip = Join-Path $tmp "main.zip"
    Invoke-WebRequest -UseBasicParsing "$RepoUrl/archive/refs/heads/main.zip" -OutFile $zip
    Expand-Archive -Path $zip -DestinationPath $tmp -Force
    Rename-Item (Join-Path $tmp "BR-SEO-Skill-main") "repo"
  }
  $src = Join-Path $tmp "repo\$Skill"
  if (-not (Test-Path (Join-Path $src "SKILL.md"))) { throw "Download failed: SKILL.md not found" }
}

try {
  # ---------- package mode: files for chat apps ----------
  if ($Package) {
    $out = (Get-Location).Path
    $zipOut = Join-Path $out "$Skill.zip"
    if (Test-Path $zipOut) { Remove-Item $zipOut -Force }
    # Build the zip by hand so entry paths use '/' (Compress-Archive on PS 5.1
    # writes '\', which some uploaders, Claude.ai included, reject).
    Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem
    $zipStream = [IO.Compression.ZipFile]::Open($zipOut, [IO.Compression.ZipArchiveMode]::Create)
    try {
      $root = Split-Path $src -Parent
      foreach ($file in (Get-ChildItem -Recurse -File $src)) {
        $entry = $file.FullName.Substring($root.Length + 1).Replace("\", "/")
        [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zipStream, $file.FullName, $entry)
      }
    }
    finally { $zipStream.Dispose() }

    $sb = New-Object System.Text.StringBuilder
    [void]$sb.AppendLine("# br-web-seo - single-file bundle")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("> This file is the whole br-web-seo skill in one document, for chat apps that")
    [void]$sb.AppendLine("> take uploaded knowledge files (ChatGPT Projects / Custom GPTs, Gemini Gems,")
    [void]$sb.AppendLine("> Claude Projects). Wherever SKILL.md says ``references/x.md`` or")
    [void]$sb.AppendLine("> ``templates/x.md``, find the section headed ``FILE: references/x.md`` below.")
    $files = @(Get-Item (Join-Path $src "SKILL.md")) +
             @(Get-ChildItem (Join-Path $src "references") -Filter *.md | Sort-Object Name) +
             @(Get-ChildItem (Join-Path $src "templates") -Filter *.md | Sort-Object Name)
    foreach ($f in $files) {
      $rel = $f.FullName.Substring($src.Length + 1).Replace("\", "/")
      [void]$sb.AppendLine("")
      [void]$sb.AppendLine("---")
      [void]$sb.AppendLine("")
      [void]$sb.AppendLine("<!-- ===================== FILE: $rel ===================== -->")
      [void]$sb.AppendLine("# FILE: $rel")
      [void]$sb.AppendLine("")
      [void]$sb.AppendLine([IO.File]::ReadAllText($f.FullName, [Text.Encoding]::UTF8))
    }
    $bundle = Join-Path $out "$Skill-bundle.md"
    [IO.File]::WriteAllText($bundle, $sb.ToString(), (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "Built:"
    Write-Host "  $zipOut         -> Claude.ai: Settings > Capabilities > Skills > Upload"
    Write-Host "  $bundle   -> ChatGPT / Gemini / Claude Projects: upload as a knowledge file"
    return
  }

  # ---------- resolve target directories ----------
  function Get-SkillBase([string]$a) {
    if ($Scope -eq "user") {
      $h = $HOME
      switch ($a) {
        "claude"  { return Join-Path $h ".claude\skills" }
        "codex"   { return Join-Path $h ".agents\skills" }
        "agents"  { return Join-Path $h ".agents\skills" }
        "gemini"  { return Join-Path $h ".gemini\skills" }
        "copilot" { return Join-Path $h ".copilot\skills" }
        "cursor"  { return Join-Path $h ".cursor\skills" }
      }
    }
    else {
      switch ($a) {
        "claude"  { return ".claude\skills" }
        "codex"   { return ".agents\skills" }
        "agents"  { return ".agents\skills" }
        "gemini"  { return ".gemini\skills" }
        "copilot" { return ".github\skills" }
        "cursor"  { return ".cursor\skills" }
      }
    }
  }

  $targets = New-Object System.Collections.Generic.List[string]
  if ($Dir) { $targets.Add($Dir) }
  else {
    foreach ($a in (($Agent -join ",") -split ",")) {
      $a = $a.Trim().ToLower()
      if ($a -eq "all") { $targets.Add((Get-SkillBase "claude")); $targets.Add((Get-SkillBase "agents")) }
      elseif (@("claude", "codex", "gemini", "copilot", "cursor", "agents") -contains $a) { $targets.Add((Get-SkillBase $a)) }
      else { throw "Unknown agent: $a (use claude, codex, gemini, copilot, cursor, agents, all)" }
    }
  }

  # ---------- install / uninstall ----------
  foreach ($base in ($targets | Select-Object -Unique)) {
    $dest = Join-Path $base $Skill
    if ($Uninstall) {
      if (Test-Path $dest) { Remove-Item -Recurse -Force $dest; Write-Host "Removed   $dest" }
      else { Write-Host "Absent    $dest" }
      continue
    }
    if ((Test-Path $dest) -and -not $Force -and [Environment]::UserInteractive -and -not [Console]::IsInputRedirected) {
      $ans = Read-Host "$dest exists. Overwrite? [Y/n]"
      if ($ans -match '^(n|no)$') { Write-Host "Skipped   $dest"; continue }
    }
    New-Item -ItemType Directory -Force $base | Out-Null
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse -Force $src $dest
    Write-Host "Installed $dest"
  }

  if (-not $Uninstall) {
    Write-Host ""
    Write-Host "Done. Restart your agent (or start a new session), then ask:"
    Write-Host '  "Use the br-web-seo skill to audit https://example.com"'
    Write-Host "Claude Code: /br-web-seo   -   Gemini CLI: /skills list   -   Codex: /skills"
  }
}
finally {
  if ($tmp -and (Test-Path $tmp)) { Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue }
}
