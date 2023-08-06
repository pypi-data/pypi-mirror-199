import os

userId = os.environ.get('SP_USER_ID')
appId = os.environ.get('SP_APP_ID')
nodeId = None

# Api
accessSecret = os.environ.get('SP_ACCESS_SECRET')
userIdHeaderField = os.environ.get('SP_USER_ID_HEADER_FIELD', 'x-sp-user-id')
userSignatureHeaderField = os.environ.get('SP_USER_SIGNATURE_HEADER_FIELD', 'x-sp-signature')
userSignVersionHeaderField = os.environ.get('SP_USER_SIGN_VERSION_HEADER_FIELD', 'x-sp-sign-version')

# Logkit
logkitUri = os.environ.get('SP_LOGKIT_URI', '')
logkitNamespace = os.environ.get('SP_LOGKIT_NAMESPACE', '/logkit')
logkitPath = os.environ.get('SP_LOGKIT_PATH', '')
logkitEventsAppend = os.environ.get('SP_LOGKIT_EVENTS_APPEND', 'append')
logkitLogsLevel = os.environ.get('SP_LOGKIT_LOGS_LEVEL', 'warning')
