from ai_driver.retrieval.qa import QADBConfig
from ai_driver.config import server_config


def get_default_qa_config():
    config = QADBConfig(
        db_path=server_config.DB_PATH,
        embed_model=server_config.CHAT_EMBED_MODEL,
        return_source=server_config.RETURN_SOURCE_DOCUMENTS,
        vector_count=server_config.VECTOR_COUNT,
    )
    return config
