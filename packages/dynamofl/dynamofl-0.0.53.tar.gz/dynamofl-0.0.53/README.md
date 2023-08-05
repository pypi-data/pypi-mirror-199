# Development

## Tired of copy-pasting your latest changes into `site-packages` ?

Follow the steps below to run the `samples` against your latest code

1. Open `<venv>/bin/activate` 
2. Paste the below code snippet to the end of file and set `CLIENT_PY_DIR` 
```
CLIENT_PY_DIR=<absolute path to client-py repo>
SYSPATHS=$($VIRTUAL_ENV/bin/python -c "import sys; print(':'.join(x for x in sys.path if x))")
export PYTHONPATH=$SYSPATHS":"$CLIENT_PY_DIR
```
3. Run `pip uninstall dynamofl` to delete the `dynamofl` package from `site-packages`

<br>

> To test against a published `dynamofl` SDK, run `pip install dynamofl` before running the samples