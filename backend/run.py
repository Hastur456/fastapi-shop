import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
    
    # Теперь обращайтесь:
    # - С этого ПК:      http://localhost:8000
    # - С другого ПК:    http://192.168.1.100:8000  (замените на реальный IP)
    