require 'yaml'
require 'digest'

WOODPECKER_YML='.woodpecker.yml'
DOCKER_COMPOSE='compose.test.yml'

desc 'iniciar entorno'
task :up do
  compose('up', '--build', '-d')
end

desc 'poblar entorno'
task :init => [:up] do
  pecker = YAML.load_file(WOODPECKER_YML)
  ['tests', 'style'].each do |pipeline|
    pecker.dig('pipeline', pipeline, 'commands').grep(/install/).each do |cmd|
      compose('exec', 'app.dev', cmd)
    end
  end
  compose('exec', 'app.dev', 'bash .dev/install_module.sh')
end

desc 'terminal'
task :sh do
  compose('exec', 'app.dev', 'bash')
end

desc 'iterar'
task :tdd do
  refresh_cache
  compose('exec', 'app.dev', 'flake8')
  compose('exec', 'app.dev', 'python3 -m unittest')
end

desc 'detener entorno'
task :down do
  compose('down')
end

desc 'entorno vivo'
namespace :live do

  desc 'iniciar entorno'
  task :up do
    compose('up', '--build', '-d', compose: 'compose.yml')
  end

  desc 'monitorear salida'
  task :tail do
    compose('logs', '-f', 'app.dev', compose: 'compose.yml')
  end

  desc 'detener entorno'
  task :down do
    compose('down', compose: 'compose.yml')
  end
end

def compose(*arg, compose: DOCKER_COMPOSE)
  sh "docker-compose -f #{compose} #{arg.join(' ')}"
end

def refresh_cache
  # cuando se realizan cambios sobre los modelos
  # que afectan las tablas es necesario limpiar el cache
  # de trytond
  changes = []

  has_git_dir = File.directory?(File.join(File.dirname(__FILE__), '.git'))
  try_git = `which git`.then { $? }.success? && has_git_dir
  try_fossil = system('fossil status', err: :close, out: :close)

  if try_fossil
    changes = %x{fossil diff}.split("\n").grep(/^[-+]/)
  elsif try_git
    changes = %x{git diff}.split("\n").grep(/^[-+]/)
  else
    warn <<WARN
no se detecta repositorio en control de versiones, debe manualmente
limpiar el cache si ahi cambios en el esquema de los modelos.

Eliminando en el contenedor los archivo /tmp/*.dump
WARN
  end

  refresh_trytond_cache(changes)
end

def refresh_trytond_cache(changes)
  num = changes.grep(/fields/).length
  hash = Digest::MD5.hexdigest(changes.flatten.join(''))
  
  # touch
  File.open('.tdd_cache', 'a+').close
  
  File.open('.tdd_cache', 'r+') do |cache|
    tdd_cache = cache.read()
    
    if num > 0 && (tdd_cache != hash)
      compose('exec', 'app.dev', 'bash -c "rm -f /tmp/*.dump"')
      cache.seek(0); cache.write(hash)
    end
  end
end
