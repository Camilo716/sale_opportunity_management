require 'yaml'

WOODPECKER_YML='.woodpecker.yml'
DOCKER_COMPOSE='compose.test.yml'

desc 'iniciar entorno'
task :up do
  compose('up', '--build', '-d')
end

desc 'poblar entorno'
task :init => [:up] do
  pecker = YAML.load_file(WOODPECKER_YML)
  pecker.dig('pipeline', 'tests', 'commands').grep(/install/).each do |cmd|
    compose('exec', 'app.dev', cmd)
  end
end

desc 'terminal'
task :sh do
  compose('exec', 'app.dev', 'bash')
end

desc 'iterar'
task :tdd do
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
