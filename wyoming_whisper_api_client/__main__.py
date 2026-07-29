#!/usr/bin/env python3
import argparse
import asyncio
import logging
import os
from functools import partial
from wyoming.info import AsrModel, AsrProgram, Attribution, Info
from wyoming.server import AsyncServer

from . import __version__
from .const import WHISPER_LANGUAGES
from .handler import WhisperAPIEventHandler

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api",
        default=os.getenv("WHISPER_API") or None,
        required=not os.getenv("WHISPER_API"),
        help="URL of whisper.cpp to use, http:// or https:// "
            "(env: WHISPER_API)",
    )

    parser.add_argument(
        "--uri",
        default=os.getenv("WYOMING_URI") or None,
        required=not os.getenv("WYOMING_URI"),
        help="unix:// or tcp:// (env: WYOMING_URI)",
    )

    parser.add_argument(
        "--model",
        default=os.getenv("WHISPER_MODEL"),
        help="Model name to use for transcription "
            "(sent as 'model' param to API) "
            "(env: WHISPER_MODEL)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.getenv("DEBUG", "").lower() in ("1", "true", "yes", "on"),
        help="Log DEBUG messages (env: DEBUG)",
    )

    parser.add_argument(
        "--log-format",
        default=os.getenv("LOG_FORMAT", logging.BASIC_FORMAT),
        help="Format for log messages (env: LOG_FORMAT)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print version and exit",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO, format=args.log_format
    )
    _LOGGER.debug(args)

    wyoming_info = Info(
        asr=[
            AsrProgram(
                name="whisper-cpp",
                description="Faster Whisper transcription via its API",
                attribution=Attribution(
                    name="Michael Hansen",
                    url="https://github.com/synesthesiam"
                ),
                installed=True,
                version=__version__,
                models=[
                    AsrModel(
                        name="whisper.cpp",
                        description="whisper.cpp",
                        attribution=Attribution(
                            name="rhasspy wyoming faster whisper",
                            url="https://github.com/rhasspy/wyoming-faster-whisper"
                        ),
                        installed=True,
                        languages=WHISPER_LANGUAGES,
                        version="1.0",
                    )
                ],
            )
        ],
    )

    # Load converted whisper API

    server = AsyncServer.from_uri(args.uri)
    _LOGGER.info("Ready")
    model_lock = asyncio.Lock()
    await server.run(
        partial(
            WhisperAPIEventHandler,
            wyoming_info,
            args
        )
    )


# -----------------------------------------------------------------------------


def run() -> None:
    asyncio.run(main(), debug=True)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
