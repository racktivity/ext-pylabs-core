from pylabs.baseclasses import BaseEnumeration

class TransactionStatus(BaseEnumeration):
    """
    possible action statuses
    - DONE
    - RUNNING
    - FINISHED
    - FAILED
    """
    
TransactionStatus.registerItem('done')
TransactionStatus.registerItem('running')
TransactionStatus.registerItem('finished')
TransactionStatus.registerItem('failed')
TransactionStatus.finishItemRegistration()