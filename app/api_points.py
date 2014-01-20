import secret_config as secret
from config import exported as config

#URL_BASE = 'https://greenbutton.affsys.com'
URL_BASE = 'https://greenbutton.powerinform.com'
API_BASE = '%s/ldc/api/v1' % URL_BASE

SERVICE_STATUS = '%s/ReadServiceStatus' % API_BASE
AUTH_STATUS = '%s/ReadAuthorizationStatus' % API_BASE
GET_EUI = '%s/UsagePoint' % API_BASE
CREATE_SUBSCRIPTION = '%s/Subscription' % API_BASE

AUTH_URL = \
"{0}/auth/signin.jsp?client_id={1}&redirect_uri={2}&state=0%2Fa7fcb34d-271f-4910-a886-2ad617021cfe"\
.format(URL_BASE, secret.CLIENT_ID, config.REDIRECT_URI)

TOKEN_URL = '%s/auth/j_oauth_resolve_access_code' % URL_BASE
