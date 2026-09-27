"""Exceções customizadas do projeto."""


class ResumeAIError(Exception):
    """Exceção base do projeto."""
    pass


class ExtractionError(ResumeAIError):
    """Falha ao extrair dados de uma fonte (URL, PDF, TXT)."""
    pass


class LLMError(ResumeAIError):
    """Falha ao comunicar com o provedor de LLM."""
    pass


class LLMConnectionError(LLMError):
    """Não foi possível conectar ao provedor de LLM."""
    pass


class LLMModelError(LLMError):
    """Modelo não encontrado ou não pôde ser carregado (ex: falta de VRAM)."""
    pass


class LLMTimeoutError(LLMError):
    """Provedor demorou demais para responder."""
    pass


class ParserError(ResumeAIError):
    """Falha ao interpretar a resposta do LLM."""
    pass


class WriterError(ResumeAIError):
    """Falha ao escrever o output (PDF, etc)."""
    pass