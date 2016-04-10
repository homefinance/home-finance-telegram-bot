import logging
import os

formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')


def make_loger(name, logfile):
    logger = logging.getLogger('financekeeper.'+name)
    logger.setLevel(logging.DEBUG)

    console_h = logging.StreamHandler()
    console_h.setLevel(logging.DEBUG)
    console_h.setFormatter(formatter)
    file_h = logging.FileHandler(os.path.dirname(os.path.abspath(__file__))+'/../logs/%s.log' % (logfile, ), encoding='utf-8')
    file_h.setFormatter(formatter)

    logger.addHandler(console_h)
    logger.addHandler(file_h)
    return logger

main_log = make_loger('telegram_bot', 'financekeeper_bot')