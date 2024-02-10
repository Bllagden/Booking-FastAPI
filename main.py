import dotenv
import uvicorn

if __name__ == "__main__":
    dotenv.load_dotenv(".env.dev")
    uvicorn.run("app:create_app", factory=True, reload=True)
