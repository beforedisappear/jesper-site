blog / informational portal [Django]

<p>features:</p>
<p>• public profile</p>
<p>• ajax registration form</p>
<p>• ajax authentification form</p>
<p>• tree-like comment system (model + forms)</p>


Create a `.env` file in the root of your project:

```
DJANGO_KEY = 'SECRET_KEY'
SAGOK = 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'
SAGOS = 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'
SATBT = 'SOCIAL_AUTH_TELEGRAM_BOT_TOKEN'
HOST = EMAIL_HOST         
HOST_USER = EMAIL_HOST_USER
HOST_PASSWORD = EMAIL_HOST_PASSWORD
PORT = EMAIL_PORT 
USE_TLS = EMAIL_USE_TLS
```