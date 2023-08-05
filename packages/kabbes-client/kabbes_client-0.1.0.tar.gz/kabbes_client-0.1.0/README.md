# client


# pecking order, lowest to highest

* Root -> _config_dict
* Root -> _config_json_Path
* Root -> _config_cache_Path
* Root -> cwd_config
* Root -> sys_kwargs
* Root -> user.config.path

* Package -> _config_dict
* Package -> _Dir
* Package -> _config_json_Path
* Package -> package.config.cache.Path
* Package -> Root.cfg_cwd[ 'package.name' ]
* Package -> Root.cfg_user[ 'package.name' ]
* Package -> overwrite dict
* Package -> Root.cfg_sys[ 'package.name' ]
