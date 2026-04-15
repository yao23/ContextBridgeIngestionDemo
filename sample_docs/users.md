# Users API

## Get User
GET /v1/users/{id}

Requires Bearer authentication.

- id: user identifier path parameter
- expand: optional field expansion query parameter

```
curl /v1/users/123 \
  -H "Authorization: Bearer <token>"
```
