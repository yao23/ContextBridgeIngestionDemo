# Users API

## Get User
GET /v1/users/{id}

Requires Bearer authentication.

- id: user identifier path parameter
- expand: optional field expansion query parameter

Response fields:
- id: user id
- email: primary email address
- profile: expanded profile object

Status codes:
- 200: user returned
- 404: user not found

```
curl /v1/users/123 \
  -H "Authorization: Bearer <token>"
```
