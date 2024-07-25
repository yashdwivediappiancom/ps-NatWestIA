import os
import json
from pathlib import Path

from logging.handlers import RotatingFileHandler
import logging.config

import appian_locust.utilities.logger

from appian_locust.uiform import SailUiForm

DEBUG_DIR = ".\\debug"

RECORDED_RESPONSES_DIR = ".\\recorded_responses"

LOGGER_NAME = "appian-locust"


def clean_debug_dir():
    # First create any required debug directories if they don't exist
    Path(DEBUG_DIR).mkdir(parents=True, exist_ok=True)
    Path(RECORDED_RESPONSES_DIR).mkdir(parents=True, exist_ok=True)

    # clean_debug_dir()
    clean_dir(dir=DEBUG_DIR)

    # clean dir appian-locust uses to output request/responses
    clean_dir(dir=RECORDED_RESPONSES_DIR)


def debug_write_ui_state_to_file(ref: str, filename: str, form: SailUiForm):
    path = DEBUG_DIR + "\\" + filename + "_" + ref + ".json"
    file = open(path, "w", encoding="utf-8")
    file.write(json.dumps(form.get_latest_state(), indent=4))
    file.close()


def fill_rich_text_field(form: SailUiForm, field: str, text: str):
    rich_text_v = "{\"protocolVersion\":2,\"action\":\"SAVE\",\"name\":\"richText\",\"value\":\"<div>" + text + "\\t</div>\"}"
    return form.fill_text_field(
        field,
        rich_text_v
    )


def clean_dir(dir: str):
    files_to_remove = [os.path.join(dir, f) for f in os.listdir(dir)]
    for f in files_to_remove:
        os.remove(f)


def set_up_logger():
    # TODO - better logging configuration
    #   1. Configure logger to be set up via config file rather than code below
    # Logging - set up via conf file
    #   (nb this requires --skip-log-setup and
    #   currently stops errors being output to console which is very annoying)
    # logging.config.fileConfig(fname='./log.conf')
    # logger = logger.getLogger()
    # logger.info("logger set up from conf file")

    # Logging - set up on top of Locust's standard logging
    logger = appian_locust.utilities.logger.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    # create a file handler
    handler = RotatingFileHandler('./logs/appian-locust.log', maxBytes=1 * 1024 * 1024, backupCount=10)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)12s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


class Utilities:
    # def get_form_with_dynamic_component(self, label: str, form: SailUiForm) -> SailUiForm:
    #     component = find_component_by_attribute_in_dict(
    #         'label', label, form.get_latest_state())
    #     if component is None:
    #         return form.get_latest_form()
    #     else:
    #         return form

    pass
