#!/usr/bin/env python3
import argparse
import asyncio
import logging
from functools import partial
from pathlib import Path
from typing import Optional

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
        required=True,
        help="URL of whisper.cpp to use, http:// or https://",
    )
    parser.add_argument("--uri", required=True, help="unix:// or tcp://")
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    parser.add_argument(
        "--log-format", default=logging.BASIC_FORMAT, help="Format for log messages"
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
