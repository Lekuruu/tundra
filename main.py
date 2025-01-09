

import uvicorn
import config

def run_ssl():
    uvicorn.run(
        "app:api",
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        reload=config.RELOAD,
        ssl_keyfile=config.SSL_KEY_PATH,
        ssl_certfile=config.SSL_CERT_PATH,
        server_header=False,
        log_config=None,
    )

def run():
    if config.SSL_ENABLED:
        return run_ssl()

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
    run()
