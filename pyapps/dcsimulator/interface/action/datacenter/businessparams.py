class businessparams:
    """
    Business params actions
    """

    def create(self, name, size, racksurface, kwhourcost, pue, salescollocation, salescpu, salesstorage, salesbandwidth,
               collocation="", storage="", cpu="", leasebuilding="", leaseinfrastructure="", leasehw="", 
               interestbuilding="", interestdatacenter="", leaseperiodbuilding="20", leaseperioddatacenter="3",
               technology="", installperiod="12", jobguid="", executionparams=None):
        """
        Create a datacenter business params scheme

        @param name: name of datacenter
        @type name: string
        
        @param size: datacenter size in square meters
        @type size: integer

        @param racksurface: required square meters per rack
        @type racksurface: integer

        @param kwhourcost: cost per kW/h
        @type kwhourcost: float

        @param pue: power usage effectiveness, ratio effective power needed per theoretical required power
        @type pue: float

        @param salescollocation: rental per rack in kEur/month
        @type salescollocation: float

        @param salescpu: sales of cpu rack in kEur/month
        @type salescpu: float

        @param salesstorage: sales of storage rack in kEur/month
        @type salesstorage: float

        @param salesbandwidth: sales of bandwidth in Eur per Mbps per month
        @type salesbandwidth: float
        
        @param collocation: percentage of racks used for collocation
        @type collocation: integer

        @param storage: percentage of racks used for storage nodes
        @type storage: integer

        @param cpu: percentage of racks used for cpu nodes
        @type cpu: integer
        
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
        
        @return: dictionary with business params scheme
        @rtype: dictionary
        
        @note: example return value
        @note: {'result': businessparamsguid,
        @note:  'collocation': 15,
        @note:  ...
        @note:  'salesbandwidth': 7,
        @note:  'jobguid': '5D2C0F39-F34E-4542-9B6F-B9233E80D803'}
        
        @raise e: raise exception in case an error occurs
        """
        