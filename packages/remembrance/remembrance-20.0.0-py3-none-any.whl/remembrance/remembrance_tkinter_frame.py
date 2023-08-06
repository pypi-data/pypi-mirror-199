import tkinter as tk
from tkinter import ttk

import re

# Need to implement
## Option to implement async with Tkinter
from .ipstat import IpStatHandler

class RemembranceApp(object):
    ipv4_regex = r'^((([1]?[1-9]?[0-9])|([2][0-4][0-9])|([2][0-5][0-5])|([1][0-9][0-9])).){3}(([1]?[1-9]?[0-9])|([2][0-4][0-9])|([2][0-5][0-5])|([1][0-9][0-9]))$'
    ipv6_regex = r'^([0-9a-fA-F]{1,4}[:]){7}[0-9a-fA-F]{1,4}$'
    
    def __init__(self, root):
        self.remembrance_frame = ttk.Frame(root, padding=10)
        self.remembrance_frame.columnconfigure(0, weight=1)
        self.remembrance_frame.rowconfigure(0, weight=1)
        
        self.search_variable = tk.StringVar()
        self.search_combobox_variable = tk.StringVar()
        self.search_combobox_values = ('All Addresses', 'Local Address', 'Remote Address', 'Port', 'State', 'Execution Name')
        self.search_variable.trace_add('write', self.filter_connections)
        
        self.data = {}
        self._iid = -1
        
        self.tree = ttk.Treeview(self.remembrance_frame)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.grid(column=0, row=0,sticky='nsew', padx=6, pady=6)
                
        self.construct()
        
        separator = ttk.Separator(self.remembrance_frame)
        separator.grid(row=2, column=0, columnspan=2, padx=(20,10), pady=(5,0), sticky="nsew")
        
        button_frame = ttk.LabelFrame(self.remembrance_frame, text="IP Options", padding=(20,10))
        button_frame.grid(row=3, column=0, columnspan=2, padx=(20,10), pady=(5,0), sticky="nsew")

        refresh_connection_btn = ttk.Button(button_frame, text="Refresh", command=self.construct)
        block_connection_btn = ttk.Button(button_frame, text="Blacklist", command=self.block_connection)
        search_connections_label = ttk.Label(button_frame, text="Filter By: ")
        search_connections_combobox = ttk.Combobox(button_frame, width = 27, textvariable = self.search_combobox_variable, values=self.search_combobox_values)
        search_connections = tk.Entry(button_frame, bd = 5, font=("Ubuntu", 16), width=20, textvariable=self.search_variable)
        
        refresh_connection_btn.grid(row=0, column=0, padx=5, pady=10)
        block_connection_btn.grid(row=0, column=1, padx=5, pady=10)
        search_connections_label.grid(row=0, column=2, padx=5, pady=10)
        search_connections_combobox.grid(row=0, column=3, padx=5, pady=10)
        search_connections.grid(row=1, column=2, columnspan=2, padx=5, pady=10)
        
    def filter_connections(self, var, index, mode):
        print ("Traced variable {}".format(self.search_variable.get()))
        
    def block_connection(self):
        pass

    def refresh(self):
        self.data.clear()
        
        for conn in IpStatHandler():
            identifier = conn.localAddr
            try:
                self.data[identifier].append(conn)
            except:
                self.data[identifier] = [conn]

    def get_new_iid(self):
        self._iid += 1

        return self._iid

    def construct(self):
        self.refresh()
        
        self.tree["columns"] = ("one", "two", "three", "four")
        #self.tree.column("one", width=10)
        self.tree.heading("one", text="Connected Port")
        #self.tree.column("two", width=50)
        self.tree.heading("two", text="State")
        #self.tree.column("three", width=50)
        self.tree.heading("three", text="PID")
        #self.tree.column("four", width=50)
        self.tree.heading("four", text="Execution Name")
        
        for key, val in sorted(self.data.items(), key = lambda x: x[0]):
            parent_key = str(key)
            parent_iid = self.get_new_iid()

            parent_identifier = self.tree.insert("", parent_iid, text=parent_key)

            for idx, child_connection in enumerate(val):
                remote_address = str(child_connection.remoteAddr)
                port = child_connection.getPort()
                state = child_connection.state
                pid = child_connection.pid
                exe_name = child_connection.exeName
                # Need to change text for hash collision
                # Test right now!!!
                try:
                    self.tree.insert(parent_identifier, "end", f'{child_connection.localAddr}', text=remote_address, values=(port, state, pid, exe_name))
                except:
                    pass

    def on_double_click(self, event):
        item = str(self.tree.selection()[0])
        
        identifier = self.tree.item(item, "text")
        
        if re.search(self.ipv4_regex, identifier) or re.search(self.ipv6_regex, identifier):
            # Then it's an IP address
            print(f"IP address {identifier}")
        else:
            # Then it's a parent identifier
            print(f"A section was selected, here is the identifier for the group {self.tree.selection()[0]}")
            
    def set_grid(self, _row: int = 0, _column: int = 0):
        self.remembrance_frame.grid(row=_row, column = _column)


if __name__ == '__main__':
    root = tk.Tk()
    # root.geometry('900x500')
    
    root.tk.call("source", "./themes/Azure-ttk-theme-main/azure.tcl")
    root.tk.call("set_theme", "dark")
    
    remembrance_frame = RemembranceApp(root)
    remembrance_frame.set_grid()
    
    root.mainloop()
