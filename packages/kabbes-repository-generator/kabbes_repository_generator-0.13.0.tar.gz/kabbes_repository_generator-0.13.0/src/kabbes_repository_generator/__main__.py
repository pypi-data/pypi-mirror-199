import kabbes_repository_generator
repo_gen = kabbes_repository_generator.Client()
repo_gen.generate()

repo_gen.cfg.print_atts()

print ('Version: ' + repo_gen.cfg['repo.version'])