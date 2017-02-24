# abstract class used for classes that are measurable
class Metric:
	# does a predefined operation on the metric variable
	@staticmethod
	def metric_func(metric):
		raise NotImplementedError("Metric Not Implemented")
	
	# initializes a metric value
	@staticmethod
	def init_metric(metric):
		raise NotImplementedError("No metric initializer")

	# does operations comparing a metric and data
	@staticmethod
	def calc_metric(metric, data):
		raise NotImplementedError("No metric calculator implemented")

# Object representing something in an environment
class Object:
	# Console representation of this object
	def toString(self):
		raise NotImplementedError("No to string method")
	
	# determines if an agent can move onto this object
	def isPassable(self):
		raise NotImplementedError("Passable not implemented")
	
	# changes state of object
	def changeState(self):
		raise NotImplementedError("No change state function")

# something that interacts with objects in the environment
class Agent:
	# Starts the agents interaction
	def process(self):
		raise NotImplementedError("Not process function")
	
	# gives the agent the environment to interact with
	def setEnv(self, env):
		raise NotImplementedError("No setEnv function")
