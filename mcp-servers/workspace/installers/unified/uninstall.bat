@echo off
REM Safe Uninstaller for MCP Federation Core (Windows)
REM Default: Selective removal - preserves user MCPs

echo ====================================================================
echo MCP Federation Core - Safe Uninstaller
echo ====================================================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ to continue
    pause
    exit /b 1
)

REM Check for command-line arguments
if "%1"=="" goto interactive

REM Handle specific modes
if /i "%1"=="selective" (
    echo Running SELECTIVE uninstall - Federation components only...
    python "%~dp0uninstall.py" --mode selective %2 %3 %4
    goto end
)

if /i "%1"=="complete" (
    echo WARNING: Complete uninstall will remove ALL MCPs!
    python "%~dp0uninstall.py" --mode complete %2 %3 %4
    goto end
)

if /i "%1"=="restore" (
    echo Restoring from backup...
    python "%~dp0uninstall.py" --mode restore %2 %3 %4
    goto end
)

if /i "%1"=="dry-run" (
    echo Running dry-run (no changes will be made)...
    python "%~dp0uninstall.py" --mode dry-run %2 %3 %4
    goto end
)

if /i "%1"=="help" goto showhelp
if /i "%1"=="-h" goto showhelp
if /i "%1"=="--help" goto showhelp
if /i "%1"=="/?" goto showhelp

echo Unknown mode: %1
goto showhelp

:interactive
REM Run interactive mode
python "%~dp0uninstall.py"
goto end

:showhelp
echo.
echo Usage: uninstall.bat [mode] [options]
echo.
echo Modes:
echo   selective   Remove Federation MCPs only (default, recommended)
echo   complete    Remove ALL MCPs (use with caution!)
echo   restore     Restore from backup
echo   dry-run     Show what would be removed without making changes
echo   help        Show this help message
echo.
echo Options:
echo   --mcp-base PATH    Path to mcp_base directory
echo   --backup-dir PATH  Specific backup to restore
echo   --force           Skip confirmation prompts
echo.
echo Examples:
echo   uninstall.bat                    (interactive mode)
echo   uninstall.bat selective          (remove Federation only)
echo   uninstall.bat complete --force   (remove everything, no prompts)
echo   uninstall.bat restore            (restore from backup)
echo   uninstall.bat dry-run           (preview changes)
echo.

:end
pause