echo "🐳 Docker 컨테이너를 빌드 및 실행 중..."
docker-compose up --build -d

echo "⏳ 서버가 준비될 때까지 잠시 기다리는 중..."
sleep 10

# macOS에서는 open, 리눅스에서는 xdg-open 사용
if [[ "$OSTYPE" == "darwin"* ]]; then
  open "http://localhost:8000"
else
  xdg-open "http://localhost:8000"
fi

echo "🚀 FastAPI 서버가 실행되었습니다! (http://localhost:8000)"
