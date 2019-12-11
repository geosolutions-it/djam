import os
from split_settings.tools import optional, include


PROJECT_ENVIRONMENT = os.getenv("DJAM_PROJECT_ENVIRONMENT", "prod")
include(
    'conf/common/*.py',
    optional(f'conf/{PROJECT_ENVIRONMENT}/*.py'),
)
