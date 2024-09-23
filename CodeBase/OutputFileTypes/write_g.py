from CodeBase.HandlerFiles.config_handler import Config_Handler
def write_G(path, CONFIG:Config_Handler):
    #
    # G code output
    #
    scale = float(sscale.get())
    xoff = float(sxoff.get())
    yoff = float(syoff.get())
    text = outfile.get()
    file = open(text, 'w')
    file.write("G90\n") # absolute positioning
    file.write("F"+sfeed.get()+"\n") # feed rate
    file.write("S"+sspindle.get()+"\n") # spindle speed
    file.write("T"+stool.get()+"\n") # tool
    file.write("M08\n") # coolant on
    file.write("M03\n") # spindle on clockwise
    for segment in range(len(path)):
        vertex = 0
        x = path[segment][vertex][X]*scale + xoff
        y = path[segment][vertex][Y]*scale + yoff
        file.write("G00X%0.4f"%x+"Y%0.4f"%y+"Z"+sztop.get()+"\n") # rapid motion
        file.write("G01Z"+szbottom.get()+"\n") # linear motion
        for vertex in range(1,len(path[segment])):
            x = path[segment][vertex][X]*scale + xoff
            y = path[segment][vertex][Y]*scale + yoff
            file.write("X%0.4f"%x+"Y%0.4f"%y+"\n")
        file.write("Z"+sztop.get()+"\n")
    file.write("M05\n") # spindle stop
    file.write("M09\n") # coolant off
    file.write("M30\n") # program end and reset
    file.close()
    print ("wrote",len(path),"G code toolpath segments to",text)