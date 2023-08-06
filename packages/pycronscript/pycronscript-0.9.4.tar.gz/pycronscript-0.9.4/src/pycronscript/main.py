import threading
import time
from . import config

logger = config.logger


def wrapper(section, target):
    try:
        target()
        config.set_timestamp(section)
    except Exception as e:
        logger.error("ERROR running '%s': %s" % (section, str(e)))


def run():
    thread = None
    sections = config.config.sections()[::-1]
    if not sections:
        logger.info("NO SECTION TO RUN, more info:\n"
            "https://github.com/tiyujopite/pycronscript/blob/main/README.md")
        return
    while True:
        if thread and thread.is_alive():
            logger.info("WAITING for last section to finish")
        else:
            section = sections and sections.pop() or None
            target = config.get_target(section)
            if target:
                thread = threading.Thread(
                    target=wrapper, args=(section, target))
                logger.info("STARTING to run '%s'", section)
                thread.start()
            else:
                logger.info("NOTHING to do")

        time.sleep(60)
        if not sections:
            sections = config.config.sections()[::-1]


if __name__ == '__main__':
    run()
