__version__ = '0.0.2'

import logging
from .tester import OpenAPITester

logger = logging.getLogger('openapi-tester')

validate_schema = OpenAPITester().validate_schema
