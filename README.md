# flask-demo

A minimal Flask app used to demo Depot CI's built-in SSH debugging.

## Project structure

```
flask-demo/
├── app/
│   └── main.py          # Flask app with /health and /users endpoints
├── tests/
│   └── test_app.py      # pytest suite (includes DATABASE_URL checks)
├── .depot/
│   └── workflows/
│       ├── ci.yml        # broken workflow — DATABASE_URL not wired up
│       └── ci.fixed.yml  # fixed workflow — secret passed through correctly
├── Dockerfile
└── requirements.txt
```

## The bug

`ci.yml` builds and runs the image but never passes `DATABASE_URL` into the
container. The test suite checks for it explicitly, so `test_database_url_is_set`
fails with a clear assertion message:

```
AssertionError: DATABASE_URL is not set. Make sure it is configured as a secret in Depot CI.
```

## Demo flow

1. Push with `ci.yml` — watch the test step fail
2. Re-trigger the run with `--ssh-after-step 2` (after the build step)
3. SSH into the runner, poke around:

```bash
# Is the secret in the environment?
env | grep DATABASE

# Try running the tests yourself
docker run --rm myapp:ci pytest tests/ -v

# Confirm the image is there
docker images | grep myapp
```

4. Exit, swap in `ci.fixed.yml` as `ci.yml`, push again — green

## Local dev

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
pytest tests/ -v
```
