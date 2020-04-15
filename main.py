import atlas, sys, os, binascii, random, subprocess, time

def stage(subj, m=1):
    '''
    Staging for work.
    '''
    if subj.f_size[1] > 500:
        data = subj.f_frags()
        # TODO: Other stuff here?
    elif subj.f_size[1] <= 500:
        data = subj.f_whole(binary=m)

    core = atlas.data_c(data) # Create the data object

    core.d_shred(micro=m) # Shred data
    
    core.d_data = core.d_convert_i2s(core.d_data)
    core.d_data = core.d_assemble(d=core.d_data,binary=m)
    core.d_save(foldername=subj.f_name, filetype=subj.f_extsn, session=subj.f_session)

def main(file):
    subj = atlas.file_c(file) # Create object
    subj.f_folder() # Make folder
    argtype = sys.argv[1]
    # Check if it has the right args
    # TODO: -b should have number of bits -c should have percent
    if argtype != '-b' and argtype != '-c':
        print("\n\tNo good args: brute [-b] nor careful [-c] options chosen.\n")
        sys.exit(1)
    stage(subj, m=1)
    # Debug
    try:
        if sys.argv[3] and sys.argv[3] == '-d':
            subj.f_debug()
    except (IndexError, ValueError) as e:
        print(f'{e} | {e.args}')

if __name__ == "__main__":
    try:
        a = sys.argv[1]
    except IndexError:
        print("Options: [-b -c] brute, careful , [filename]")
        sys.exit(0)
    try:
        a = sys.argv[2]
        os.path.isfile(a)
    except (IndexError, FileNotFoundError) as e:
        print(f'{e} | {e.args}')
        sys.exit(0)

    main(sys.argv[2])