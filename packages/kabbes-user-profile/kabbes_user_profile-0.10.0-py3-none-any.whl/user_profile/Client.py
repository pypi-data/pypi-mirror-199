import kabbes_client
import user_profile
import py_starter as ps

class Client( user_profile.Profile ):

    _BASE_DICT = {
        "user_to_load": ps.get_env_var('USER') if ps.get_env_var('USER') != None else 'USER'
    }

    def __init__( self, dict={} ):
        
        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( user_profile._Dir, dict=d )
        self.cfg = self.Package.cfg

        user_profile.Profile.__init__( self )

