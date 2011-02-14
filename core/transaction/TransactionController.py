from pymonkey.Shell import *
import string
#import sys
#import inspect
#import operator
from Transaction import Transaction
import pymonkey

class TransactionController(object):
    '''
    Manager controlling actions
    Transactions = pylabs transactions
    see #@todo doc on pylabs
    @property transactions: array of transactions 
    @property width: Maximum width of output
    @property maxloglevel : max loglevel which will be captured (default for all transactions)
    for more info see: http://www.pylabs.org/display/PM/Transactions
    '''
    def __init__(self):
        self.activeTransaction=None
        self.transactions=[] #list of transactions
        self.maxloglevel=5
        self.send2console=True
    def hide(self,maxloglevel, callback, callbackparams):
        self.start("hide", "", "", maxloglevel, callback, callbackparams,noOutput=True)

    def start(self, description, errormessage=None, resolutionmessage=None,maxloglevel=2,maxloglevelcapture=5,\
              callback=None,callbackparams=None,silent=False):
        '''Start a new transaction and return the transaction

        @param description: Description of the transaction
        @param errormessage: Error message displayed to the user when the transaction fails
        @param resolutionmessage: Resolution message displayed to the user when the transaction fails
        @param maxloglevel specify which logs with max level should be remembered when doing the transaction
        @param callback can use this to provide a sort of rollback mechanism to e.g. cleanup a state
        @param callbackparams dict of parameters

        '''
        #pymonkey.q.logger.log('Starting transaction: %s' % description,5)
        if self.hasRunningTransactions()==False:
            self.originalwidth=pymonkey.q.console.width
        
        transaction = Transaction(description, errormessage, resolutionmessage,\
                        maxloglevel=maxloglevel,maxloglevelcapture=maxloglevelcapture,\
                        callback=callback,callbackparams=callbackparams,silent=silent)
        
        self.transactions.append(transaction)
        self.activeTransaction=transaction

                         
        #msg="TRANSACTION START: %s" % transaction.description
        msg="%s" % transaction.description
        if self.send2console and silent==False:
            pymonkey.q.console.echoListItem(msg)
        else:
            pymonkey.q.logger.log(msg,5)
        if silent==False:
            pymonkey.q.console.indent+=1   

    def stop(self,failed=False):
        '''
        Stop the currently running transaction

        This will get the latest started transaction from the transaction stack and
        display status
        @param failed, used when error is raised by errorconditionhanlder
        '''
        if not self.transactions:
            raise RuntimeError('[ACTIONS] Stop called while no transactionsactions are '
                                  'running at all')
        
        transaction = self.transactions.pop()
        _TransactionStatus=pymonkey.q.enumerators.TransactionStatus
        status = _TransactionStatus.DONE if not failed else _TransactionStatus.FAILED
        if not failed and not self.transactions:
            status = _TransactionStatus.FINISHED
        if transaction.silent==False:
            pymonkey.q.console.indent-=1                    
        if status==_TransactionStatus.FINISHED:
            msg="TRANSACTION %s: %s" % (string.upper(str(status)),transaction.description)
            self.activeTransaction=None
        else:
            msg="TRANSACTION %s: %s" % (string.upper(str(status)),transaction.description)
        #if self.send2console:
            #pymonkey.q.console.echoListItem(msg)
        #else:
        pymonkey.q.logger.log(msg,5)
        
    def stopall(self):
        """
        stop all transaction
        """
        for tr in self.transactions:
            self.stop()

    def clean(self):
        '''Clean the list of running actions'''
        pymonkey.q.logger.log('[ACTIONS] Clearing all actions', 5)
        self.transactions = list()


    def hasRunningTransactions(self):
        '''
        Check whether actions are currently running
        @returns: Whether actions are runnin
        '''
        return bool(self.transactions)

