import roslib; roslib.load_manifest('rostop')
import rosnode
import rospy
import xmlrpclib
import psutil

ID = '/NODEINFO'

class NodeInfo(object):
	pids = dict()
	def get_node_info(self, node_name):
		node_api = rosnode.get_api_uri(rospy.get_master(), node_name)
		code, msg, pid = xmlrpclib.ServerProxy(node_api[2]).getPid(ID)
		if pid in self.pids:
			return self.pids[pid]
		else:
			try:
				p = psutil.Process(pid)
				self.pids[pid] = p
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