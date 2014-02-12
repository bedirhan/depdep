try:
	import sys
	import re
	import os
	import tempfile
	import subprocess
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        print exit_message
        sys.exit(7)



class Nmap:
	"""	
		Nmap operations ...
	"""

        def __init__(self, nmap_path):
		"""
			init functions and variables ...
		"""

                self.nmap = nmap_path
                self.port_reg = re.compile("Host:\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s\(\)\s+Ports:\s445")


	def write_result(self, result, output_file):
                """
                        Write results to the tmp file ... 
                """

                file = open(output_file,"a")
                file.write("%s\n"% result)
                file.close()


        def port_scan(self, include_ip, exclude_ip = None):
		"""
			Port scan using nmap ...
		"""

		result = []

                nmap_result_file = tempfile.NamedTemporaryFile(mode='w+t')
                nmap_result_file_name = nmap_result_file.name

		if exclude_ip:
                	nmap_scan_option = "-n -PN -sS -T4 --open -p 445 --host-timeout=10m --max-rtt-timeout=600ms --initial-rtt-timeout=300ms --min-rtt-timeout=300ms --max-retries=2 --min-rate=150 %s --exclude %s -oG %s"% (include_ip, exclude_ip, nmap_result_file_name)
		else:
			nmap_scan_option = "-n -PN -sS -T4 --open -p 445 --host-timeout=10m --max-rtt-timeout=600ms --initial-rtt-timeout=300ms --min-rtt-timeout=300ms --max-retries=2 --min-rate=150 %s -oG %s"% (include_ip, nmap_result_file_name)

                run_nmap = "%s %s"% (self.nmap, nmap_scan_option)

                proc = subprocess.Popen([run_nmap], shell=True, stdout=subprocess.PIPE,)
                stdout_value = str(proc.communicate())

                nmap_result_file.seek(0)
                for line in nmap_result_file:
                        if re.search(self.port_reg, line):
                                host = re.search(self.port_reg, line).group(1)
				result.append(host)

                nmap_result_file.close()
                if result:
                        return result
                else:
                        return None
