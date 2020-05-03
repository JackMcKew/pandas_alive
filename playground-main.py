import pandas as pd
import pandas_alive

pandas_alive.output_file('test.mp4')

df = pandas_alive.load_dataset()

df.plot_animated()
