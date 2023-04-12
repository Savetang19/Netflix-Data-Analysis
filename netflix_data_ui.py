"""
The netflix_data_ui module is responsible for the program's graphical output.
"""
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandastable import Table
from netflix_data import *


class App(tk.Tk):
    """
    Define the main user interface class.
    """
    def __init__(self, netflixdata: NetflixData):
        super().__init__()
        self.netflix = netflixdata
        self.data = netflixdata.data
        self.df_for_table = self.data
        self.df_for_graph = None
        self.table_frame = ttk.LabelFrame(self, text="Table output")
        self.menu_frame = ttk.LabelFrame(self, text="Menu")
        self.selected_column = tk.StringVar()
        self.number = tk.StringVar()
        self.selected_graph = tk.StringVar()
        self.selected_data = tk.StringVar()
        self.scatter_x = tk.StringVar()
        self.scatter_y = tk.StringVar()
        self.graph = None
        self.options = {"padx": 5, "pady": 5, "sticky": tk.EW}
        self.init_components()
        self.update_table()

    def init_components(self):
        """ Create components and layout."""
        self.title("Netflix Originals Data Analysis")
        self.geometry("1200x675")
        self.resizable(False, False)
        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.columnconfigure(1, weight=1)
        self.menu()

        # set frames position.
        self.table_frame.pack(fill="both", expand=True, side="left")
        self.menu_frame.pack(fill="both", expand=True, side="right")

    def update_table(self):
        """ Update the table data and display the changes."""
        self.table = Table(self.table_frame, dataframe=self.df_for_table, showstatusbar=True)
        self.table.editable = False
        self.table.show()

    def menu(self):
        """ Create a menu button allowing the user to select what they want."""
        menu_button = ttk.Menubutton(self.menu_frame, text="Select menu")
        menu_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        menu_list = tk.Menu(menu_button, tearoff=0)
        menu_button["menu"] = menu_list
        menu_list.add_command(label="Data in column", command=self.data_in_column)
        menu_list.add_command(label="Browse data", command=self.browse_data)
        menu_list.add_command(label="Plot graph", command=self.plot_graph)
        menu_list.add_separator()
        menu_list.add_command(label="Exit", command=self.quit)

    def data_in_column(self):
        """ Create UI that allows users to browse each column's data."""
        self.clear_menu_frame()
        message = ttk.Label(self.menu_frame, text="Which column would you like to select?", font=("Monospace", 15))
        column_cb = ttk.Combobox(self.menu_frame, textvariable=self.selected_column)
        column_list = [col for col in self.data.columns]
        column_cb["values"] = column_list
        column_cb["state"] = "readonly"

        # update table by tracing the variable
        self.selected_column.trace("w", lambda *args: self.set_df_table(self.selected_column))
        reset_butt = self.reset_button()

        # set UI components
        message.grid(row=1, column=0, columns=2, **self.options)
        column_cb.grid(row=2, column=0, columns=2, **self.options)
        reset_butt.grid(row=3, column=1, columns=2, **self.options)

    def set_df_table(self, variable: tk.StringVar):
        """ Set the data frame for the table based on the user's selection
        and update it.
        """
        self.df_for_table = self.netflix.find_list(variable.get())
        self.update_table()

    def browse_data(self):
        """ Create UI that allows users to browse about film's data."""
        self.clear_menu_frame()
        message = ttk.Label(self.menu_frame,
                            text="Which titel's number(s) do you want to browse? ex.1,2,3,4 or 1-9",
                            font=("Monospace", 15))
        num_entry = ttk.Entry(self.menu_frame, textvariable=self.number)
        show_butt = self.show_button(self.set_df_browse_data)
        reset_butt = self.reset_button()

        # set UI components
        message.grid(row=1, column=0, columns=2, **self.options)
        num_entry.grid(row=2, column=0, columns=2, **self.options)
        reset_butt.grid(row=3, column=1, columns=2, **self.options)
        show_butt.grid(row=3, column=0, **self.options)

    def set_df_browse_data(self):
        """ Set the data frame for the table based on the user's selection
        and update it.
        """
        # check whether the input is a number or not.
        try:
            if self.number.get().isdigit():
                self.df_for_table = self.netflix.find_data([int(self.number.get()) - 1])
                self.update_table()
            elif "," in self.number.get():
                num_list = [int(num) - 1 for num in self.number.get().split(",")]
                self.df_for_table = self.netflix.find_data(num_list)
                self.update_table()
            elif "-" in self.number.get():
                user_input = self.number.get().split("-")
                num_list = list(range(int(user_input[0]) - 1, int(user_input[1])))
                self.df_for_table = self.netflix.find_data(num_list)
                self.update_table()
            else:
                self.show_all()
        except:
            self.show_all()

    def plot_graph(self):
        """Create a UI that allows users to select the data they want to visualize."""
        self.clear_menu_frame()
        self.show_all()
        message = ttk.Label(self.menu_frame, text="Chose graph type.", font=("Monospace", 15))
        graph_cb = ttk.Combobox(self.menu_frame, textvariable=self.selected_graph)
        graph_cb["values"] = ["Bar", "Bar (horizontal)", "Pie", "Scatter"]
        graph_cb["state"] = "readonly"

        # update UI by tracing variable
        self.selected_graph.trace("w", lambda *args: self.select_graph_data(self.selected_graph))

        # set UI components
        message.grid(row=1, column=0, columns=2, **self.options)
        graph_cb.grid(row=2, column=0, columns=2, **self.options)

    def select_graph_data(self, variable: tk.StringVar):
        """ Update UI for the 'plot graph' command"""
        if variable.get() in ["Bar", "Bar (horizontal)"]:
            self.input_graph_data(["Runtime", "IMDB Score"])
        elif variable.get() == "Pie":
            self.input_graph_data(["Genre", "Premiere", "Runtime", "IMDB Score", "Language"])
        elif variable.get() == "Scatter":
            self.scatter_data()

    def input_graph_data(self, cb_values: list):
        """ Create UI components that allow the user to select graph data.
        This is valid for bar, bar (horizontal), and pie graphs.

        Parameters
        ----------
        cb_values : List of combobox values.
        """
        self.number.set("")
        self.selected_data.set("")
        graph_data = ttk.Label(self.menu_frame, text="What do you want to plot?:", font=("Monospace", 15))
        graph_data_cb = ttk.Combobox(self.menu_frame, textvariable=self.selected_data)
        graph_data_cb["values"] = cb_values
        graph_data_cb["state"] = "readonly"
        self.input_number()

        # set UI components
        graph_data.grid(row=3, column=0, columns=2, **self.options)
        graph_data_cb.grid(row=4, column=0, columns=2, **self.options)

    def scatter_data(self):
        """Create UI components that allow the user to select graph data.
        This is only valid for scatter graphs.
        """
        self.number.set("")
        self.scatter_x.set("")
        self.scatter_y.set("")
        graph_data = ttk.Label(self.menu_frame,
                               text="What do you want to plot? (x,y axis):",
                               font=("Monospace", 15))
        x_axis = ttk.Combobox(self.menu_frame, textvariable=self.scatter_x)
        x_axis["values"] = ["Title", "Genre", "Premiere", "Runtime",
                            "IMDB Score", "Language"]
        x_axis["state"] = "readonly"
        y_axis = ttk.Combobox(self.menu_frame, textvariable=self.scatter_y)
        y_axis["values"] = ["Premiere", "Runtime", "IMDB Score"]
        y_axis["state"] = "readonly"
        self.input_number()

        # set UI components
        graph_data.grid(row=3, column=0, columns=2, **self.options)
        x_axis.grid(row=4, column=0, columns=1, **self.options)
        y_axis.grid(row=4, column=1, columns=1, **self.options)

    def input_number(self):
        """ Create UI components that allow users to input film numbers."""
        message = ttk.Label(self.menu_frame,
                            text=f"Which Title's number(s) do you want to plot? ex.1,2,3,4 or 1-9",
                            font=("Monospace", 15))
        num_entry = ttk.Entry(self.menu_frame, textvariable=self.number)
        show_butt = self.show_button(self.set_graph_df)
        reset_butt = self.reset_button()
        message.grid(row=5, column=0, columns=2, **self.options)
        num_entry.grid(row=6, column=0, columns=2, **self.options)
        reset_butt.grid(row=7, column=1, columns=2, **self.options)
        show_butt.grid(row=7, column=0, **self.options)

    def set_graph_df(self):
        """ Set the data frame for graph and table."""
        # create graph frame as 'Toplevel' frame
        self.graph_frame = tk.Toplevel(self)
        self.graph_frame.title("Graph output")

        graph_type = self.selected_graph.get()
        data_column = []
        # determine the type of graph to create a list of columns
        if graph_type in ["Bar", "Bar (horizontal)", "Pie"]:
            data_column = ["Title", self.selected_data.get()]
        elif graph_type == "Scatter":
            data_column = [self.scatter_x.get(), self.scatter_y.get()]

        # check whether the input is a number or not.
        try:
            if "," in self.number.get():
                num_list = [int(num) - 1 for num in self.number.get().split(",")]
                self.df_for_graph = self.netflix.graph_df(graph_type, data_column, num_list)
                self.df_for_table = self.df_for_graph
                self.update_table()
                self.show_graph()
            elif "-" in self.number.get():
                user_input = self.number.get().split("-")
                num_list = list(range(int(user_input[0]) - 1, int(user_input[1])))
                self.df_for_graph = self.netflix.graph_df(graph_type, data_column, num_list)
                self.df_for_table = self.df_for_graph
                self.update_table()
                self.show_graph()
            else:
                self.show_all()
        except:
            self.show_all()

    def show_all(self):
        """ Update the data frame to default."""
        self.number.set("")
        self.table = Table(self.table_frame, dataframe=self.data, showstatusbar=True)
        self.table.editable = False
        self.table.show()

    def show_button(self, cmd):
        """ Create button to for show data.

        Parameters
        ----------
        cmd : command for the button.

        Returns
        -------
            Button object.
        """
        return ttk.Button(self.menu_frame, text="Click to show", command=cmd)

    def reset_button(self):
        """ Create button to for reset data.

        Returns
        -------
            Button object.
        """
        return ttk.Button(self.menu_frame, text="Click to reset", command=self.show_all)

    def graph_plotter(self):
        """ Plot the graph."""
        graph_type = self.selected_graph.get()
        if graph_type == "Bar":
            self.graph = BarGraph(self.df_for_graph).plotter()
        elif graph_type == "Bar (horizontal)":
            self.graph = BarHGraph(self.df_for_graph).plotter()
        elif graph_type == "Pie":
            if self.selected_data.get() == "Premiere":
                self.graph = PieGraph(self.df_for_graph, "Title").plotter()
            else:
                self.graph = PieGraph(self.df_for_graph,  self.selected_data.get()).plotter()
        elif graph_type == "Scatter":
            self.graph = ScatterGraph(self.df_for_graph, self.scatter_x.get(), self.scatter_y.get()).plotter()

    def show_graph(self):
        """ Place the graph in the frame."""
        self.graph_plotter()
        self.fig_canvas = FigureCanvasTkAgg(self.graph.get_figure(), master=self.graph_frame)
        self.fig_canvas.get_tk_widget().grid(row=0, column=0, columns=1, rows=1, padx=5, pady=5, sticky=tk.NSEW)
        self.graph_frame.columnconfigure(0, weight=1)
        self.graph_frame.rowconfigure(0, weight=1)
        self.graph_frame.tkraise(self)  # raise frame to the top

    def clear_menu_frame(self):
        """ Remove all widgets from the menu frame."""
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        self.menu()

    def run(self):
        """Run all the event."""
        self.mainloop()
