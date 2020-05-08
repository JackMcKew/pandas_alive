import pandas as pd
import pandas_alive

covid_df = pandas_alive.load_dataset()

# with open("examples/example_dataset_table.md", "w") as md_file:
#     md_file.write(df.dropna().head(5).to_markdown())

covid_df.plot_animated(filename="examples/example-barh-chart.gif")

covid_df.plot_animated(filename="examples/example-barv-chart.gif", orientation="v")

covid_df.diff().fillna(0).plot_animated(
    filename="examples/example-line-chart.gif", kind="line"
)

animated_line_chart = covid_df.diff().fillna(0).plot_animated(kind="line",period_label=False)

animated_bar_chart = covid_df.plot_animated(kind="barh", n_visible=10)

pandas_alive.animate_multiple_plots(
    "examples/example-bar-and-line-chart.gif", [animated_bar_chart, animated_line_chart]
)

urban_df = pandas_alive.load_dataset("urban_pop")

animated_line_chart = (
    urban_df.sum(axis=1)
    .pct_change()
    .dropna()
    .mul(100)
    .plot_animated(
        kind="line", title="Total % Change in Population", 
    )
)

animated_bar_chart = urban_df.plot_animated(
    kind="barh", n_visible=10, title="Top 10 Populous Countries",period_label=False
)

pandas_alive.animate_multiple_plots(
    "examples/example-bar-and-line-urban-chart.gif",
    [animated_bar_chart, animated_line_chart],
    title="Urban Population 1977 - 2018",
)


elec_df = pd.read_csv("data/Aus_Elec_Gen_1980_2018.csv",index_col=0,parse_dates=[0],thousands=',')

elec_df.fillna(0).plot_animated('examples/example-electricity-generated-australia.gif',period_fmt="%Y")