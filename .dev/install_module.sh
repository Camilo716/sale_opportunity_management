# este script fuerza que los cambios se vean reflejados
# directamente en trytond.
#
# variables exportadas:
# - module_name

[ ! -d "$SRC" ] && die "no se ubica ruta en SRC"

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


# se limpia para evitar enlaces recursivos
module_trytond_path="$trytond_modules_path/$module_name"
rm -f "$module_trytond_path"
ln -sf "$SRC" "$module_trytond_path"
