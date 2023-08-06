import kabbes_client
import real_time_input

class Client( real_time_input.RealTimeInput ):

    _BASE_DICT = {
        'PLATFORM_SYSTEM': real_time_input.PLATFORM_SYSTEM,
        'KEY_MAPPING': real_time_input.KEY_MAPPING
    }

    def __init__( self, dict={} ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        self.Package = kabbes_client.Package( real_time_input._Dir, dict=d )
        self.cfg_rti = self.Package.cfg

        real_time_input.RealTimeInput.__init__( self )
