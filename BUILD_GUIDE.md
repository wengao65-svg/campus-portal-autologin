# Developer Guide: Building Standalone Executable

## Overview

This guide explains how to build the standalone Windows executable for campus-portal-autologin.

## Prerequisites

- Windows 10 or higher
- Python 3.8 or higher
- Administrative privileges (for Task Scheduler setup)

## Build Steps

### Option 1: Automated Build (Recommended)

#### Using GitHub Actions

1. Push code to GitHub (already done!)
2. GitHub Actions will automatically build the executable
3. Download the artifact from Actions page
4. Create a release to publish

#### Using Build Script

```bash
# Clone repository
git clone https://github.com/wengao65-svg/campus-portal-autologin.git
cd campus-portal-autologin

# Run build script
python build_executable.py
```

This will:
- Clean previous builds
- Install dependencies
- Install Playwright browsers (bundled mode)
- Build standalone executable
- Output: `dist/CampusPortalAutologin/`

### Option 2: Manual Build with PyInstaller

```bash
# Create virtual environment
python -m venv playwright-build
source playwright-build/Scripts/activate  # Windows

# Install dependencies
pip install playwright==1.40.0 pyinstaller

# Install browsers in bundled mode
$env:PLAYWRIGHT_BROWSERS_PATH="0"
playwright install chromium

# Build executable
pyinstaller --clean \
    --name=CampusPortalAutologin \
    --onedir \
    --console \
    --add-data="config.json.template:." \
    --add-data="install_task.py:." \
    --add-data="remove_task_scheduler.bat:." \
    --add-data="run_hidden.vbs:." \
    --add-data="README_STANDALONE.md:." \
    --hidden-import=playwright \
    --hidden-import=playwright.sync_api \
    --hidden-import=playwright._impl._api_types \
    --hidden-import=playwright._impl._driver \
    --hidden-import=playwright.driver \
    src/campus_auto_connect_browser.py
```

## Testing the Build

### 1. Create Test Configuration

```bash
cd dist/CampusPortalAutologin
copy config.json.template config.json
```

Edit `config.json` with test credentials.

### 2. Run Executable

```bash
CampusPortalAutologin.exe
```

### 3. Verify Output

- Check that browser launches
- Verify login attempt
- Check logs in `campus_connect.log`

## Build Output

The build process creates:

```
dist/CampusPortalAutologin/
├── CampusPortalAutologin.exe       # Main executable
├── config.json.template            # Configuration template
├── install_task.py                # Install script
├── remove_task_scheduler.bat         # Uninstall script
├── run_hidden.vbs                 # Run script
├── README_STANDALONE.md          # Standalone usage guide
└── [Internal PyInstaller files]     # Python runtime and dependencies
```

## Creating Release

### 1. Create ZIP Package

```bash
cd dist
powershell Compress-Archive -Path CampusPortalAutologin -DestinationPath CampusPortalAutologin.zip -Force
```

### 2. Create GitHub Release

1. Go to GitHub → Releases
2. Click "Create a new release"
3. Tag version (e.g., `v1.0.0`)
4. Upload `CampusPortalAutologin.zip`
5. Add release notes

## Common Build Issues

### Issue: "playwright.sync_api not found"

**Solution**: Playwright not installed. Run:
```bash
pip install playwright
```

### Issue: Browser not found

**Solution**: Install browsers in bundled mode:
```bash
PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
```

### Issue: Large executable size

**Expected**: 150-300MB is normal for Playwright + Chromium.

**To reduce size**:
- Install only needed browser (chromium, not firefox)
- Exclude unused modules in spec file

### Issue: Antivirus detection

**Solution**: False positive. Add to antivirus whitelist or code sign the executable.

## Advanced Configuration

### Custom Icon

Add an icon file (`.ico`):

```bash
pyinstaller --icon=app.ico --name=MyApp main.py
```

Or in spec file:
```python
exe = EXE(
    ...,
    icon='app.ico',
)
```

### Version Information

Create `version.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    productvers=(1, 0, 0, 0),
    mask=0x3f,
    filetype=0x0,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'00000000', uFileVersion, u'1.0.0.0'),
        StringStruct(u'00000000', uFileDescription, uCampus Portal Autologin'),
        StringStruct(u'00000000', uProductName, uCampus Portal Autologin),
        String[Struct](u'00000000', uCompanyName, u''),
      ])
    ),
    VarFileInfo([VarStruct(u'Translation', langid=1033, charset=1200)])
  ]
)
```

## CI/CD Integration

GitHub Actions workflow is already configured in `.github/workflows/build-windows.yml`.

This workflow:
- Triggers on push to main, tags, and PRs
- Builds Windows executable
- Uploads as artifact
- Creates release for tags
- Can be manually triggered via workflow_dispatch
