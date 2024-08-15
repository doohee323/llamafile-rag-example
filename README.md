# tz-llmafile-rag

```
# Rag test 
1. upload a test input data file
curl -F "file=@/Users/dhong/Downloads/11.txt" -F "filename=11.txt" http://localhost:8000/api/upload

or http://localhost:8080/upload 

2. reload index
curl -d '{"filename":"11.txt"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/load
curl -X POST http://localhost:8000/api/reload
3. query
curl -d '{"query":"홍두희는 무엇을 좋아하나? 한국어로 답해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
curl -d '{"query":"소다기프트는 어떤 서비스인가? 한국어로 답해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
curl -d '{"query":"소다기프트 결제 방법 선택 옵션은 무엇이 있나? 한국어로 답해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
curl -d '{"query":"소다기프트를 위해서 페이팔을 쓸 수 있나? 한국어로 답해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
curl -d '{"query":"소다기프트를 위해서 벤모를 쓸 수 있나? 한국어로 답해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
curl -d '{"query":"소다기프트의 가능한 결제 방법 선택 옵션 목록을 보여줘? 한국어로 답해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
curl -X GET http://localhost:8000/api/query?query=What%20does%20Daniel%20like

sudo apt install intel-gpu-tools
sudo intel_gpu_top

```

```
# run Vue alone
    cd statics
    npm i
    npm run build
    npm run serve

open http://localhost:8080 or 
open http://localhost:8081
```

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```


