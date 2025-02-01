from uvicorn.workers import UvicornWorker


class GunicornUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"proxy_headers": True, "log_config": "gunicorn-logging.yaml"}
