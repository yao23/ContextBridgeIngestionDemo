# Auth API

## Create Token
POST /v1/token

Requires Bearer authentication.

- client_id: OAuth client identifier
- client_secret: OAuth client secret

Response fields:
- access_token: issued bearer token
- expires_in: token lifetime in seconds

Status codes:
- 200: token created
- 401: invalid admin token

```
curl -X POST /v1/token \
  -H "Authorization: Bearer <admin-token>" \
  -d "client_id=demo-app" \
  -d "client_secret=super-secret"
```
