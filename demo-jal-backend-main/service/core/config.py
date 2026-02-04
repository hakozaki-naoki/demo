from typing import Dict, Any


class Settings:
    """Application settings."""

    provider: str = "openai"

    def dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {"provider": self.provider}


# Create a settings instance to be imported by other modules
settings = Settings()
