class distributionscheme:
	"""
	Description of the actions on a distribution scheme object
	"""

	def create(self, collocation="", storage="", cpu="", jobguid="", executionparams=None):
		"""
		Create a distribution scheme for the racks in a datacenter

		@param collocation: percentage of racks used for rental to 3rd party users
		@type collocation: integer

		@param storage: percentage of racks used for storage nodes
		@type storage: integer

		@param cpu: percentage of racks used for cpu nodes
		@type cpu: integer

		@param jobguid: guid of the job if available, else empty string
		@type jobguid: guid

		@param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
		@type executionparams: dictionary

		@return: dictionary with distribution scheme
		@rtype: dictionary

		@note: example return result
		@note: {'result': distributionschemeguid,
		@note:  'collocation': 25,
		@note:  'storage': 50,
		@note:  'cpu': 25,
		@note:  'jobguid': '5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

		@raise e: raise exception in case an error occurs
		"""
