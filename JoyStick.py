import tkinter as tk


class JoyStick(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.wn_size = root.winfo_width()
        self.wn_pos = [root.winfo_rootx(), root.winfo_rooty()]
        self.radius = 110
        pad = 200
        self.canvas_range = tk.Canvas(root,
                                      bg='white',
                                      borderwidth=0,
                                      highlightthickness=0)
        range_pos = (self.wn_size-(self.radius+pad))*0.5
        range_size = (self.radius+pad)
        relsize = range_size / self.wn_size
        self.canvas_range.place(x=range_pos, y=range_pos, relwidth=relsize, relheight=relsize)
        self.create_circle(range_size // 2, range_size // 2, self.radius, self.canvas_range, None)

        self.dot = tk.Canvas(self.canvas_range,
                             bg='white',
                             borderwidth=0,
                             highlightthickness=0)
        size_ratio = 3
        dot_size = range_size / size_ratio
        self.dot_pos = (range_size-dot_size)*0.5
        self.dot.place(x=self.dot_pos, y=self.dot_pos, relwidth=1/size_ratio, relheight=1/size_ratio)
        self.create_circle(dot_size // 2, dot_size // 2, dot_size*0.8//2, self.dot, 'black')
        self.dot.bind("<Motion>", self.mouse_appearance)
        self.dot.bind("<B1-Motion>", self.drag)
        self.dot.bind("<ButtonRelease-1>", self.centralize)
        self.offset = dot_size - range_pos - dot_size*0.2*2

        self.generator = 0
        self.pressed = False
        self.increment_x = 0
        self.increment_y = 0

    @staticmethod
    def create_circle(x, y, r, canvas, fill):  # center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas.create_oval(x0, y0, x1, y1, outline='black', width=2, fill=fill)

    def drag(self, event):
        self.pressed = True
        if self.generator == 0:
            self.set_stage()
        cur_wn_pos = [root.winfo_rootx(), root.winfo_rooty()]
        if cur_wn_pos != self.wn_pos:
            self.wn_pos = cur_wn_pos
        x = event.widget.winfo_pointerx()-self.wn_pos[0]-self.offset
        y = event.widget.winfo_pointery()-self.wn_pos[1]-self.offset
        x, y = self.get_coord(x, y)
        event.widget.place(x=x, y=y)
    
    def mouse_appearance(self, event):
        self.dot.config(cursor="hand2")

    def centralize(self, event):
        self.pressed = False
        self.dot.place(x=self.dot_pos, y=self.dot_pos)

    def get_coord(self, x, y):
        delta_x = self.dot_pos-x
        delta_y = self.dot_pos-y
        radius = (delta_x**2 + delta_y**2)**0.5
        ratio = radius/self.radius
        if ratio <= 1:
            self.increment_x = (x-self.dot_pos) / self.radius
            self.increment_y = (self.dot_pos-y) / self.radius
            return x, y
        else:
            if delta_x < 0:
                edge_x = abs(delta_x/ratio) + self.dot_pos
            else:
                edge_x = self.dot_pos - (delta_x/ratio)
            if delta_y < 0:
                edge_y = abs(delta_y/ratio) + self.dot_pos
            else:
                edge_y = self.dot_pos - (delta_y/ratio)
            self.increment_x = (edge_x-self.dot_pos) / self.radius
            self.increment_y = (self.dot_pos- edge_y) / self.radius
            return edge_x, edge_y

    def set_stage(self):
        self.generator = 0
        if self.pressed:
            print((self.increment_x, self.increment_y))
            self.generator = root.after(100, self.set_stage)
        else:
            if self.generator != 0:
                root.after_cancel(generator)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("JoyStick Control")
    root.geometry('320x320')
    root.configure(bg='white')
    root.resizable(0, 0)
    root.update()
    JoyStick(root)
    root.mainloop()
