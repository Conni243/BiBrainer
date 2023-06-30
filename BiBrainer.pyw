from tkinter.filedialog import askopenfilename
from tkinter import messagebox, simpledialog
import tkinter as tk
import json as js
import webbrowser


#If you try to takes this source code go ahead im not stopping you, but be warned 


filepath = None         #initialize constant values
json = None


def openhyper(why):     #opens the Bibite cheat sheet
    webbrowser.open_new("https://drive.google.com/file/d/1-6AyPj3MMdWPcam4Uq-2ofupDO9vKrZP/view")



def addnode(widget):    #is used for adding new neurons
    global json
    neuronname = simpledialog.askstring(title="Name Neuron", prompt="What should the neuron be called?")
    widget.insert(widget.size(), str(len(json["brain"]["Nodes"])) + ": " + str(neuronname))
    nodemode = simpledialog.askinteger(title="Set the Neuron's mode", prompt="Choose from one of the modes 2-7 (1 is reserved for Input Neurons)") - 1
    if(nodemode < 1 | nodemode > 10):
        messagebox.showerror('Invalid Neuron!', 'Not a valid Neuron function, defaulting to 1')
        nodemode = 1
    newnode = {
        "Type": nodemode,
        "TypeName": "Doesn't Matter anyways!",
        "Index": len(json["brain"]["Nodes"]),
        "Inov": 0,
        "Desc": neuronname,
        "Value": 0,
        "LastInput": 0.0,
        "LastOutput": 0.0
      }
    json["brain"]["Nodes"].append(newnode)


def addsynapse(widget):     #is used for adding new synapses
    global json
    syninput = simpledialog.askinteger(title="Input for Synapse", prompt="What should the Synapses input Neuron be?")
    synout = simpledialog.askinteger(title="Output for Synapse", prompt="What should the Synapses output Neuron be?")
    synweight = simpledialog.askfloat(title="Weight of Synapse", prompt="What should the Synapses weight be?")
    synen = messagebox.askyesno(title="Enabled?",message="Should the Synapse be enabled?")
    widget.insert(widget.size(),"Synapse: " + "From: " + str(syninput) + " To: " + str(synout) + " Weight: " + str(synweight))
    newsyn = {
        'Inov': 0, 
        'NodeIn': syninput, 
        'NodeOut': synout, 
        'Weight': synweight, 
        'En': synen
      }
    json["brain"]["Synapses"].append(newsyn)
    drawcanvas()

def removesyn(widget):      #is used for removing synapses
    global json
    for item in widget.curselection():
        json["brain"]["Synapses"].pop(item)
    widget.delete(widget.curselection())
    drawcanvas()
def removeneuron(widget):   #is used for removing neurons
    global json
    try:
        for item in widget.curselection():
            index = int(widget.get(item).split(":")[0])
            json["brain"]["Nodes"].pop(index)
        widget.delete(widget.curselection())
    except Exception:
        pass




def returnallobjectsinlistdict(list, objectname):       #implementation for returing a list of all n inside lists inside of a list (pretty stupid i know)
    returnlist = []
    for element in list:
        returnlist.append(str(element["Index"]) + ": " + element[objectname])
    return returnlist


def _create_circle(self, x, y, r, **kwargs):            #so i can actually draw circles not ovals
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle                #Monkey patching

def openfile():                                         #used for opening a Bibite File  
    global filepath
    global json
    filepath = askopenfilename(filetypes=(
        ('Bibite files', '*.bb8'),
        ('All files', '*.*')
    ))
    try:
        with open(filepath, "r") as file:
            json = js.load(file)
    except Exception:
        messagebox.showerror('Couldn\'t open!', 'BiBrainer has failed to open this file. if you think this is a bug please report this (and steps to reproduce) to the Creator!')

def savebibite():                                       #used for saving a Bibite File
    global json
    global filepath
    with open(filepath, "w") as file:
        js.dump(json, file)
        exit()


