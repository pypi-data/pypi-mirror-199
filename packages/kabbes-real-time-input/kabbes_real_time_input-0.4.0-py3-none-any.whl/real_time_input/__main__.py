import real_time_input

RTI = real_time_input.Client()   
#RTI.cfg_rti.print_atts()

print ('Type to add words to your selection: ')
RTI.get_multiple_inputs()
print ()
print ('Selections: ' + str(RTI.selections))
print ('Final Input: ' + RTI.string)