import pandas as pd
import pandas_alive

pandas_alive.output_file('test.mp4')
# pandas_alive.output_html()

df = pandas_alive.load_dataset()

# df.diff().max(axis=1).plot_animated(kind='line')

i=0

# print(df.select_dtypes(include=[pd.np.number]).min().min())
# print(df.select_dtypes(include=[pd.np.number]).max().max())

# print(df.values.min())

# print(df.values.max())

print(df.diff().plot_animated(kind='line'))


