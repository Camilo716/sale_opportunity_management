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

# instalar modulo
source ${SCRIPT_DIR}/install_module.sh

# inicializar base de datos
# https://docs.tryton.org/projects/server/en/latest/tutorial/module/setup_database.html
yes admin | trytond-admin -d ${DB_NAME} --all 


# ejecutar servidor
export SCRIPT_DIR
export MODULE_NAME=$module_name
export DB_NAME
export SRC

honcho -d ${SCRIPT_DIR} start
