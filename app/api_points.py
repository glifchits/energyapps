import secret_config as secret

URL_BASE = 'https://greenbutton.affsys.com'
API_BASE = '%s/ldc/api/v1' % URL_BASE

SERVICE_STATUS = '%s/ReadServiceStatus' % API_BASE
AUTH_STATUS = '%s/ReadAuthorizationStatus' % API_BASE
GET_EUI = '%s/UsagePoint' % API_BASE
CREATE_SUBSCRIPTION = '%s/Subscription' % API_BASE

AUTH_URL = \
"https://greenbutton.affsys.com/auth/signin.jsp?client_id={0}&redirect_uri={1}&state=0%2Fa7fcb34d-271f-4910-a886-2ad617021cfe"\
.format(secret.CLIENT_ID, secret.REDIRECT_URI)

TOKEN_URL = '%s/auth/j_oauth_resolve_access_code' % URL_BASE
