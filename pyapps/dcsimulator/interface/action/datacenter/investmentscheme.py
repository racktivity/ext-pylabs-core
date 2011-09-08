class investmentscheme:
	"""
	Investment scheme actions
	"""

	def create(self, leasebuilding="", leaseinfrastructure="", leasehw="", interestbuilding="", interestdatacenter="", leaseperiodbuilding="20", leaseperioddatacenter="3", technology="", installperiod="12", jobguid="", executionparams=None):
		"""
		Create a datacenter investment scheme

		@param leasebuilding: percentage of building in leasing
		@type leasebuilding: integer

		@param leaseinfrastructure: percentage of infrastructure in leasing
		@type leaseinfrastructure: integer

		@param leasehw: percentage of hardware in leasing
		@type leasehw: integer

		@param interestbuilding: interest rate of leasing the building
		@type interesbuilding: float

		@param interestdatacenter: interest rate of leasing datacenter infrastructure
		@type interestdatacenter: float

		@param leaseperiodbuilding: leasing period of the building, expressed in years, by default 20 years
		@type leaseperiodbuilding: integer

		@param leaseperioddatacenter: leasing period of datacenter infrastructure, expressed in years, by default 3 years
		@type leaseperioddatacenter: integer

		@param technology: percentage of technology that is installed prior to activation of datacenter
		@type technology: integer

		@param installperiod: period for installing the datacenter, expressed in months, by default 12 months
		@type installperiod: integer

		@param jobguid: guid of the job, if available
		@type jobguid: guid

		@param executionparams: dictionary of job specific params e.g. userErrormsg, maxduration ...
		@type executionparams: dictionary

		@return: dictionary with investment scheme
		@rtype: dictionary

		@note: example return value
		@note: {'result': investmentschemeguid,
		@note:  'leasebuilding': 0,
		@note:  ...
		@note:  'installperiod': 18,
		@note:  'jobguid': '5D2C0F39-F34E-4542-9B6F-B9233E80D803'}

		@raise e: raise exception in case an error occurs
		"""
