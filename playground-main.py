from pandas_alive.charts import animate_multiple_plots
import pandas as pd
import pandas_alive

pandas_alive.output_file('test.mp4')
# pandas_alive.output_html()

df = pandas_alive.load_dataset()

# print(df)

lc = df.diff().plot_animated(kind='line',write_to_file=False)

bc = df.plot_animated(kind='barh',write_to_file=False)

print(lc.get_frames())
print(bc.get_frames())

# print(lc.prepare_data())

animate_multiple_plots('Multi-test.mp4',[bc,lc])


