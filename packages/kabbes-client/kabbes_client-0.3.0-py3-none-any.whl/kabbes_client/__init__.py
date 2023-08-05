import dir_ops as do
import os
import xdg
import py_starter as ps

_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
_src_Dir = _Dir.ascend()                                  #src Dir that is one above
_repo_Dir = _src_Dir.ascend()                    
_cwd_Dir = do.Dir( do.get_cwd() )

_src_Dir = _Dir.ascend()                                  #src Dir that is one above
_repo_Dir = _src_Dir.ascend()                    
_cwd_Dir = do.Dir( do.get_cwd() )
_xdg_Dir = do.Dir( str(xdg.XDG_CONFIG_HOME ) )
_home_Dir = do.Dir( do.get_home_dir() )

sys_args, sys_kwargs = ps.get_system_input_arguments()

from .Root import Root, set_Root
set_Root( Root() ) #kabbes_client.root = Root()

from .Package import Package
