import logging

logging.basicConfig(level=logging.INFO)

# Using uvicorn logger, I like its format, and its coloured output
log = logging.getLogger("uvicorn.error")
