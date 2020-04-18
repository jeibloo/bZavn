import atlas, sys, os, binascii, random, subprocess, time

def work(data, file, cmd, flips, i, hb_type=1):
    for x in range(0, i):
        core = atlas.data_c(data)
        # Shred data
        core.d_shred(bitflips=flips, hb_type=hb_type)
        # Convert list
        core.d_data = core.d_convert_i2s(core.d_data)   
        # Convert format; if option == 0 then hex else binary passed in
        core.d_data = core.d_assemble(d=core.d_data, hb_type=hb_type)
        # Save file to folder
        w_file = core.d_save(foldername=file.f_name, count=x, 
                    filetype=file.f_extsn, session=file.f_session)
        if cmd:
            try:
                # Check if file crashes program
                p = subprocess.Popen([cmd, os.path.abspath(f'{file.f_name}/{w_file}')],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
                error = p.communicate()
                # TODO: requires some multiprocessing or something to use
                # TODO: without sleep for some programs
                time.sleep(2)
                if p.returncode != 0:
                    # TODO: Save output?
                    print(f'RETURNCODE:{p.returncode}\nERROR:{error}')
                else:
                    # Delete file if it doesn't crash given program
                    core.d_delete(foldername=file.f_name, filename=w_file)
            except BaseException as e:
                print(f'{e}')

        # Delete object
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
        cmd=arg_dict['cmd_nm'],         # Command to pass malformed files
        flips=int(arg_dict['msr_at']),  # Set amount of flips/slides
        hb_type=1,                      # Set if binary or hex type
        i=int(arg_dict['atk_it'])       # Set amount of iterations
        )

    # DEBUG
    if sys.argv and sys.argv[-1] == '-d':
        con.f_debug()

if __name__ == "__main__":
    mesg = '\nUsage:\n [-s] shred, <iterations>, \n [-b] bits <number> | [-p] percentage <number>, [filename], [command to pass in]'
    file = 0
    # SET DEBUG MODE & CHECK if file exists
    try:
        if len(sys.argv) == 8:
            file = sys.argv[-3]
            print(f'DEBUG:\n {sys.argv} | {len(sys.argv)}')
        else:
            file = sys.argv[-2]
    except FileNotFoundError:
        print(mesg)
        sys.exit(1) 

    # Attack type; Attack Iterations
    # Measurement of Attack type; Measurement Actual
    # Command to pass
    try:
        arg_dict = {'atk_tp' : sys.argv[1],
                    'atk_it' : sys.argv[2],
                    'msr_tp' : sys.argv[3],
                    'msr_at' : sys.argv[4],
                    'cmd_nm' : sys.argv[6]}
    except IndexError as e:
        print(mesg+e)
        sys.exit(1) 

    # CHECK args 
    if (
            arg_dict['atk_tp'] != '-s' and isinstance(arg_dict['atk_it'], int) and 
            arg_dict['msr_tp'] != '-b' and arg_dict['msr_tp'] != '-p' and 
            arg_dict['cmd_nm'] and isinstance(arg_dict['msr_at'], int) and 
            len(sys.argv) <= 5
        ):
        print(mesg)
        sys.exit(1)

    main(file=file, mesg=mesg, arg_dict=arg_dict)