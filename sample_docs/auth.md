# Auth API

## Create Token
POST /v1/token

Requires Bearer authentication.

- client_id: OAuth client identifier
- client_secret: OAuth client secret

```
curl -X POST /v1/token \
  -H "Authorization: Bearer <admin-token>" \
  -d "client_id=demo-app" \
  -d "client_secret=super-secret"
```
