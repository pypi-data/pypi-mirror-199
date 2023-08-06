import configparser
import importlib.util
import logging
import os
import sys
from ast import literal_eval
from datetime import datetime, timedelta
from appdirs import user_config_dir

LOG_LEVEL = logging.INFO
LOG_FORMAT = \
    '%(process)s %(thread)s [%(asctime)s] %(levelname)s %(name)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger('pycronscript')

CONF_DIR = user_config_dir('pycronscript')
CONF_FILE = os.path.join(CONF_DIR, 'config.cfg')
config = configparser.ConfigParser()

if os.path.isfile(CONF_FILE):
    config.read(CONF_FILE)
else:
    if not os.path.exists(CONF_DIR):
        os.makedirs(CONF_DIR)
    with open(CONF_FILE, 'w') as config_file:
        config.write(config_file)
    logger.info("Configuration file created: %s" % CONF_FILE)


def must_run(section):
    try:
        file = os.path.join(CONF_DIR, '.%s' % section)
        with open(file, 'r') as f:
            timestamp = float(f.read())
            last_run = datetime.fromtimestamp(timestamp)
    except Exception:
        last_run = None

    if not last_run:
        return True

    try:
        delta = timedelta(**literal_eval(config.get(section, 'each')))
    except Exception:
        logger.warning("Empty or bad 'each' for '%s'. (Default=1h)" % section)
        delta = timedelta(hours=1)

    if (datetime.now() - last_run) > delta:
        return True
    return False


def get_target(section):
    target = None
    if not must_run(section):
        return target
    try:
        spec = importlib.util.spec_from_file_location(
            section, config.get(section, 'path'))
        module = importlib.util.module_from_spec(spec)
        sys.modules[section] = module
        spec.loader.exec_module(module)
        target = module.run
    except Exception as e:
        logger.error("ERROR loading '%s': %s" % (section, str(e)))
    return target


def set_timestamp(section):
    file = os.path.join(CONF_DIR, '.%s' % section)
    with open(file, 'w') as f:
        f.write(str(datetime.now().timestamp()))
