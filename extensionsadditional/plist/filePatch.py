class filePatch:
  """
  represents binary file which can be used to patch a file to become a new file
  structure of file
     1byteChangeType,8bytesPosition,8bytesNrBytesChanged,xBytesTheChangedInfo,yBytesCRCOfChangedInfo,1byteChangeType,...
  """
  
  def validatePatchFile
  
  
  def applyPatchFileOnFile(self,patchFile,FilePathToPatch):
    """
    @return the patched file
    """
  