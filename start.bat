@echo off
chcp 65001 >nul
echo 🚀 启动概率论与数理统计备考Agent...

:: 启动后端
cd backend
call study_venv\Scripts\activate
start "Backend" cmd /k "python main.py"

:: 等待后端启动
timeout /t 5 /nobreak >nul

:: 启动前端
cd ..\frontend
start "Frontend" cmd /k "npm run dev"

echo.
echo ✅ 服务已启动！
echo 📱 前端: http://localhost:5173
echo 🔧 后端: http://localhost:8000
echo 📚 API文档: http://localhost:8000/docs
echo.
pause