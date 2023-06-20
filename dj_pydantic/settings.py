import os
import pathlib
from pathlib import Path
from typing import Dict, List

from pydantic import BaseSettings, Field
from pydantic.fields import Undefined
from pydjantic import BaseDBConfig, to_django


def make_dir(directory: str) -> str:
    """

    :rtype: object
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


# Build paths inside the project like this: BASE_DIR / 'subdir'.
CUR_DIR = Path(__file__).resolve().parent
BASE_DIR: Path = CUR_DIR.parent
DATA_DIR = make_dir(BASE_DIR.joinpath("data"))


class DatabaseSettings(BaseDBConfig):
    # https://docs.djangoproject.com/en/3.1/ref/settings/#databases
    default: str = Field(
        default=str(f"sqlite:///{DATA_DIR}/djpydantic.sqlite3"),
        env="DATABASE_URL",
        conn_max_age=0,
        ssl_require=False,
    )

    class Config:
        env_file = CUR_DIR / ".env"


class GeneralSettings(BaseSettings):
    # https://docs.djangoproject.com/en/dev/ref/settings/
    SECRET_KEY: str = Field(default=Undefined, env="DJANGO_SECRET_KEY")
    DEBUG: bool = Field(default=False, env="DEBUG")
    DATABASES: DatabaseSettings = DatabaseSettings()

    ALLOWED_HOSTS: List[str] = ["127.0.0.1", "localhost"]
    ROOT_URLCONF: str = "dj_pydantic.urls"
    WSGI_APPLICATION: str = "dj_pydantic.wsgi.application"

    INSTALLED_APPS: List[str] = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    MIDDLEWARE: List[str] = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    AUTH_PASSWORD_VALIDATORS: List[Dict] = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]


class I18NSettings(BaseSettings):
    # https://docs.djangoproject.com/en/3.1/topics/i18n/
    LANGUAGE_CODE: str = "en-us"
    TIME_ZONE: str = "UTC"
    USE_I18N: bool = True
    USE_L10N: bool = True
    USE_TZ: bool = True


class TransactionSettings(BaseSettings):
    LOG_DIR = make_dir(DATA_DIR.joinpath("logs"))

    MEDIA_DIR = make_dir(DATA_DIR.joinpath("uploads"))
    MEDIA_URL = "/uploads/"
    MEDIA_ROOT = DATA_DIR / "uploads"


class StaticSettings(BaseSettings):
    # https://docs.djangoproject.com/en/3.1/howto/static-files/
    STATIC_URL: str = "/static/"
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
    TEMPLATES: List[Dict] = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]


class ProjectSettings(
    GeneralSettings, I18NSettings, TransactionSettings, StaticSettings
):
    class Config:
        env_file = CUR_DIR / ".env"


to_django(ProjectSettings())