def drawcanvas():                                       #Draws the entire Neuron layout on the screen
    global canvas
    canvas.delete("all")
    global json
    allusedneurons = []
    allusedneuronsout = []
    for element in json["brain"]["Synapses"]:
        used = False
        for f in allusedneurons:
            if f["Index"] == json["brain"]["Nodes"][element["NodeIn"]]["Index"]:
                used = True
        if(used == False):
            allusedneurons.append(json["brain"]["Nodes"][element["NodeIn"]])
    for element in json["brain"]["Synapses"]:
        used = False
        for f in allusedneuronsout:
            if f["Index"] == json["brain"]["Nodes"][element["NodeOut"]]["Index"]:
                used = True
        if(used == False):
            allusedneuronsout.append(json["brain"]["Nodes"][element["NodeOut"]])

    size = 200 / len(allusedneurons)
    inputspacing = size + 5
    sizeout = 200 / len(allusedneuronsout)
    inputspacingout = sizeout + 5
    x1, x2, y1, y2 = 0,0,0,0
    for element in json["brain"]["Synapses"]:
        i = 1
        for ins in allusedneurons:
            if(ins["Index"] == element["NodeIn"]):
                x1 = size + 30
                y1 = inputspacing + 500/len(allusedneurons)*i - 500/len(allusedneurons)
            i += 1
        i = 1
        for insout in allusedneuronsout:
            if(insout["Index"] == element["NodeOut"]):
                x2 = 870 - sizeout
                y2 = inputspacingout + 500/len(allusedneuronsout)*i - 500/len(allusedneuronsout)
            i += 1
        if element["En"] == True:
            canvas.create_line(x1,y1,x2,y2, fill="red", width=5)
        else:  
            canvas.create_line(x1,y1,x2,y2, fill="#808080", width=5)      
        midpoint = (x1+ x2 * 0.333333)/1.3333333, (y1 + y2 * 0.3333333)/1.3333333 -8
        canvas.create_text(midpoint, text=element["Weight"])
        x1, x2, y1, y2 = 0,0,0,0


    for element in allusedneurons:
        canvas.create_circle(size + 30, inputspacing, size, fill="green", outline="#000", width=1)
        canvas.create_text(size + 30, inputspacing, text=str(element["Index"]) + ": " + element["Desc"])
        inputspacing += 500/len(allusedneurons)

    for element in allusedneuronsout:
        canvas.create_circle(870 - sizeout, inputspacingout, sizeout, fill="green", outline="#000", width=1)
        canvas.create_text(870 - sizeout, inputspacingout, text=str(element["Index"]) + ": " + element["Desc"])
        inputspacingout += 500/len(allusedneuronsout)


def main():                                 #create the tkinter window(and a bunch of other stuff im too lazy to explain)
    global canvas
    global json
    window = tk.Tk()
    window.title("BiBrainer")
    openfile()
    
    synlist = tk.Listbox(
        window,
        listvariable=None,
        height=14,
        width=33,
        selectmode='browse')
    synlist.grid(row=1,column=2)
    nodes = tk.StringVar(value=returnallobjectsinlistdict(json["brain"]["Nodes"][:48], "Desc"))
    nodes2 = tk.StringVar(value=returnallobjectsinlistdict(json["brain"]["Nodes"][48:], "Desc"))
    for element in json["brain"]["Synapses"]:
        synlist.insert(synlist.size(),"Synapse: " + "From: " + str(element["NodeIn"]) + " To: " + str(element["NodeOut"]) + " Weight: " + str(element["Weight"]))
    neurons = tk.Label(window, text="Input and Output Neurons")
    neurons.grid(row=0,column=0)
    syn = tk.Label(window, text="Synapses")
    syn.grid(row=0,column=1)

    nodelist = tk.Listbox(
        window,
        listvariable=nodes,
        height=14,
        width=33,
        selectmode='multiple')
    nodelist2 = tk.Listbox(
        window,
        listvariable=nodes2,
        height=14,
        width=33,
        selectmode='browse')
    nodelist.grid(column=0,row=1)
    hiddentips = tk.Label(window, text="Need Help?: " + "\nhttps://drive.google.com/file/d/1-6AyPj3MMdWPcam4Uq-2ofupDO9vKrZP/view", fg="blue", cursor="hand2")
    hiddentips.grid(row=4,column=2)
    hiddentips.bind("<Button-1>",openhyper)
    hidden = tk.Label(window, text="Hidden Neurons")
    hidden.grid(row=3,column=0)
    nodelist2.grid(column=0,row=4)


    addbutton = tk.Button(window, text="Add Neuron", command=lambda: addnode(nodelist2))
    addbutton.grid(column=0,row=5)
    addbutton = tk.Button(window, text="Remove selected Synapse", command=lambda: removesyn(synlist))
    addbutton.grid(column=2,row=3)
    addsybutton = tk.Button(window, text="Add Synapse", command=lambda: addsynapse(synlist))
    addsybutton.grid(column=2,row=2)
    addbutton = tk.Button(window, text="Remove selected Neuron", command=lambda: removeneuron(nodelist2))
    addbutton.grid(column=0,row=6)
    savebutton = tk.Button(window, text="Save Bibite", command=savebibite)
    savebutton.grid(column=1,row=0)

    canvas = tk.Canvas(window, width=900,height=500)
    canvas.grid(row=1,column=1,rowspan=5)
    drawcanvas()

    window.mainloop()


if __name__ == '__main__': # make sure its not used as a library (as if anybody's going to do that anyways)
    main()

    
