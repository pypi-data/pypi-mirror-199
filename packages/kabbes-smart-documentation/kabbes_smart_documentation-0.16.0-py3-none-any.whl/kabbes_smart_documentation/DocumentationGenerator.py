import kabbes_pypi_builder
import os

class DocumentationGenerator( kabbes_pypi_builder.PackageGenerator ):

    def __init__( self ):
        kabbes_pypi_builder.PackageGenerator.__init__( self )

    def generate_sphinx( self ):
        os.system( self.cfg['sphinx_script_Path'].read() ) 
