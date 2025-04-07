from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    model_config = SettingsConfigDict(env_file=PROJECT_DIR / 'example.env')

    debug: bool = False
    directory: str = './'
    db_name: str = 'db'
    db_user: str = 'user'
    db_password: str = 'password'
    db_host: str = 'localhost'
    db_port: str = '5432'
    sqlite: bool = True

    @property
    def db_url(self) -> str:
        if self.sqlite:
            return 'sqlite+aiosqlite:///../db.sqlite3'
        return (
            f'postgresql+asyncpg://{self.db_user}:{self.db_password}@'
            f'{self.db_host}:{self.db_port}/{self.db_name}'
        )


settings = Settings()
