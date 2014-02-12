try:
        import sys
        from xml.etree import ElementTree
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        print exit_message
        sys.exit(1)



class ConfigParser:
	result = {}

	@staticmethod
        def parse(config_file):
		if not ConfigParser.result:
			try:
                		with open(config_file, 'rt') as f:
                        		tree = ElementTree.parse(f)
			except:
				raise


			try:
				node_list = ["target","settings","content", "scanning"]
				for node_name in node_list:
					for item in tree.getiterator(node_name):
						if node_name == "target":
							include_ip = ""
							exclude_ip = ""
							for node in item.findall('include-ip'):
                                                		if not include_ip:
                                                        		include_ip = node.text.strip()
                                                		else:   
                                                        		include_ip = include_ip + " " + node.text.strip()

							for node in item.findall('exclude-ip'): 
                                                		if not exclude_ip:
                                                        		exclude_ip = node.text.strip()
                                                		else:  
                                                        		exclude_ip = exclude_ip + "," + node.text.strip()

							ConfigParser.result["include_ip"] = include_ip 
							ConfigParser.result["exclude_ip"] = exclude_ip

						elif node_name == "scanning":
							thread = item.find("thread").text.strip()

							ConfigParser.result["scanning_thread"] = thread 

						elif node_name == "settings":
                                        		max_filesize = item.find('max_filesize').text.strip()
                                        		output_file = item.find('output_file').text.strip()

                                        		ConfigParser.result["max_filesize"] = max_filesize
                                        		ConfigParser.result["output_file"] = output_file

							username = ""
							password = ""
							domain = ""
							if (item.find('credentials/username') is not None) and (item.find('credentials/password') is not None) and (item.find('credentials/domain') is not None):
								if item.find('credentials/username').text is not None:
									username = item.find('credentials/username').text.strip()
								
								if item.find('credentials/password').text is not None:
									password = item.find('credentials/password').text.strip()

								if item.find('credentials/domain').text is not None:
									domain = item.find('credentials/domain').text.strip()	

							ConfigParser.result["username"] = username
							ConfigParser.result["password"] = password
							ConfigParser.result["domain"] = domain

						elif node_name == "content":
							content_thread = item.find('thread').text.strip()
							ConfigParser.result["content_thread"] = content_thread

							include_type = ""
							exclude_type = ""
							for node in item.findall('filetype/include-type'):
                                                                if not include_type:
                                                                        include_type = node.text.strip()
                                                                else:   
                                                                        include_type = include_type + "," + node.text.strip()

                                                        for node in item.findall('filetype/exclude-type'):
                                                                if not exclude_type:
                                                                        exclude_type = node.text.strip()
                                                                else:   
                                                                        exclude_type = exclude_type + "," + node.text.strip()

                                                        ConfigParser.result["include_type"] = include_type
                                                        ConfigParser.result["exclude_type"] = exclude_type
				
							filename_type = {}
							filename_type_list = []
							filecontent_type = {}
							filecontent_type_list = []	
							for node in item.findall('filename/keyword'):
                                                        	keyword_name = node.text.strip()
								keyword_case = node.get('case').strip()
								keyword_type = node.get('type').strip()
								keyword_description = node.get('description').strip()

								filename_type[keyword_name] = filename_type_list
								filename_type_list.append(keyword_case)
								filename_type_list.append(keyword_type)
								filename_type_list.append(keyword_description)
				
								ConfigParser.result["filename_keyword_name"] = filename_type
								filename_type_list = []
							
							filename_type = {}
                                                        filename_type_list = []
                                                        filecontent_type = {}
                                                        filecontent_type_list = []	
							for node in item.findall('filecontent/keyword'):
                                                        	keyword_name = node.text.strip()
								keyword_case = node.get('case').strip()
								keyword_type = node.get('type').strip()
								keyword_description = node.get('description').strip()

								filename_type[keyword_name] = filename_type_list
								filename_type_list.append(keyword_case)
								filename_type_list.append(keyword_type)
								filename_type_list.append(keyword_description)
					
								ConfigParser.result["filecontent_keyword_name"] = filename_type
								filename_type_list = []
							
				return ConfigParser.result
			except:		
				raise
		else:
			return ConfigParser.result	
