# script para refrescar cambios de xml del modulo de tryton
import sys
import os
import logging
import time

import inotify.adapters

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

SRC = os.environ['SRC']
MODULE_NAME = os.environ['MODULE_NAME']
DB_NAME = os.environ['DB_NAME']

def _main():
    i = inotify.adapters.Inotify()

    i.add_watch(SRC)
    logging.info("MONITOREANDO ARCHIVOS EN %s", SRC)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        (_, ext) = os.path.splitext(filename)
        if 'IN_CLOSE_WRITE' not in type_names:
            continue

        if ext in ['.py', '.xml', '.cfg']:
            for _ in range(0, 10):
                if os.system("trytond-admin -d {} -u {}".format(DB_NAME, MODULE_NAME)) != 0:
                    time.sleep(2)
                    logging.error("fallo trytond-admin")
                else:
                    logging.info("ACTUALIZADO TRYTOND POR CAMBIO DE ARCHIVO %s", filename)
                    break


if __name__ == '__main__':
    _main()
