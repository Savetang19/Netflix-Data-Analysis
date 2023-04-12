from netflix_data import NetflixData
from netflix_data_ui import App

if __name__ == '__main__':
    netflixdata = NetflixData()
    ui = App(netflixdata)
    ui.run()
