
# General error class
class PySLError(Exception):
	""" Base exception class. Each exception consists of an error code and an error message. """
	def __init__( self, code, msg ):
		Exception.__init__(self)
		self.code = code
		self.msg = msg

	def __str__( self ):
		return "%d: %s" % ( self.code, self.msg )


# Specific errors

ERROR_DIRNOTFOUND       = 1
ERROR_INVALIDSERVER     = 2

class PySLDirNotFoundError( PySLError ):
	""" Exception thrown when a directory does not exist """
	def __init__( self ):
		PySLError.__init__( self, ERROR_DIRNOTFOUND, "Directory does not exist." )

class PySLInvalidServerError( PySLError ):
	""" Exception thrown when a server is not found on the config files """
	def __init__( self ):
		PySLError.__init__( self, ERROR_INVALIDSERVER, "Server does not exist on the configuration files." )
