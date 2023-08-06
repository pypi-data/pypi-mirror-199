import kabbes_nanoid
import kabbes_client
import py_starter as ps
from parent_class import ParentClass

class Client( ParentClass ):

    _BASE_DICT = {}

    def __init__( self, dict={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( kabbes_nanoid._Dir, dict=d )
        self.cfg_nano = self.Package.cfg

    def make_Nanoid( self, **kwargs ):

        default_kwargs = {
            "alphabet": self.cfg_nano['alphabet'], 
            "size": self.cfg_nano['size']
        }

        return kabbes_nanoid.Nanoid( **ps.merge_dicts(default_kwargs, kwargs) )
