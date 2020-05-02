import pandas as pd
import pandas_alive

df = pandas_alive.load_dataset()

df.animated_plot()
