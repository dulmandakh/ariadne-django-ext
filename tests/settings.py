SECRET_KEY = "SECRET_KEY"
INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test",
    }
}
USE_TZ = True
