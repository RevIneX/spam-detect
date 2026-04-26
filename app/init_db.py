import logging
from app.db import engine
from app.models import Base

logger = logging.getLogger(__name__)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("[ OK ] psql tables")
    except Exception as e:
        logger.error(f"[ XX ] {e}")
        raise

if __name__ == "__main__":
    init_db()
