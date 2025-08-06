from app.api import app 

if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT, DEBUG_MODE

    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=DEBUG_MODE)
 