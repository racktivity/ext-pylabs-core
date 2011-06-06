import mod_difflib
from functools import partial
from collections import defaultdict

class Diff(object):

    def getSequenceMatcher(self, seq1, seq2, comparator=None):
        '''
        accepts two iterable sequences, iterators, generators, etc of arbitrary length and diff the sequences
        to use the pylabs_diff correctly, you need to invoke next installComparator(foo) on the sequenceMatcher instance you receive
        @param seq1: sequence
        @param seq2: anotherSequence
        @param comparator: an instance method form, with the signature def foo(self, other) and return True if some instance attributes are modified
        @return: difflib.SequenceMatcher
        '''
        seq_matcher = mod_difflib.SequenceMatcher(a=seq1, b=seq2)
        if comparator:
            seq_matcher.installComparator(comparator)
        return seq_matcher

    def diffSequences(self, seq_matcher, groupSimilarOperations=False, ignoreEquals=True):
        '''
        if groupSimilarOperations is False, returns a list of strings representing Transaction Log of changes between the two sequences
        else a dictionary of <action> : <list of files/dirs> based on the value of 
        @param seq1: a sequence of objects, naturally an iterator or a generator can be used as well. Note that for sequences of primitive values e.g. int the modified operation has no meaning and standard python difflib should be used in such case
        @param seq2: another sequence, iterator or generator of objects
        @param groupdSimilarOperations: modifies the format of the return value to be in dict form, with keys being the opcodes (insert, delete, equal, modified) and the values are list of objects corresponding to the operation
        @param ignoreEquals: skips the equal objects in the return report, useful for large sequences with minimal modification, e.g. file system metadata
        '''
        if groupSimilarOperations:
            return self._getActionGroups(seq_matcher, ignoreEquals=ignoreEquals)
        else:
            return self._getTLog(seq_matcher, ignoreEquals=ignoreEquals)

    def _getActionGroups(self, seq_matcher, ignoreEquals=True):
        actionGroups = defaultdict(list)
        def replace_handler(opcode_handlers, actionGroups, a, b, alo, ahi, blo, bhi):
            opcode_handlers['delete'](opcode_handlers, actionGroups, a, b, alo, ahi, blo, bhi)
            opcode_handlers['insert'](opcode_handlers, actionGroups, a, b, alo, ahi, blo, bhi)
            
        opcode_handlers = {
              'equal' : lambda opcode_handlers, actionGroups, a, b, alo, ahi, blo, bhi: actionGroups['equal'] if ignoreEquals 
              else actionGroups['equal'].extend(a[alo:ahi]),
              'delete' : lambda opcode_handlers, actionGroups, a, b, alo, ahi, blo, bhi: actionGroups['delete'].extend(a[alo:ahi]),
              'modified' : lambda opcode_handlers, actionGroups, a, b, alo, ahi, blo, bhi: actionGroups['modified'].extend(a[alo:ahi]),
              'insert' : lambda opcode_handlers, actionGroups, a, b, alo, ahi, blo, bhi: actionGroups['insert'].extend(b[blo:bhi]),
              'replace' : replace_handler
              }
            
        for opcode in seq_matcher.get_opcodes():
            opcode_handlers[opcode[0]](opcode_handlers, actionGroups, seq_matcher.a, seq_matcher.b, *opcode[1:])
        return actionGroups
            
        
    def _getTLog(self, seq_matcher, ignoreEquals=True):
        opcodes = seq_matcher.get_opcodes()
        opcode_handlers = {
              'delete' : lambda code, a, alo, ahi, b, blo, bhi: ['%s: %s\n'%(code, entry) for entry in a[alo:ahi]],
              'modified' : lambda code, a, alo, ahi, b, blo, bhi: ['%s: %s\n'%(code, entry) for entry in b[alo:ahi]],
              'insert' : lambda code, a, alo, ahi, b, blo, bhi: ['%s: %s\n'%(code, entry) for entry in b[blo:bhi]],
              'replace' : lambda code, a, alo, ahi, b, blo, bhi: ['%s: %s\n'%('delete', entry) for entry in a[alo:ahi]] + ['%s: %s\n'%('insert', entry) for entry in b[blo:bhi]],
              'equal' : lambda code, a, alo, ahi, b, blo, bhi: [] if ignoreEquals else ['%s: %s\n'%(code, entry) for entry in a[alo:ahi]]
              }
        def buildTLog(seq_matcher, opcode_handlers, prev, opcode):
            code, a_start, a_end, b_start, b_end = opcode
            return prev + opcode_handlers[code](code, seq_matcher.a, a_start, a_end, seq_matcher.b, b_start, b_end)
        
        return reduce(partial(buildTLog, seq_matcher, opcode_handlers), opcodes, [])

