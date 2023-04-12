"""
The netflix data module generates data frame and graph for the program.
"""
import pandas as pd
import matplotlib.pyplot as plt


class NetflixData:
    """
    Define the main data analysis class
    """
    def __init__(self):
        self.__data = pd.read_csv("NetflixOriginals.csv")
        self.data["Premiere"] = pd.to_datetime(self.data["Premiere"])

    @property
    def data(self):
        """ Get a data frame with all of the information."""
        return self.__data

    def find_list(self, column: str):
        """ Find and return column's data that have no duplicates.
        
        Parameters
        ----------
        column : column title of the data frame

        Returns
        -------
            Data frame of column's data that have no duplicates.
        """
        return pd.DataFrame(self.data[column].drop_duplicates())

    def find_data(self, data_index: list):
        """ Find and return each film's data from its index.

        Parameters
        ----------
        data_index : list of film indexes that the user wants to browse.

        Returns
        -------
            Data frame of each film's data from its index.
        """
        return pd.DataFrame(self.data.iloc[data_index])

    def graph_df(self, graph_type: str, column: list, data_index: list):
        """ Find and return data for plot graph.

        Parameters
        ----------
        graph_type : graph's type
        column : list of column title of the data frame
        data_index : list of film indexes that the user wants to browse.

        Returns
        -------
            Data frame for the graph.
        """
        if graph_type in ["Bar", "Bar (horizontal)"]:
            return pd.DataFrame(self.data[column].iloc[data_index])
        elif graph_type == "Pie":
            if column[1] == "Premiere":
                new_df = self.data[column].iloc[data_index].set_index("Premiere")
                return new_df.resample("y").count()
            else:
                return pd.DataFrame(self.data[column[1]].iloc[data_index].value_counts())
        elif graph_type == "Scatter":
            return pd.DataFrame(self.data[column].iloc[data_index])


class Graph:
    """ Define the main graph plotter class."""
    def __init__(self, data: pd.DataFrame, x=None, y=None):
        self.data = data
        self.selected_x = x
        self.selected_y = y

    def plotter(self):
        pass

class BarGraph(Graph):
    """ Define bar graph plotter class."""
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

    def plotter(self):
        graph = self.data.plot.bar(x="Title")
        plt.xticks(rotation=45)
        return graph


class PieGraph(Graph):
    """ Define pie graph plotter class."""
    def __init__(self, data: pd.DataFrame, y):
        super().__init__(data, y=y)

    def plotter(self):
        return self.data.plot.pie(y=self.selected_y, autopct="%.2f%%", legend=False, ylabel="")


class BarHGraph(Graph):
    """ Define bar (horizontal) graph plotter class."""
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

    def plotter(self):
        return self.data.plot.barh(x="Title")


class ScatterGraph(Graph):
    """ Define scatter graph plotter class."""
    def __init__(self, data: pd.DataFrame, x, y):
        super().__init__(data, x=x, y=y)

    def plotter(self):
        graph = self.data.plot.scatter(x=self.selected_x, y=self.selected_y)
        plt.xticks(rotation=45)
        return graph
