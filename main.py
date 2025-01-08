

import uvicorn
import config

def main():
    # NOTE: Only for debugging; use a wsgi for production
    #       (e.g. uvicorn app:api)
    uvicorn.run(
        "app:api",
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        server_header=False,
        log_config=None,
        reload=True
    )

if __name__ == "__main__":
    main()
