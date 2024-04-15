
import app

def main():
    # NOTE: Only for debugging; use uvicorn for production
    #       (e.g. uvicorn app:api --reload)
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
