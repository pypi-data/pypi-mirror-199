import json
import logging
import os
from contextvars import ContextVar
from typing import Optional, Union
from uuid import uuid4

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

# Keeps track of logger id in the Thread, across different modules.
current_logger_id = ContextVar("Current logger id")


class LoggingManager:
    """Logging Manager

    A wrapper on Python built-in logging module. that handles GCP Cloud Logging
    According to importance there are 6 levels i.e Debug,Info,Warning
        ,Error,Exception,Critical
    """

    def __init__(
        self,
        name: str = __name__,
        level: int = logging.DEBUG,
        logger_id: Optional[str] = None,
    ):
        """Initializing Logging Manager

        Args:
            name (str, optional): name of module/class which initialize
                logging. Defaults to __name__.
            level (int, optional): level to determine importance & up to what
                point capture logs. Defaults to logging.DEBUG.
            logger_id (str, optional): id of the logger.
            DEBUG : 10
            INFO : 20
            WARNING : 30
            ERROR : 40
            At time of initialization whatever the level is given below score
                levels will be ignored.
        """
        if logger_id:
            self._set_logger_id(logger_id)

        self._is_local_dev = False
        self.exclude_keys = {}
        if os.environ.get("EXCLUDE_KEYS"):
            self.exclude_keys = json.loads(os.environ["EXCLUDE_KEYS"])

        self._logger = logging.getLogger(name)

        client = None
        try:
            client = google.cloud.logging.Client()
        except Exception:
            print("GCP Cloud Logging is not enabled.")

        if client:
            cloudlogging_formatter = logging.Formatter("%(name)s: %(message)s")
            cloud_handler = CloudLoggingHandler(client)
            cloud_handler.setFormatter(cloudlogging_formatter)
            self._logger.addHandler(cloud_handler)

        streamlog_format = "%(asctime)s [%(levelname)s] - %(name)s: %(message)s - JSON Payload: %(json_fields)s"  # noqa
        streamlog_formatter = logging.Formatter(fmt=streamlog_format)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(streamlog_formatter)
        self._logger.addHandler(stream_handler)

        self._logger.setLevel(level)

    @property
    def _logger_id(self) -> str:
        """Get logger from Thread ContextVar if one exists or set it."""
        try:
            return current_logger_id.get()
        except LookupError:
            self._set_logger_id(uuid4().hex)
            return current_logger_id.get()

    def _set_logger_id(self, logger_id: str) -> None:
        current_logger_id.set(logger_id)

    def _preprocess_json_params(self, params: dict) -> Union[dict, str]:
        for key in self.exclude_keys:
            params.pop(key, None)

        params["request_id"] = self._logger_id

        return params

    def log(
        self,
        msg: str,
        json_params: dict,
        level: int,
        skip_if_local: bool = False,
    ) -> None:
        if skip_if_local and self._is_local_dev:
            return

        processed_params = self._preprocess_json_params(json_params)
        self._logger.log(level, msg, extra={"json_fields": processed_params})

    def debug(
        self, msg: str, json_params: dict, skip_if_local: bool = False
    ) -> None:
        """Logs a debug message. Params: [msg] required"""
        self.log(
            msg, json_params, level=logging.DEBUG, skip_if_local=skip_if_local
        )

    def info(
        self, msg: str, json_params: dict, skip_if_local: bool = False
    ) -> None:
        """Logs a info message. Params: [msg] required"""
        self.log(
            msg, json_params, level=logging.INFO, skip_if_local=skip_if_local
        )

    def warning(
        self, msg: str, json_params: dict, skip_if_local: bool = False
    ) -> None:
        """Logs a warning message. Params: [msg] required"""
        self.log(
            msg,
            json_params,
            level=logging.WARNING,
            skip_if_local=skip_if_local,
        )

    def error(
        self, msg: str, json_params: dict, skip_if_local: bool = False
    ) -> None:
        """Logs an error message. Params: [msg] required"""
        self.log(
            msg, json_params, level=logging.ERROR, skip_if_local=skip_if_local
        )

    def exception(
        self, msg: str, json_params: dict, skip_if_local: bool = False
    ) -> None:
        """Logs an exception. Params: [msg] required"""
        self.log(
            msg, json_params, level=logging.ERROR, skip_if_local=skip_if_local
        )
