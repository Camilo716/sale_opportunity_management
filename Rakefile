require 'yaml'

WOODPECKER_YML='.woodpecker.yml'
DOCKER_COMPOSE='docker-compose.test.yml'

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

desc 'iterar'
task :tdd do
  compose('exec', 'app.dev', 'python3 -m unittest')
end

desc 'detener entorno'
task :down do
  compose('down')
end

def compose(*arg)
  sh "docker-compose -f #{DOCKER_COMPOSE} #{arg.join(' ')}"
end
