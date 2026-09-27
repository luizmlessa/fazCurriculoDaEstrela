"""Configurações globais do projeto, carregadas de variáveis de ambiente."""
import os


class Config:
    """Centraliza configurações externalizadas.

    Segue o princípio de inversão de dependência: os valores não ficam
    hardcoded nas classes que os utilizam.
    """

    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")
    DATA_DIR: str = os.getenv("DATA_DIR", "data")