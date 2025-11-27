# Activate virtual environment and run Flask app
.\tfenv\Scripts\Activate.ps1
Write-Host "`n🚀 Starting Flask App Locally`n" -ForegroundColor Cyan
Write-Host "The app will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow
python app.py
