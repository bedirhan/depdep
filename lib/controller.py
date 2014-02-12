try:
        import sys
        import argparse
	import os
        from main import Main
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        print exit_message
        sys.exit(1)


class Controller:
        """
                Parse Command Line Arguments and Control DepDep ...
        """

        def __init__(self):

                description = "Description ..."
                usage = "Usage: use --help for futher information"
                parser = argparse.ArgumentParser(description = description, usage = usage)
                parser.add_argument('-f','--config', dest = 'config', help = 'Configuration File', required = True)
                parser.add_argument('-w', '--wipe', dest = 'wipe', action = 'store', help = 'Wipe All Sessions', type = int)
                self.args = parser.parse_args()

		if not os.path.exists("sessions"):	
			os.mkdir("sessions")

        def run(self):
                """
                        Control DepDep start or stop and daemonize depdep ...
                """

                depdep = Main(self.args.config, self.args.wipe)
		try:	
                	depdep.run()
		except Exception, err_mess:
			print err_mess
			print exit_message	
			sys.exit(2)
