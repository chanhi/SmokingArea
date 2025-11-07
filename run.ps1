docker-compose up --build -d
Write-Output "⏳ Waiting..."
Start-Sleep -Seconds 10
Start-Process "http://localhost:8000"
Write-Output "🚀 FastAPI Sever is running!(http://localhost:8000)"