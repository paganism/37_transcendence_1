import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://cfcda0ab3c1b4fc9bdc7a3dd139e75ac@sentry.io/1305643",
    integrations=[DjangoIntegration()]
)

