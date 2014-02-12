try:
	import sys
	import re
	import os
	import subprocess
	import tempfile
	import socket
	from core.configparser import ConfigParser
	from core.threadpool import Worker,ThreadPool
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        print exit_message
        sys.exit(1)


class MountDetect:
	def __init__(self, config_file, share_session, sharestatus_session, mount_path, umount_path, find_path, curl_path):
		"""
			Initialize functions and variables
		"""
		
		self.share_session = share_session
		self.sharestatus_session = sharestatus_session
		self.mount_path = mount_path
		self.umount_path = umount_path
		self.find_path = find_path
		self.curl_path = curl_path
		
		self.tika_ip = "localhost"
		self.tika_port = 9998

		sock = socket.socket()
		try:
			sock.connect((self.tika_ip, self.tika_port)) 		
		except:
			print "Tikaya Baglanti Saglanamadi"
			print exit_message
			sys.exit(22)	

		self.depdep_mount = "/mnt/depdep"
		if not os.path.exists(self.depdep_mount):
			os.mkdir(self.depdep_mount)
	
		self.config_result = ConfigParser.parse(config_file)

		self.output_file = self.config_result["output_file"]
		self.username = self.config_result["username"]
		self.password = self.config_result["password"]
		self.domain = self.config_result["domain"]

		file_include_type =  self.config_result["include_type"]
		file_exclude_type =  self.config_result["exclude_type"]	
		file_max_size =  self.config_result["max_filesize"]

		if file_include_type:
			ftype = ""
			for file_ext in file_include_type.split(","):
				if not ftype:
					ftype = file_ext
				else:
					ftype = ftype + "|" + file_ext 
			if file_max_size:
				self.find_cmd_opt = "-type f -size -%s -regextype posix-extended -regex '.*(%s)' -print"% (file_max_size,ftype)
			else:
				self.find_cmd_opt = "-type f -regextype posix-extended -regex '.*(%s)' -print"% (ftype)
		elif file_exclude_type:
			ftype = ""
                        for file_ext in file_exclude_type.split(","):
                                if not ftype:
                                        ftype = "[" + "^" + "(" +  file_ext + ")" + "]" 
                                else:   
                                        ftype = ftype + "|" + "[" + "^" + "(" +  file_ext + ")" + "]"
			if file_max_size:
				self.find_cmd_opt = "-type f -size -%s -regextype posix-extended -regex '.*(%s)' -print"% (file_max_size, ftype)		
			else:
				self.find_cmd_opt = "-type f -regextype posix-extended -regex '.*([^(htm)|^(ztmp)|^(vmsn)])' -print"
		else:
			if file_max_size:
				self.find_cmd_opt = "-type f -size -%s"% (file_max_size)
			else:
				self.find_cmd_opt = "-type f"

		self.filename_reg = {}
		self.filename_info = []
		filename_type = self.config_result["filename_keyword_name"]
		for reg_name in filename_type.keys():
			ret_case = filename_type[reg_name][0]		
			fcontent_type = filename_type[reg_name][1]		
			fcontent_desc = filename_type[reg_name][2]

			if ret_case == "insensitive":
				reg_filename = re.compile(reg_name, re.IGNORECASE)
				self.filename_info.append(fcontent_type)
				self.filename_info.append(fcontent_desc)
				self.filename_reg[reg_filename] = self.filename_info
				self.filename_info = []
			else:
				reg = re.compile(reg_name)
				self.filename_info.append(fcontent_type)
                                self.filename_info.append(fcontent_desc)
				self.filename_reg[reg_filename] = self.filename_info
				self.filename_info = []
	

		self.filecontent_reg = {}
		self.filecontent_info = []
		filecontent_type = self.config_result["filecontent_keyword_name"]
		for reg_content in filecontent_type.keys():
                        ret_case = filecontent_type[reg_content][0]
                        fname_type = filecontent_type[reg_content][1]
			fname_desc = filecontent_type[reg_content][2]

                        if ret_case == "insensitive":
                                reg_filecontent = re.compile(reg_content, re.IGNORECASE)
				self.filecontent_info.append(fname_type)
				self.filecontent_info.append(fname_desc)
				self.filecontent_reg[reg_filecontent] = self.filecontent_info
				self.filecontent_info = []
                        else:
                                reg_filecontent = re.compile(reg_content)
				self.filecontent_info.append(fname_type)
				self.filecontent_info.append(fname_desc)
				self.filecontent_reg[reg_filecontent] = self.filecontent_info
				self.filecontent_info = []



	def write_result(self, result, type):
		"""
			Write result into the result file
		"""
		
		try:
			result_file = open(self.output_file, "a")
		except:
			print "Result File Cannot Opened %s"% self.output_file

		if type == "filename":
			result_file.write("Filename <-> %s\n"% result)
		else:
			result_file.write("FileContent <-> %s"% result)

		result_file.close()



	def write_session_id(self, session_id):
                """
                        Write session id into the sharestatus.session file
                """

                session_file = open(self.sharestatus_session, "w")
                session_file.write(session_id)
                session_file.close()


	def get_session(self, session_id):
                """
                        Get session id from share.session file
                """

		try:
                	session_file = open(self.share_session, "r").read().splitlines()
		except:
			return None

                for session_line in session_file:
                         if re.match("%s,"% session_id,session_line):
				return session_line
		return None	



	def is_mounted(self, mount_point):
		"""
			Check whether sharing point is mounted or not ...
		"""

		cmd = ['%s'% self.mount_path]
		proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)

		for line in iter(proc.stdout.readline, ''):
        		if re.search(mount_point, line):
				return True

		return None



	def mount_device(self, cmd, *mount_point):
		"""
			Mount given remote device
		"""
		
	
		if cmd == "mount":
			remote_mount_point = mount_point[0] 
			local_mount_point = mount_point[1]

			if self.username and self.password and self.domain:
				creds = "'username=" + self.username + ",domain=" + self.domain + ",password=" + self.password + "'"
				mount_cmd = ['%s -o %s  %s %s'% (self.mount_path, creds, remote_mount_point, local_mount_point)]
			else:
				mount_cmd = ['%s -o guest  %s %s'% (self.mount_path, remote_mount_point, local_mount_point)]
		
			# debug
			print "Mounting with command: " + mount_cmd[0]	
			proc = subprocess.Popen(mount_cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out = proc.communicate()[0]
	
			return proc.returncode
		else:
			local_mount_point = mount_point[0]
			umount_cmd = ['%s %s'% (self.umount_path, local_mount_point)]
			proc = subprocess.Popen(umount_cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = proc.communicate()

			if err:
				print err
			else:
				pass
		

        def run_tika(self, filename):
                """
                        Run tika and get extract data
                """

                result_file = tempfile.NamedTemporaryFile(mode='w+t')
                result_file_name = result_file.name
                tika_command = """%s -T \"%s\" http://%s:%d/tika > %s"""% (self.curl_path, filename, self.tika_ip, self.tika_port, result_file_name)

                process = subprocess.Popen(tika_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out = process.communicate()[0]

                return result_file



	def run_find_command(self, path):
		"""
			Run find commands and get file types
		"""

		find_cmd = self.find_path + " " + path + " " + self.find_cmd_opt
		# debug 
		print "Content analysis running command: " + find_cmd
		proc = subprocess.Popen(find_cmd, shell = True, stdout = subprocess.PIPE)

		for file_name in iter(proc.stdout.readline, ''):
			if self.filename_reg:
				for depdep_reg in self.filename_reg.keys():	
					if re.search(depdep_reg, file_name):
						ret_type = self.filename_reg[depdep_reg][0]	
						ret_desc = self.filename_reg[depdep_reg][1]	
						result = ret_desc + " : " + file_name.strip()
						self.write_result(result, "filename")
						print "File Name -> %s "% result

			if self.filecontent_reg:
				result_file = self.run_tika(file_name.strip())
				result_file.seek(0)
				for line in result_file:
					for depdep_reg in self.filecontent_reg.keys():
						if re.search(depdep_reg, line):
							ret_type = self.filecontent_reg[depdep_reg][0]
							ret_desc = self.filecontent_reg[depdep_reg][1]
							result = file_name.strip() + " : " + ret_desc + " : " + line
							self.write_result(result, "filecontent")
							print "File Content -> %s"% result	


	def mount_sharing(self, line):
		"""
			Mount and end files to tika ...
		"""		

		ip = line.split(",")[1]
		create_path = "%s/%s"% (self.depdep_mount,ip)
		if not os.path.exists(create_path):	
			os.mkdir(create_path)

		sharings = line.split(",")[2]
		for point in sharings.split(":"):
			remote_mount_point = "//%s/%s"% (ip,point)
			local_mount_point = "%s/%s"% (create_path, point)

			if not self.is_mounted(remote_mount_point):
				if not os.path.exists(local_mount_point):
					os.mkdir(local_mount_point)
				
				ret = self.mount_device("mount", remote_mount_point, local_mount_point)
				if ret == 0:
					# debug
					print "Device mounted: " + local_mount_point
					self.run_find_command(local_mount_point)
					mnt_ret = self.mount_device("umount", local_mount_point)
				else:
					# debug
					print "Device cannot be mounted: " + remote_mount_point
					if os.path.exists(local_mount_point):
						os.rmdir(local_mount_point)
			else:
                                self.run_find_command(local_mount_point)
                                self.mount_device("umount", local_mount_point)




	def run(self, session_id):
		"""
			Run the main function ...
		"""

		self.thread_count = self.config_result["content_thread"]
		# debug
		print "Thread count to run mount %s"% self.thread_count

		pool = ThreadPool(int(self.thread_count))
		if session_id == 0:
			try:
				read_file = open(self.share_session, "r").read().splitlines()
			except Exception, err_mess:
				print err_mess
				print exit_message
				sys.exit(22)	
			
			for line in read_file:	
				pool.add_task(self.mount_sharing, line)

			pool.wait_completion()

			self.write_session_id(str(session_id))
			session_id = session_id + 1
		else:
			# debug 
			print "Session files will be used ..."

			while True:
				if self.get_session(session_id):
					line = self.get_session(session_id)
					pool.add_task(self.mount_sharing, line)
					self.write_session_id(str(session_id))
					session_id = int(session_id) + 1
				else:
					pool.wait_completion()
					break
