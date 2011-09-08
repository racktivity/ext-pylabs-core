class salesscheme:
	"""
	Description of the actions on a sales scheme object
	"""

	def create(self, collocation, cpu, storage, bandwidth, jobguid="", executionparams=None):
		"""
        Define the sales scheme of a datacenter
		
		@param collocation: rental price per rack in kEur per month
		@type collocation: float 

		@param cpu: sales price per cpu rack in kEur per month
		@type cpu: float 

		@param storage: sales price per storage rack in kEur per month
		@type storage: float

		@param bandwidth: sales price euros per Mbps per month
		@type bandwidth: float 

		@param jobguid: guid of the job if available, else empty string
		@type jobguid: guid

		@param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
		@type executionparams: dictionary

		@return: dictionary with datacenter sizing scheme
		@rtype: dictionary

		@note: example return result
		@note: {'result': salesschemeguid,
		@note:  'size': 1000,
		@note:  'racksurface': 3,
		@note:  'kwhourcost': 0.05,
		@note:  'pue': 1.4, 
		@note:  'jobguid': '5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

		@raise e: raise exception in case an error occurs
		"""
