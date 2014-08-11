#!/usr/bin/env python

import win32file

def main():
   #import ctypes
   ## WARNING: requires Windows XP SP2 or higher!
   #try:
   #   print ctypes.windll.shell32.IsUserAnAdmin()
   #   return
   #except:
   #   traceback.print_exc()
   #   print "Admin check failed, assuming not an admin."
   #   return False

   #======================================

   # win32file doesn't define this
   FILE_ATTRIBUTE_REPARSE_POINT = 1024

   #tPath = "D:\\Desktop\\aaa.txt"
   tPath = unicode("one")
   
   tHandle = win32file.CreateFile(
      tPath,                        # fileName
      win32file.GENERIC_READ,       # desiredAccess
      win32file.FILE_SHARE_READ ,#| win32file.FILE_SHARE_WRITE | win32file.FILE_SHARE_DELETE,    # shareMode
      None,                         # attributes
      win32file.OPEN_EXISTING,      # createDisposition
      FILE_ATTRIBUTE_REPARSE_POINT ,#| win32file.FILE_FLAG_BACKUP_SEMANTICS, (this causes problems) # flagsAndAttributes
      None)                         # hTemplateFile

if __name__ == "__main__":
   main()
