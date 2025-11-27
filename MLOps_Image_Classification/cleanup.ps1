# Project Cleanup Script
# Removes unnecessary documentation and test files before final submission

Write-Host "`n=== MLOps Project Cleanup ===" -ForegroundColor Cyan
Write-Host "This will remove temporary and redundant files`n" -ForegroundColor Yellow

# Files to delete (temporary, redundant docs, test scripts)
$filesToDelete = @(
    # Temporary test files
    "test_fixes.py",
    "test_fixes_without_tf.py",
    "test_integration.py",
    "test_deployment.py",
    "mock_tensorflow.py",
    "run_app_with_mock.py",
    
    # Redundant documentation (keep only essential)
    "ANSWER_ENV_VARIABLES.md",
    "ASSIGNMENT_REQUIREMENTS_CHECKLIST.md",
    "COMPLETE_ANALYSIS.md",
    "COMPLETE_SUMMARY.md",
    "DEPLOY_NOW.md",
    "DEPLOYMENT_MASTER_GUIDE.md",
    "DOCUMENTATION_INDEX.md",
    "ENVIRONMENT_VARIABLES_GUIDE.md",
    "ENVIRONMENT_VARIABLES_INDEX.md",
    "FINAL_ACTION_PLAN.md",
    "FINAL_STATUS_REPORT.md",
    "FINAL_SUMMARY.txt",
    "FIXES_APPLIED.md",
    "HOW_TO_VERIFY_PROJECT_WORKS.md",
    "IMPROVEMENTS.md",
    "PRE_DEPLOYMENT_TESTING.md",
    "PROJECT_ANALYSIS.md",
    "QUICKSTART.md",
    "RENDER_DEPLOYMENT_GUIDE.md",
    "RENDER_ENV_QUICK_REFERENCE.md",
    "RENDER_ENV_SETUP_VISUAL.md",
    "RENDER_EXACT_ENV_VALUES.md",
    "RENDER_QUICK_START.md",
    "RENDER_VISUAL_GUIDE.md",
    "REQUIREMENTS_MAPPING.md",
    "START_HERE_DEPLOYMENT.md",
    "SUBMISSION_SUMMARY.md",
    "TENSORFLOW_WINDOWS_FIX.md",
    "VISUALIZATION_GUIDE.md",
    "WHATS_LEFT_TODO.md"
)

$deletedCount = 0
$notFoundCount = 0

foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "* Deleted: $file" -ForegroundColor Green
        $deletedCount++
    } else {
        Write-Host "- Not found: $file" -ForegroundColor Gray
        $notFoundCount++
    }
}

Write-Host "`n=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files deleted: $deletedCount" -ForegroundColor Green
Write-Host "Files not found: $notFoundCount" -ForegroundColor Gray

Write-Host "`n=== Essential Files Kept ===" -ForegroundColor Cyan
Write-Host "* README.md (comprehensive project documentation)" -ForegroundColor White
Write-Host "* app.py (Flask API)" -ForegroundColor White
Write-Host "* config.py (configuration)" -ForegroundColor White
Write-Host "* requirements.txt (dependencies)" -ForegroundColor White
Write-Host "* Dockerfile & docker-compose.yml (deployment)" -ForegroundColor White
Write-Host "* nginx.conf (load balancer)" -ForegroundColor White
Write-Host "* locustfile.py (load testing)" -ForegroundColor White
Write-Host "* src/ (preprocessing, model, prediction)" -ForegroundColor White
Write-Host "* tests/ (unit tests)" -ForegroundColor White
Write-Host "* notebook/ (Jupyter notebook)" -ForegroundColor White
Write-Host "* models/ (trained models)" -ForegroundColor White
Write-Host "* results/ (load test results)" -ForegroundColor White
Write-Host "* templates/ (web UI)" -ForegroundColor White
Write-Host "* .env.example (configuration template)" -ForegroundColor White

Write-Host "`n=== Next Steps ===" -ForegroundColor Yellow
Write-Host "1. Review README.md - update YouTube link" -ForegroundColor White
Write-Host "2. Ensure notebook has all visualizations" -ForegroundColor White
Write-Host "3. Run: git add ." -ForegroundColor White
Write-Host "4. Run: git commit -m 'Final cleanup and documentation'" -ForegroundColor White
Write-Host "5. Run: git push origin main" -ForegroundColor White

Write-Host "`nCleanup complete!`n" -ForegroundColor Green
