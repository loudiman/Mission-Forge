$ErrorActionPreference = 'Stop'

Write-Host "Installing Mission-Forge..."

# Check required tools
if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Error "python not found. Install it from https://python.org"
    exit 1
}

if (-not (Get-Command pip -ErrorAction SilentlyContinue) -and -not (Get-Command pip3 -ErrorAction SilentlyContinue)) {
    Write-Error "pip not found. Install it from https://python.org"
    exit 1
}

if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
    Write-Error "npx not found. Install Node.js 18+ from https://nodejs.org"
    exit 1
}

pip install git+https://github.com/loudiman/Mission-Forge.git
if ($?) { npx -y skills add loudiman/Mission-Forge }

Write-Host "✓ missionforge CLI installed"
Write-Host "✓ Agent skills installed"
Write-Host "Run ``missionforge init MF-001`` to create your first mission."
