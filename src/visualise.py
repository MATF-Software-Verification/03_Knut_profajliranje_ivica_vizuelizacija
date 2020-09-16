import tkinter as tk
from main import activate

windowWidth = 750
windowHeight = 400


def getInstructionsText(block):
    text = ""
    for instr in block.get_instructions():
        text += str(instr)
        text += '\n'
    return text

class mainWindow:
    def __init__(self, root):
        self.root = root
        self.codeText= self.setCodeText()
        self.errorLabel = tk.Label(root, fg='red', justify=tk.LEFT)

        self.codeText.update()
        codeTextWidth = self.codeText.winfo_width()
        
        btn = tk.Button(root, text="Submit code", command=(lambda: self.submitData()))
        btn.place(x=20+codeTextWidth, rely=10/windowHeight)

        # Set clear button
        btn = tk.Button(root, text="Clear code", command=(lambda: self.clear()))
        btn.place(x=20+codeTextWidth, rely=50/windowHeight)

        btn = tk.Button(root, text="Generate canvas", command=(lambda: self.openNewWindow()))
        btn.place(x=20+codeTextWidth, rely=90/windowHeight)

    def clear(self):
        self.codeText.delete('1.0', tk.END)
        self.errorLabel.place_forget()
    
    def setCodeText(self):
        # setup the text input
        numOfLines = 80
        codeText = tk.Text(self.root, width=numOfLines)
        scroll = tk.Scrollbar(self.root, command=codeText.yview)
        codeText.configure(yscrollcommand=scroll.set)
        codeText.place(relx=10/windowWidth, rely=10/windowHeight)
        return codeText

    def openNewWindow(self): 
      
        newWindow = tk.Toplevel() 
        newWindow.title("New Window") 
        newWindow.geometry("1200x1200") 
        canvas = tk.Canvas(newWindow, bg="gray", height=1200, width=1200)
        for i in range(0,len(self.blocks)):
            instructionsText = getInstructionsText(self.blocks[i])
            text = canvas.create_text((40, 40), text=instructionsText)
            rentacle = canvas.create_rectangle(0, 0, 150, 150, outline="black", fill="#1f1", width=2)
            canvas.move(rentacle, 20+ int(i) * 100, 20 + int(i) * 100)
            canvas.move(text,20+ int(i) * 100, 20 + int(i) * 100 )
            canvas.tag_raise(text)


        #canvas.create_rectangle(0, 0, 300, 300, outline="#f11", fill="#1f1", width=2)
        #canvas.create_text(100,10,fill="darkblue",font="Times 9 bold",
        #                text="Click the bubbles that are multiples of two.")
        canvas.pack()
  

    def submitData(self):
        input = self.codeText.get("1.0",'end-1c')
        codeTextWidth = self.codeText.winfo_width()
        try:
            blocks = activate(input)
        except Exception as e:
            self.errorLabel['text'] = "Syntax error: \n" + str(e)
            self.errorLabel.place(x=20+codeTextWidth, rely=100/windowHeight)
            return

        self.codeText.delete('1.0', tk.END)
        for block in blocks:
            self.codeText.insert(tk.END, block.stringify_block())
            self.codeText.insert(tk.END, "\n")
        self.errorLabel.place_forget()

        self.blocks = blocks



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(str(windowWidth) + 'x' + str(windowHeight))
    app = mainWindow(root)
    app.root.title("Knutov algoritam")
    root.mainloop()

