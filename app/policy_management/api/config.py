from pathlib import Path
import os


class Settings:
    app_name: str = "TMHCC Policy Management"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./policies.db")

    current_dir: Path = Path(__file__).parent
    static_dir: Path = current_dir / "static"
    templates_dir: Path = current_dir / "templates"


def get_settings() -> Settings:
    return Settings()
