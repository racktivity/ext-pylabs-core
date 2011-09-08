class sizingscheme:
	"""
	Description of the actions on a sizing scheme object
	"""

	def create(self, size, racksurface, kwhourcost, pue, jobguid="", executionparams=None):
		"""
        Define the sizing scheme of a datacenter, set datacenter surface and surface per rack; cost per kWh and pue.
		
		@param size: total surface of datacenter, in square meters
		@type size: integer

		@param racksurface: surface taken by one rack, in square meters
		@type racksurface: integer

		@param kwhourcost: cost per kWh of the datacenter
		@type kwhourcost: float

        @param pue: power usage effectivness, ratio effective power needed for theoretical power needed
		@type pue: float

		@param jobguid: guid of the job if available, else empty string
		@type jobguid: guid

		@param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
		@type executionparams: dictionary

		@return: dictionary with datacenter sizing scheme
		@rtype: dictionary

		@note: example return result
		@note: {'result': sizingschemeguid,
		@note:  'size': 1000,
		@note:  'racksurface': 3,
		@note:  'kwhourcost': 0.05,
		@note:  'pue': 1.4, 
		@note:  'jobguid': '5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

		@raise e: raise exception in case an error occurs
		"""
