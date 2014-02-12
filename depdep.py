#!/usr/bin/python

try:
        import sys
        from lib.controller import Controller
        from lib.core.common import *
        from lib.core.version import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        print exit_message
        sys.exit(1)


##
### Main ...
##

if __name__ == "__main__":

	try:
       		controller = Controller()
       		controller.run()
	except Exception, err_mess:
		print err_mess
		print exit_message	
		sys.exit(2)
 
