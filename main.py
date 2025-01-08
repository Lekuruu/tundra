

import uvicorn
import config

def main():
    # NOTE: Only for debugging; use a wsgi for production
    #       (e.g. uvicorn app:api)
    uvicorn.run(
        "app:api",
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        reload=config.RELOAD,
        server_header=False,
        log_config=None,
    )

if __name__ == "__main__":
    main()
