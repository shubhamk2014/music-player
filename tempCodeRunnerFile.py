
    # get_pos returns time in millisec ,converting it to sec by dvidin with 1000
    current_pos = mixer.music.get_pos()/1000
    # converting time in the sec into format %M:%S
    converted_pos = strftime("%M:%S", gmtime(current_pos))
    # updating label with converted time
    dur_lbl.config(text=converted_pos)
    # for getting the position of the song every sec run the function every sec
    dur_lbl.after(1000, duration)