import logging

from core import Core

logger = logging.getLogger('core')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def run():
    core = Core(target=(6,))
    print(core.run((13,) * 5))
    core.plot()


if __name__ == '__main__':
    run()
