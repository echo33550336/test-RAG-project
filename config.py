# AI工具使用标注（2026大赛要求）
# 1. DeepSeek：立项、方向确认、分工优化
# 2. 豆包：方案整理、规范文档
# 3. Kimi K2.5：代码生成、Debug、优化
# 4. Trae：前端UI样式微调
# AI仅辅助开发，核心设计与整合均为团队原创

import os
from datetime import datetime

try:
    import dotenv

    _cfg_root = os.path.dirname(os.path.abspath(__file__))
    dotenv.load_dotenv(os.path.join(_cfg_root, ".env"))
except ImportError:
    pass

class ProjectConfig:
    """项目统一配置"""
    
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    
    DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
    RAW_DATA_DIR = os.path.join(DATA_DIR, "Raw-Data")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "Processed-Data")
    CHROMA_DB_DIR = os.path.join(DATA_DIR, "Chroma_db")
    # 管理端上传的原始知识库文件（向量在 Chroma，图谱在 SQLite；此处只存盘 + 元数据在 SQL）
    KNOWLEDGE_UPLOADS_DIR = os.path.join(DATA_DIR, "Knowledge-Uploads")
    KNOWLEDGE_ARCHIVE_FILES = os.getenv("KNOWLEDGE_ARCHIVE_FILES", "true").lower() == "true"
    
    BACKEND_DIR = os.path.join(PROJECT_ROOT, "Backend")
    
    MODELS_DIR = os.path.join(BACKEND_DIR, "Models")
    LOCAL_EMBEDDING_MODEL_DIR = os.path.join(MODELS_DIR, "embedding", "bge-small-zh-v1.5")
    EMBEDDING_CACHE_DIR = os.path.join(MODELS_DIR, "embedding", ".cache")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-small-zh-v1.5")
    EMBEDDING_HF_ENDPOINT = os.getenv("EMBEDDING_HF_ENDPOINT", "https://hf-mirror.com").strip()
    EMBEDDING_REMOTE_DOWNLOAD_ENABLED = os.getenv("EMBEDDING_REMOTE_DOWNLOAD_ENABLED", "true").lower() in ("1", "true", "yes")
    _EMBEDDING_MODEL_DIR_RAW = os.getenv("EMBEDDING_MODEL_DIR", "").strip()
    if _EMBEDDING_MODEL_DIR_RAW:
        EMBEDDING_MODEL_DIR = (
            _EMBEDDING_MODEL_DIR_RAW
            if os.path.isabs(_EMBEDDING_MODEL_DIR_RAW)
            else os.path.abspath(os.path.join(PROJECT_ROOT, _EMBEDDING_MODEL_DIR_RAW))
        )
    else:
        EMBEDDING_MODEL_DIR = LOCAL_EMBEDDING_MODEL_DIR
    # 全项目向量「存储维数」：SQL Server VECTOR(n)、Chroma 入库与查询补零目标（BGE-small 句向量 384 会尾部补 0）
    VECTOR_STORAGE_DIM = int(os.getenv("VECTOR_STORAGE_DIM", "512"))
    SQL_SERVER_VECTOR_DIM = int(os.getenv("SQL_SERVER_VECTOR_DIM", str(VECTOR_STORAGE_DIM)))
    EMBEDDING_VECTOR_DIM = int(os.getenv("EMBEDDING_VECTOR_DIM", str(VECTOR_STORAGE_DIM)))
    
    RAG_ENGINE_DIR = os.path.join(BACKEND_DIR, "rag")
    
    ENV_FILE_PATH = os.path.join(RAG_ENGINE_DIR, ".env")
    
    PORT = int(os.getenv("PORT", "5000"))
    
    DATABASE_URI = os.getenv("DATABASE_URI", "mysql+pymysql://root:password@localhost:3306/campus_qa")
    # mysql_graph: chunk+向量进关系库；chroma（默认）: 向量 Chroma + 图谱 Data/knowledge_graph.sqlite3，关系库仅存业务与上传元数据
    STORAGE_MODE = os.getenv("STORAGE_MODE", "chroma")
    # 知识库写入关系库后，同步节点/边到 campus_graph_*（与前端图谱 API 同源）
    KNOWLEDGE_GRAPH_SYNC = os.getenv("KNOWLEDGE_GRAPH_SYNC", "true").lower() == "true"
    # 向量检索命中后，按「同一文档源」在图谱上拉取相邻 chunk 作为补充上下文
    KNOWLEDGE_GRAPH_RAG_EXPAND = os.getenv("KNOWLEDGE_GRAPH_RAG_EXPAND", "true").lower() == "true"
    # STORAGE_MODE=chroma 时，入库文档是否同步写入 Data/knowledge_graph.sqlite3
    KNOWLEDGE_GRAPH_CHROMA_SYNC = os.getenv("KNOWLEDGE_GRAPH_CHROMA_SYNC", "true").lower() == "true"
    # 将图谱命中的实体名并入 embedding 输入，增强向量检索（问句触发/过滤仍用用户原话）
    ENTITY_QUERY_AUGMENT = os.getenv("ENTITY_QUERY_AUGMENT", "true").lower() == "true"

    # 管理后台敏感写操作（改模型、改权限、删用户、知识库清空等）需额外校验「二级密码」
    # 仅支持：ADMIN_SECONDARY_PASSWORD_HASH（PBKDF2；可用 Backend.infrastructure.auth.hash_password 生成）
    ADMIN_SECONDARY_PASSWORD_HASH = os.getenv("ADMIN_SECONDARY_PASSWORD_HASH", "").strip()

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_to_a_secure_random_key_at_least_32_bytes_long")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 1800))  # Access Token 30分钟
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 604800))  # Refresh Token 7天
    
    LOGIN_MAX_FAILURES = 5  # 最大连续失败次数
    LOGIN_FAILURE_LOCKOUT = 1800  # 锁定时间（秒），默认30分钟
    MAX_CONCURRENT_SESSIONS = 3  # 最大并发会话数（多地登录控制）
    
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "hunyuan")  # hunyuan | auto
    HUNYUAN_API_KEY = os.getenv("HUNYUAN_API_KEY", "")
    HUNYUAN_API_BASE = os.getenv("HUNYUAN_API_BASE", "https://tokenhub.tencentmaas.com/v1")
    HUNYUAN_MODEL = os.getenv("HUNYUAN_MODEL", "")
    
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM = os.getenv("SMTP_FROM", "noreply@campus.edu")
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    
    VERIFICATION_CODE_EXPIRES = 300  # 验证码有效期（秒），默认5分钟
    VERIFICATION_CODE_LENGTH = 6  # 验证码长度
    
    VECTOR_SEARCH_CONFIG = {
        "k": int(os.getenv("RAG_VECTOR_TOP_K", "2"))
    }
    
    @classmethod
    def init_directories(cls):
        """初始化项目目录"""
        directories = [
            cls.DATA_DIR,
            cls.RAW_DATA_DIR,
            cls.PROCESSED_DATA_DIR,
            cls.CHROMA_DB_DIR,
            cls.KNOWLEDGE_UPLOADS_DIR,
            cls.BACKEND_DIR,
            cls.MODELS_DIR,
            cls.RAG_ENGINE_DIR,
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

ProjectConfig.init_directories()