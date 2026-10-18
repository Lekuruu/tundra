
from argparse import ArgumentParser
from collections.abc import Sequence

import logging
import config

logging.basicConfig(
    format='[%(asctime)s] - <%(name)s> %(levelname)s: %(message)s',
    level=logging.DEBUG if config.DEBUG else logging.INFO,
)

def run_api() -> None:
    import uvicorn

    uvicorn.run(
        'app.api:api',
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        reload=config.RELOAD,
        ssl_keyfile=config.SSL_KEY_PATH if config.SSL_ENABLED else None,
        ssl_certfile=config.SSL_CERT_PATH if config.SSL_ENABLED else None,
        server_header=False,
        log_config=None,
    )

def run_world() -> None:
    from app.world_server import create_world_server
    create_world_server().run()

def main(arguments: Sequence[str] | None = None) -> None:
    parser = ArgumentParser(
        description='Run a Tundra service'
    )
    parser.add_argument(
        'service',
        choices=('api', 'world'),
        default='api',
        nargs='?',
        help='service to run (default: api)',
    )
    service = parser.parse_args(arguments).service

    if service == 'world':
        run_world()
        return

    run_api()

if __name__ == '__main__':
    main()
