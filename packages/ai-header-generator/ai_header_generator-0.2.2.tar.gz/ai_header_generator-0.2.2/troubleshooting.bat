@echo off

REM Check for Python
python --version >nul 2>&1 || (echo Python not found && exit /b 1)

REM Check for ai-header-generator module
python -c "import ai_header_generator" >nul 2>&1 || (echo ai_header_generator module not found && exit /b 1)

REM Check for config.ini file
if not exist config.ini (echo config.ini file not found && exit /b 1)

REM Check for template file
if not exist template.json (echo template.json file not found && exit /b 1)

REM Generate headers
python -m ai_header_generator.cli --config config.ini --template-file template.json || (echo Header generation failed && exit /b 1)

REM Check for README.md file
if not exist README.md (echo README.md file not found && exit /b 1)

echo All recommendations passed
exit /b 0