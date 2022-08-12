# skin cancer diagnostic system

using flask

## installation steps

- STEP 1
  run installation command below

`pip install -r requirements.txt`

- STEP 2
  intialize database by running the command below

`flask db init`

- STEP 3
  migrate and upgrade db run the command below

```
flask db migrate --message "initial migration"
flask db upgrade
```

- STEP 4
  start the api by running

`flask run`
