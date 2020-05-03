import pandas as pd
import pandas_alive

df = pandas_alive.load_dataset()

with open("example_dataset_table.md", "w") as md_file:
    md_file.write(df.dropna().head(5).to_markdown())

pandas_alive.output_file('example-barh-chart.gif')
df.plot_animated()

pandas_alive.output_file('example-barv-chart.gif')
df.plot_animated(orientation='v')

pandas_alive.output_file('example-line-chart.gif')
df.diff().plot_animated(kind='line')

animated_line_chart = df.diff().plot_animated(kind='line',write_to_file=False,period_length=200)

animated_bar_chart = df.plot_animated(kind='barh',write_to_file=False,period_length=200)

pandas_alive.animate_multiple_plots('example-bar-and-line-chart.gif',[animated_bar_chart,animated_line_chart])


