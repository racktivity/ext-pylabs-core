from collections import deque

from pylabs import q

class CompositeIterator(object):
    def __init__(self, node):
        self.iteratorQueue = deque()
        self.build(node)
        self.current_iter = self.iteratorQueue.popleft() 
        
    def build(self, node):
        q.logger.log('building iterator for %s'%node)
        #temp solution since FileNode would can't have both __iter__ or __getitem__
        if node.isLeaf: return
        itr = iter(node) 
        self.iteratorQueue.append(itr)
        for child in node.children:
            self.build(child)
    
    def __iter__(self):
        return self
    
    def next(self):
        while not self.current_iter.hasNext():
            try:
                self.current_iter = self.iteratorQueue.popleft()
            except IndexError:
                raise StopIteration()
            
        return self.current_iter.next()    
       
class DirIterator(object):
    def __init__(self, dirNode):
        self.content = dirNode.children
        self.idx = 0
        self.path = dirNode.path
        
    def __iter__(self):
        return self
    
    def hasNext(self):
        return self.idx < len(self.content)
    
    def next(self):
        if self.hasNext():
            item = self.content[self.idx]
            self.idx += 1
            return item
        else:
            raise StopIteration()     

class DirNodeStoreCompositeIterator(object):
    def __init__(self, objectStore, startPath, recursive=True):
        self.store = objectStore
        self.startPath = startPath
        self.recursive = recursive
        self.iteratorQueue = deque()
        self.build(self.startPath)
        self.current_iter = self.iteratorQueue.popleft() 
        
    def build(self, startPath):
        node = self.store.get(startPath)
        q.logger.log('building iterator for %s'%node)
        itr = iter(node) 
        self.iteratorQueue.append(itr)
        for subdirname in sorted(node.dirs):
            if self.recursive: self.build(q.system.fs.joinPaths(startPath, subdirname))
    
    def __iter__(self):
        return self
    
    def next(self):
        while not self.current_iter.hasNext():
            try:
                self.current_iter = self.iteratorQueue.popleft()
            except IndexError, ex:
                q.logger.log(ex)
                raise StopIteration('No more queued iterators')
            
        return self.current_iter.next()
        
class NullIterator(object):
    def __iter__(self):
        return self
    
    def hasNext(self):
        return False
    
    def next(self):
        raise StopIteration()