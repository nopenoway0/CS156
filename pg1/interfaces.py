class Metric:
	@staticmethod
	def metric_func(metric):
		raise NotImplementedError("Metric Not Implemented")
	
	@staticmethod
	def init_metric(metric):
		raise NotImplementedError("No metric initializer")

	@staticmethod
	def calc_metric(metric, data):
		raise NotImplementedError("No metric calculator implemented")

class Object:
	def toString(self):
		raise NotImplementedError("No to string method")
	def isPassable(self):
		raise NotImplementedError("Passable not implemented")
	def changeState(self):
		raise NotImplementedError("No change state function")

class Agent:
	def process(self):
		raise NotImplementedError("Not process function")
	def setEnv(self, env):
		raise NotImplementedError("No setEnv function")
