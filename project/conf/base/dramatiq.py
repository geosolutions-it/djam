import os

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": f"amqp://{os.getenv('DJAM_RABBITMQ_HOST', 'localhost')}:{os.getenv('DJAM_RABBITMQ_PORT', '5672')}",
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ],
}

# Defines which database should be used to persist Task objects when the
# AdminMiddleware is enabled.  The default value is "default".
DRAMATIQ_TASKS_DATABASE = "default"
