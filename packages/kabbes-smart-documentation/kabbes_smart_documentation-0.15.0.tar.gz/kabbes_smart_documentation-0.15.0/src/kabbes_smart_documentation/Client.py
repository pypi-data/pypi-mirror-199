import kabbes_smart_documentation
import kabbes_client
import kabbes_pypi_builder

class Client( kabbes_smart_documentation.DocumentationGenerator ):

    _BASE_DICT = {}

    def __init__( self, dict={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( kabbes_smart_documentation._Dir, dict=d )
        cfg_sd = self.Package.cfg
        cfg_pypi = kabbes_pypi_builder.Client().cfg

        cfg_pypi.merge( cfg_sd )
        self.cfg = cfg_pypi

        kabbes_smart_documentation.DocumentationGenerator.__init__( self )

