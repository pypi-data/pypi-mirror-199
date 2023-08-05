import kabbes_client
import kabbes_config
import dir_ops as do

class Root:

    _config_dict = {
        "cwd.!Dir":    kabbes_client._cwd_Dir,
        "xdg.!Dir":    kabbes_client._xdg_Dir,
        "home.!Dir":   kabbes_client._home_Dir
    }

    _config_json_Path = kabbes_client._Dir.join_Path( path='Root.json' )
    _config_cache_json_rel_Path = do.Path( path= do.join(kabbes_client._Dir.lowest(), 'Root_cache.json')  )  

    def __init__( self ):

        ### Load baseline
        self.cfg = kabbes_config.Config( dict = Root._config_dict )
        
        ### Load Root.json
        cfg_json = kabbes_config.Config( dict = Root._config_json_Path.read_json_to_dict() )
        self.cfg.merge( cfg_json )

        ### Load Cache -> Root_cache.json
        if not self.cfg[ 'config.Dir' ].exists():
            self.cfg['config.Dir'].create( override=True )

        config_cache_json_Path = self.cfg['config.Dir'].join_Path( Path = Root._config_cache_json_rel_Path )
        if not config_cache_json_Path.exists():
            config_cache_json_Path.write( string='{}' )
            dict = {}
        else:
            dict = config_cache_json_Path.read_json_to_dict()

        cfg_cache = kabbes_config.Config( dict = dict )
        self.cfg.merge( cfg_cache )

        ### Load cwd Config - user_config.json
        self.cfg_cwd = kabbes_config.Config()
        if self.cfg[ 'cwd.config.Path' ].exists():
            self.cfg_cwd = kabbes_config.Config( dict = self.cfg['cwd.config.Path'].read_json_to_dict() )
            self.cfg.merge( self.cfg_cwd )

        ### Load system kwargs
        self.cfg_sys = kabbes_config.Config( dict = kabbes_client.sys_kwargs )
        self.cfg.merge( self.cfg_sys )  

        ### Load user specified config
        self.cfg_user = kabbes_config.Config()
        if self.cfg.has_key( 'user.config.path' ):
            if self.cfg['user.config.Path'].exists():
                self.cfg_user = kabbes_config.Config( dict=self.cfg['user.config.Path'].read_json_to_dict() )
                self.cfg.merge( self.cfg_user ) #merge at root now, merge on package key later


def set_Root( root_inst ):
    kabbes_client.root = root_inst
