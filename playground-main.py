import pandas as pd
import pandas_alive

pandas_alive.output_file('test.mp4')
# pandas_alive.output_html()

df = pandas_alive.load_dataset()

print(df.diff().plot_animated(kind='line'))


