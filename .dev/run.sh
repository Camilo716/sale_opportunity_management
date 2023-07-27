#!/bin/bash
# script para iniciar entorno vivo


SCRIPT_DIR=$(dirname `realpath $0`)

die() {
    echo $1
    exit 1
}

[ ! -d "$SRC" ] && die "no se ubica ruta en SRC"
[ -z "$DB_NAME" ] && die "se requiere variable DB_NAME"

set -e

# dependencias minimas
pip3 install psycopg2 proteus inotify honcho

# instalar dependencias de tryton desde paquete
python3 setup.py install

# usamos enlace al paquete
python3 setup.py develop

# instalar modulo
trytond_modules_path=`pip3 show trytond | grep Location | sed -nr 's/Location: +//gp'`/trytond/modules
module_name=`cat "$SRC/setup.py"  | fgrep -A 1 [trytond.modules] | sed 1d | cut -d '=' -f 1 | tr -d ' \n'`
[ ! -d "$trytond_modules_path" ] && die "fallo al ubicar ruta de modulos de trytond"
ln -sf "$SRC" "$trytond_modules_path/$module_name"

# inicializar base de datos
# https://docs.tryton.org/projects/server/en/latest/tutorial/module/setup_database.html
yes admin | trytond-admin -d ${DB_NAME} --all 


# ejecutar servidor
export SCRIPT_DIR
export MODULE_NAME=$module_name
export DB_NAME
export SRC

honcho -d ${SCRIPT_DIR} start
