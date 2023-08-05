import kabbes_client

R = kabbes_client.Root()
R.cfg.print_atts()

P = kabbes_client.Package( _Dir = R.cfg['cwd.Dir'], root=R )
P.cfg.print_atts()

print ( P.cfg['package.version'] )