
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

ERROR_GENERALERROR      = 0
ERROR_DIRNOTFOUND       = 1
ERROR_INVALIDSERVER     = 2
ERROR_DIRNOTMOUNTED     = 3
ERROR_NOPERMISSION      = 4

class PySLDirNotFoundError( PySLError ):
   """ Exception thrown when a directory does not exist """
   def __init__( self, msg="Directory does not exist." ):
	   PySLError.__init__( self, ERROR_DIRNOTFOUND, msg )

class PySLInvalidServerError( PySLError ):
   """ Exception thrown when a server is not found on the config files """
   def __init__( self, msg="Server does not exist on the configuration files." ):
      PySLError.__init__( self, ERROR_INVALIDSERVER, msg )

class PySLDirNotMountedError( PySLError ):
   """ Exception thrown when a folder is not an existing mountpoint """
   def __init__( self, msg="Directory is not a mountpoint." ):
      PySLError.__init__( self, ERROR_DIRNOTMOUNTED, msg )

class PySLNoPermissionsError( PySLError ):
   """ Exception thrown when a folder is not an existing mountpoint """
   def __init__( self, msg="No permissions to perform this operation." ):
      PySLError.__init__( self, ERROR_NOPERMISSION, msg )

