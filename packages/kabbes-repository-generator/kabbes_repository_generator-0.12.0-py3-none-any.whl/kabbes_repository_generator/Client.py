import kabbes_repository_generator
import kabbes_client

class Client( kabbes_repository_generator.RepositoryGenerator ):

    _BASE_DICT = {}

    def __init__( self, dict={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( kabbes_repository_generator._Dir, dict=d )
        self.cfg = self.Package.cfg

        kabbes_repository_generator.RepositoryGenerator.__init__( self )
