from apps.billing.settings import (
    ACCEPTED_PERMISSIONS_FOR_INDIVIDUALS_SUB,
    ACCEPTED_PERMISSIONS_FOR_COMPANY_SUB,
)
from prometheus_client import Enum


class SubscriptionTypeEnum(Enum):
    INDIVIDUAL = "INDIVIDUAL"
    COMPANY = "COMPANY"


class SubscriptionPermissions(Enum):
    FREE = "FREE"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"
    ALL = ["FREE", "PRO", "ENTERPRISE"]
    INDIVIDUAL = ACCEPTED_PERMISSIONS_FOR_INDIVIDUALS_SUB
    COMPANY = ACCEPTED_PERMISSIONS_FOR_COMPANY_SUB
