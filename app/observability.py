from __future__ import annotations

import atexit
import logging

from dotenv import load_dotenv

load_dotenv()

from langfuse import Langfuse  # noqa: E402

logger = logging.getLogger(__name__)

langfuse = Langfuse()

atexit.register(langfuse.flush)

logger.info("Langfuse observability initialized")
