import amorph, sys, os, binascii, random, subprocess, time

def mal_filesave(d, foldername):
    with open(os.path.join(foldername,'A_'+str(int(time.time()))),'wb') as f:
        f.write(d)

def offering(filename):
    '''
    Gives corrupted file to apropos program and stores error message.
    '''
    pass

def bit_assemble(d):
    '''
    Takes a string of 1's and 0's and converts it using int(x,2).to_bytes
    '''
    # Accidentally made byteorder little lmao
    convert_data = int(d,2).to_bytes(len(d)//8, byteorder='big')
    return convert_data

def hex_assemble(d):
    return binascii.unhexlify(data)

def folder(name="unknown", title="roman", cleanup=1):
    fulltitle = name+'_'+title
    if cleanup==0:
        try:
            os.mkdir(fulltitle)
        except FileExistsError:
            print(f"\t[-] Folder already exists.")
        except OSError as e:
            print(f"\t[-] Folder creation failed -> {e}")
    elif cleanup==1:
        try:
            os.rmdir(fulltitle)
            print(f"\n\t[-] Deleted {fulltitle}")
        except FileNotFoundError:
            print(f"\t[-] Folder doesn't exist!")
        except OSError as e:
            print(f"\t[-] Folder deletion failed -> {e}")
    return fulltitle

def brutus(s, bitflips=100, micro=1):
    '''
    Absolute calamity. Take every X amount of bits and poke holes. Will
    undoubtedly cause crashes to the programs involved.
    - Does not use the type_finder method, doesn't care about the file
    whatsoever so who cares.
    '''

    # Make directory filename_brutus to store malformed files
    foldertitle = folder(name=s.name,title="brutus", cleanup=0)

    # Get chunks or whole data
    # TODO: Apply logic to this, refactor even; logic being .get_whole and .get_frag logic branch
    data = s.get_whole(binary=micro)
    data_len = len(data)

    # Bitflips is how many bits we shall flip
    for n in range(0, bitflips):
        # Location to prick
        pin = random.randrange(0, data_len)
        if micro==1:
            # Let the pinpricking begin
            if data[pin] == 0:
                data[pin] = 1
            else:
                data[pin] = 0
        if micro==0:
            # Let the shuffle begin
            pass

    # Convert from ints to characters
    str_data = [str(t) for t in data]
    # Join them to make one long string
    com_str_data = "".join(str_data)
    # Assemble it
    assem_data = bit_assemble(d=com_str_data)
    mal_filesave(assem_data, foldername=foldertitle)
    print("\n\t[*] MUTATED brutally")

def cassius(s):
    '''
    Carefully examining headers, being sure to not mess with things that
    can easily crash the programs involved. Non-chaotic. Intelligent fuzzing.
    - Uses relevant smart methods.
    '''
    print("\n\t[*] MUTATED carefully")

def main(file):
    subject = amorph.mono(file) # Create object
    argtype = sys.argv[1]
    if argtype == '-b':
        brutus(subject, micro=1)
    elif argtype == '-c':
        subject.type_finder() # File signatures search
        cassius(subject)
    else:
        raise ValueError("Brute [-b] nor careful [-c] options chosen.")
    try:
        if sys.argv[3] and sys.argv[3] == '-d':
            subject.debug()
    except IndexError:
        pass
    except ValueError:
        print("Erroneous value.")

if __name__ == "__main__":
    try:
        a = sys.argv[1]
    except IndexError:
        print("Options: [-b -c] brute, careful , [filename]")
        sys.exit(0)
    try:
        a = sys.argv[2]
        os.path.isfile(a)
    except IndexError as e:
        print(f"No filename argument provided -> {e}")
        sys.exit(0)
    except FileNotFoundError:
        print(f"No file {sys.argv[2]} found.")
        sys.exit(0)

    main(sys.argv[2])