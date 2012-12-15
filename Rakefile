require 'rake/packagetask'

def version()
  ENV['GO_PIPELINE_LABEL'] || 'dev'
end

Rake::PackageTask.new("puppet", version) do |p|
  p.need_tar = true
  p.package_files.include("puppet/**/*")
end
