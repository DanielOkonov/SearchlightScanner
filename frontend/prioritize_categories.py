import tkinter as tk

class DraggableListbox(tk.Listbox):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind('<Button-1>', self._setCurrent)
        self.bind('<B1-Motion>', self._shiftSelection)
        self.curIndex = None

    def _setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def _shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i
        self.master.update_target_order()  # Update target order in the main application