# Users service


# Run Development

**RUN ONLY WITH DOCKER!!!**


1. Copy `cp envs/api.default.env envs/api.env` and fill environmental [variables](#apienv).
2. Copy `cp envs/postgres.default.env envs/postgres.env` and fill environmental [variables](#postgresenv).
3. Start containers in root directory `docker compose up --build`.
4. Does it work?
   
    **Go to:**
   - [localhost](http://localhost) to see frontend app
   - [django admin](http://localhost/admin/) to see Django Admin

For tests run:

```shell
  make pytest
```

To generate coverage report:
```shell
  make pytest-cov
```

To load some initial data:
**All users have the same password `TestPass123`, except django admin user, this one has password from this api.env variable `DJ_SU_PASSWORD`
```shell
  make loaddata
```

## Filling environmental variables

### api.env

> **DJ_SECRET_KEY=**

This is a secret key for Django. It is used to provide cryptographic signing, and should be set to a unique,
unpredictable value.
To generate a new secret key, run the following command inside django shell:

```python
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

Also, you can use this site: https://djecrety.ir/

e.g:
`DJ_SECRET_KEY="d_lam4k3w^-mj&tve4u3-nnuzqy9jlw^quw=4!rrw6r#55zq(="`

> **DJ_DEBUG=**

An integer that specifies the debug mode.
If 1, Django will use technical error responses when an exception occurs.
If 0, Django will display a standard page for the given exception, provided by the handler for that exception.

e.g:
`DJ_DEBUG=1`

> **DJ_ALLOWED_HOSTS=**

A list of strings representing the host/domain names that this Django site can serve.
This is a security measure to prevent an attacker from poisoning caches and password reset emails with links to
malicious hosts by submitting requests with a fake HTTP Host header, which is possible even under many seemingly-safe
web server configurations.

e.g:
**!!! Only for development**

`DJ_ALLOWED_HOSTS = '0.0.0.0 localhost 127.0.0.1'`

Hint: Multiple hosts should be separated by a space.

> **Variables used for Django superuser migration**

E.g.
```dotenv
DJ_SU_NAME=lordOfDarkness
DJ_SU_EMAIL=lordofdarkness@gmail.com
DJ_SU_PASSWORD=strongPassword123
```

### postgres.env

> POSTGRES_USER=

The username for the database.
e.g.
`POSTGRES_USER=custom_username`

> POSTGRES_PASSWORD=

The password for the database.
e.g:
`POSTGRES_PASSWORD=strong_password`

> POSTGRES_DB=

The name of the database.

e.g:`POSTGRES_DB=fancy_name`

> POSTGRES_HOST=

The host name of the database.
If you are using docker-compose, you can use the name of the service.

e.g:
`POSTGRES_HOST=postgres_service`

> POSTGRES_PORT=
>
The port number of the database.
If you are using docker-compose, you can use the port number of the service.
Default port number for postgres is 5432.

e.g: `POSTGRES_PORT=5432`


