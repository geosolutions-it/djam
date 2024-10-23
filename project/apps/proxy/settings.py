import ast
import os

SHOW_UPSTREAM_SERVICES_IN_DASHBOARD = ast.literal_eval(os.getenv("SHOW_UPSTREAM_SERVICES_IN_DASHBOARD", "False"))