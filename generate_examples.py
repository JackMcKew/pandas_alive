import pandas as pd
import pandas_alive

df = pandas_alive.load_dataset()

# with open("examples/example_dataset_table.md", "w") as md_file:
#     md_file.write(df.dropna().head(5).to_markdown())

# df.plot_animated(filename='examples/example-barh-chart.gif')

# df.plot_animated(filename='examples/example-barv-chart.gif',orientation='v')

# df.diff().fillna(0).plot_animated(filename='examples/example-line-chart.gif',kind='line')

animated_line_chart = df.diff().fillna(0).plot_animated(kind='line',period_length=200)

animated_bar_chart = df.plot_animated(kind='barh',period_length=200,n_visible=10)

pandas_alive.animate_multiple_plots('examples/example-bar-and-line-chart.gif',[animated_bar_chart,animated_line_chart])
