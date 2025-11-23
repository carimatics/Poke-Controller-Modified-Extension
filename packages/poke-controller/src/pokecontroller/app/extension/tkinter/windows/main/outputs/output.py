import tkinter as tk
import tkinter.ttk as ttk


class Output(ttk.Frame):
    def __init__(self, master, id, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id: int = id
        self.build_ui()

    def build_ui(self):
        labelframe = ttk.Labelframe(self,
                                    text=f"Output#{self.id}",
                                    relief=tk.GROOVE)

        # Text Area
        text_area = tk.Text(labelframe,
                            height=3,
                            width=50,
                            blockcursor=True,
                            insertunfocussed=tk.NONE,
                            undo=False,
                            maxundo=0,
                            relief=tk.FLAT,
                            state=tk.DISABLED)
        scroll = tk.Scrollbar(labelframe, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scroll.set)

        # Layout
        text_area.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=(5, 0), pady=5)
        scroll.pack(expand=False, fill=tk.Y, side=tk.LEFT, pady=5)
        labelframe.pack(expand=True, fill=tk.BOTH)
