
from prometheus_client import Enum


class SubscriptionTypeEnum(Enum):
    INDIVIDUAL = 'INDIVIDUAL'
    COMPANY = 'COMPANY'