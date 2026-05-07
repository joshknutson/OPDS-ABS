"""OPDS Feed for Audiobookshelf - Entry Point.

This script serves as the entry point for the OPDS-ABS application.
It configures and starts the uvicorn ASGI server with appropriate settings
based on the configured log level.

The server runs on all network interfaces (0.0.0.0) on port 8000 with
hot reload enabled for development convenience.
"""
import os
import socket
import uvicorn
import logging
from opds_abs.config import (
    LOG_LEVEL,
    AUDIOBOOKSHELF_INTERNAL_URL,
    AUDIOBOOKSHELF_EXTERNAL_URL,
    AUDIOBOOKSHELF_API
)

# Set up logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger("opds_abs")

if __name__ == "__main__":
    # Log URL configurations
    logger.info("-" * 50)
    logger.info("Starting OPDS-ABS server with the following configuration:")
    logger.info(f"AUDIOBOOKSHELF_INTERNAL_URL: {AUDIOBOOKSHELF_INTERNAL_URL}")
    logger.info(f"AUDIOBOOKSHELF_EXTERNAL_URL: {AUDIOBOOKSHELF_EXTERNAL_URL}")
    logger.info(f"AUDIOBOOKSHELF_API: {AUDIOBOOKSHELF_API}")
    logger.info("-" * 50)

    # Allow configuring host/port via environment variables.
    # If the desired port is unavailable, fall back to the next one.
    host = os.getenv("HOST", "0.0.0.0")
    base_port = int(os.getenv("PORT", "8000"))
    log_level = LOG_LEVEL.lower()

    def port_is_available(host: str, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
                return True
            except OSError:
                return False

    for port in range(base_port, base_port + 5):
        if not port_is_available(host, port):
            logger.warning("Port %s:%s is unavailable; trying next port...", host, port)
            continue

        uvicorn.run(
            "opds_abs.main:app",
            host=host,
            port=port,
            reload=True,
            proxy_headers=True,
            forwarded_allow_ips="*",
            log_level=log_level,
            use_colors=True,
        )
        break
    else:
        logger.error("Could not start server: no available ports between %s and %s.", base_port, base_port + 4) 
