import kabbes_pypi_builder
import kabbes_client
import kabbes_repository_generator
import datetime

class Client( kabbes_pypi_builder.PackageGenerator ):

    _BASE_DICT = { "year_str": str(datetime.datetime.now().year) }

    def __init__( self, dict={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( kabbes_pypi_builder._Dir, dict=d )
        cfg_pypi = self.Package.cfg
        cfg_repo_gen = kabbes_repository_generator.Client().cfg

        cfg_repo_gen.merge( cfg_pypi )
        self.cfg = cfg_repo_gen


        kabbes_pypi_builder.PackageGenerator.__init__( self )

