import roslib; roslib.load_manifest('rostop')
import rosnode
import rospy
import xmlrpclib
import psutil

ID = '/NODEINFO'

class NodeInfo(object):
	nodes = dict()
	def get_node_info(self, node_name):
		node_api = rosnode.get_api_uri(rospy.get_master(), node_name)
		code, msg, pid = xmlrpclib.ServerProxy(node_api[2]).getPid(ID)
		if node_name in self.nodes:
			return self.nodes[node_name]
		else:
			try:
				p = psutil.Process(pid)
				self.nodes[node_name] = p
				return p
				# print '%s\t%0.2f%%' % (node_name, process.get_cpu_percent())
			except:
				return False


	def get_all_node_info(self):
		infos = []
		for node_name in rosnode.get_node_names():
			info = self.get_node_info(node_name)
			if info is not False: infos.append((node_name, info))
		return infos

	def get_all_node_fields(self, fields):
		processes = self.get_all_node_info()
		infos = []
		for name, p in processes:
			infos.append(p.as_dict(fields))
			infos[-1]['node_name'] = name
		return infos