import os, sys, random, time, filecmp, binascii, binwalk, subprocess

class mono:
    def __init__(self, filename):
        self.name = filename
        self.size = os.path.getsize(self.name)
        self.types = {}
        self.pos_bytes = 0 # For get_frags
    
    def type_finder(self, shush=True):
        try:
            for a in binwalk.scan(self.name, signature=True, quiet=shush, extract=False):
                for b in a.results:
                    self.types[f'{b.offset:06x}'] = b.description
        except FileNotFoundError:
            print("File was not found.")
        except binwalk.ModuleException as e:
            print(f"Critical failure! -> {e}")
    
    def get_frags(self):
        pass
    
    def get_whole(self, binary=0):
        '''
        Simply gets whole file into memory at once.
        WARNING: will take lots of memory probably.
        '''
        with open(self.name, 'rb') as file:
            if binary==0:
                a = binascii.hexlify(file.read())
                return list(a) # Gives int list of hexes [115, 100 ..etc
            if binary==1:
                a = binascii.hexlify(file.read())
                b = bin(int(a,16))[2:] # Gives giant string
                return [int(n) for n in str(b)]

    def debug(self):
        """
        Debug options.
        """
        # May take a bit with large files
        orig_shasum = "".join(subprocess.run(["shasum"], stdout=subprocess.PIPE, text=True, input=f'{self.name}').stdout[:-2].split())
        print(f'''\n\t[-] TITLE: {self.name}\tSIZE: {self.size} bytes
        \n\t[-] FILE SIGS: {self.types}
        \n\t[-] SHASUM: {orig_shasum}\tLEN: {len(orig_shasum)}
        \n\t[-] OS BYTE ORDER: {sys.byteorder}
        ''')