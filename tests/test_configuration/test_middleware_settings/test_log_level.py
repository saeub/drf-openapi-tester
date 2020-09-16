# noqa: TYP001
import pytest
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured

from django_swagger_tester.configuration import SwaggerTesterSettings
from tests.utils import patch_middleware_settings, patch_settings


def test_non_string_log_level(monkeypatch) -> None:
    """
    LOG_LEVEL must be a string.
    """
    for value in [None, {}, [], 2]:
        with pytest.raises(
            ImproperlyConfigured, match='The SWAGGER_TESTER middleware setting `LOG_LEVEL` must be a string value'
        ):
            monkeypatch.setattr(django_settings, 'SWAGGER_TESTER', patch_middleware_settings('LOG_LEVEL', value))
            SwaggerTesterSettings()


def test_bad_log_level_name(monkeypatch) -> None:
    for value in ['test', '']:
        with pytest.raises(
            ImproperlyConfigured,
            match='is not a valid log level. Please change the `LOG_LEVEL` '
            'setting in your `SWAGGER_TESTER` settings to one of `DEBUG`, `INFO`, '
            '`WARNING`, `ERROR`, `EXCEPTION`, or `CRITICAL`',
        ):
            monkeypatch.setattr(django_settings, 'SWAGGER_TESTER', patch_middleware_settings('LOG_LEVEL', value))
            SwaggerTesterSettings()


def test_valid_log_level_names(monkeypatch) -> None:
    """
    Make sure we accept all valid log levels, regardless of casing.
    """
    for value in ['debug', 'info', 'warning', 'error', 'critical', 'exception']:
        for method in [str.lower, str.upper]:
            monkeypatch.setattr(django_settings, 'SWAGGER_TESTER', patch_middleware_settings('LOG_LEVEL', method(value)))
            SwaggerTesterSettings()