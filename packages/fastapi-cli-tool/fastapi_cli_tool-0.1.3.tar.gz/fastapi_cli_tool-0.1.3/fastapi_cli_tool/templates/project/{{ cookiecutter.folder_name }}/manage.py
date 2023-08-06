import argparse

import uvicorn
from backend.settings import settings


def run(app: str, port: int, reload: bool):
    uvicorn.run(app, port=port, reload=reload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the server")
    parser.add_argument(
        "--port", type=int, default=3000, help="Port number to run the server on"
    )
    parser.add_argument(
        "--reload",
        default=settings.DEBUG,
        action="store_true",
        help="Reload the server on file changes",
    )
    args = parser.parse_args()

    run("core.app:app", port=args.port, reload=args.reload)
