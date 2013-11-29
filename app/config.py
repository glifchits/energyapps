import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

BASE_URL = 'http://localhost:5000'
REDIRECT_URI = '{0}/auth'.format(BASE_URL)

CLIENT_ID = 'id-a3a5e887-9717-46df-b2f1-7a33ed9da42b'
CLIENT_SECRET = 'secret-9e586bf6-dd1f-4ea3-9a63-afec930fdad5'

AUTH_URL = 'https://greenbutton.affsys.com/auth/signin.jsp?client_id={0}&redirect_uri={1}&state=0%2F75ad7ebc-ccc0-4efd-9e49-f327b0060c7f'.format(CLIENT_ID, REDIRECT_URI)
TOKEN_URL = 'https://greenbutton.affsys.com/auth/j_oauth_resolve_access_code'
