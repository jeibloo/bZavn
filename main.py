import atlas, sys, os, binascii, random, subprocess, time

def work(data, file, flips, i, hb_type=1):
    for x in range(0, i):
        core = atlas.data_c(data)
        # Shred data
        core.d_shred(bitflips=flips, hb_type=hb_type)
        # Convert list
        core.d_data = core.d_convert_i2s(core.d_data)   
        # Convert format; if option == 0 then hex else binary passed in
        core.d_data = core.d_assemble(d=core.d_data, hb_type=hb_type)
        # Save file to folder
        core.d_save(foldername=file.f_name, count=x, 
                    filetype=file.f_extsn, session=file.f_session)
        # Idk if needed...
        del core

def main(file, mesg, arg_dict):
    '''
    Execute the work and get down etc.
    '''
    con = atlas.file_c(file)   # Create object
    con.f_folder()             # Make folder
    # TODO: Execute work but with the fragmented data and then append etc
    work(
        data=con.f_whole(hb_type=1),    # Load data in
        file=con,                       # Attack file to function
        flips=int(arg_dict['msr_at']),  # Set amount of flips/slides
        hb_type=1,                      # Set if binary or hex type
        i=int(arg_dict['atk_it'])       # Set amount of iterations
        )

    # DEBUG
    if sys.argv and sys.argv[-1] == '-d':
        con.f_debug()
    
    # FILE HOCKEY!
    return con.f_name

if __name__ == "__main__":
    mesg = '\nUsage:\n [-s] shred, <iterations>, [-b] bits <number> | [-p] percentage <number>, [filename]'
    file = 0
    # SET DEBUG MODE & CHECK if file exists
    try:
        if len(sys.argv) == 7:
            file = sys.argv[-2]
            print(f'DEBUG:\n {sys.argv} | {len(sys.argv)}')
        else:
            file = sys.argv[-1]
    except FileNotFoundError:
        print(usg_msg+' ....\n')
        sys.exit(1) 

    # Attack type; Attack Iterations
    # Measurement of Attack type; Measurement Actual
    arg_dict = {'atk_tp' : sys.argv[1],
                'atk_it' : sys.argv[2],
                'msr_tp' : sys.argv[3],
                'msr_at' : sys.argv[4]}

    # CHECK args 
    if (
            arg_dict['atk_tp'] != '-s' and isinstance(arg_dict['atk_it'], int) and 
            arg_dict['msr_tp'] != '-b' and arg_dict['msr_tp'] != '-p' and 
            isinstance(arg_dict['msr_at'], int) and len(sys.argv) <= 5
        ):
        print(usg_msg+' .\n')
        sys.exit(1)

    main(file=file, mesg=mesg, arg_dict=arg_dict)