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
curl -X GET http://localhost:8000/api/query?query=What%20does%20Daniel%20like

curl -d '{"query":"홍두희는 무엇을 좋아하나? 한국어로 답해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
curl -d '{"query":"ArogoCD는 왜 쓰는 거지? 한국어로 답해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query
curl -d '{"query":"GitOps on K8S을 한국어로 설명해줘"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query

curl -d '{"query":"홍두희는 무엇을 좋아하나? 한국어로 답해줘?"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query

4. append tmp index
cp uploads/1.txt tmp_data/1.txt
curl -X POST http://localhost:8000/api/tmpidx
curl -d '{"query":"홍두희는 무엇을 좋아하나? 한국어로 답해줘?"}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/query

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


