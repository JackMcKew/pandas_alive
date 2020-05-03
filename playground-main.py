import pandas as pd
import pandas_alive

pandas_alive.output_file('test.mp4')

df = pandas_alive.load_dataset()

lc = df.diff().plot_animated(kind='line',write_to_file=False)

bc = df.plot_animated(kind='barh',write_to_file=False)

pandas_alive.animate_multiple_plots('Multi-test.gif',[bc,lc])


