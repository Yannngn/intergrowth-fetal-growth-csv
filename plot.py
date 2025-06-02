import glob
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_size_graph(csv_path, output_dir="graphs"):
    sns.set_theme(style="whitegrid")

    csv_name = os.path.splitext(os.path.basename(csv_path))[0]

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{csv_name}.png")

    df = pd.read_csv(csv_path)
    df.drop(columns=["L", "M", "S"], inplace=True)
    df_melted = df.melt(id_vars=[df.columns[0]], var_name="Percentile", value_name="Measurement")

    line_styles = {
        "SD3neg": {"color": "#ff0000", "linestyle": ":", "linewidth": 1},  # red
        "SD2neg": {"color": "#ff7f0e", "linestyle": "--", "linewidth": 1},  # orange
        "SD1neg": {"color": "#808080", "linestyle": "-.", "linewidth": 1},  # gray
        "SD0": {"color": "#000000", "linestyle": "-", "linewidth": 1.5},  # black
        "SD1": {"color": "#808080", "linestyle": "-.", "linewidth": 1},  # gray
        "SD2": {"color": "#ff7f0e", "linestyle": "--", "linewidth": 1},  # orange
        "SD3": {"color": "#ff0000", "linestyle": ":", "linewidth": 1},  # red
    }

    plt.figure(figsize=(8, 6))
    for perc in df_melted["Percentile"].unique():
        subset = df_melted[df_melted["Percentile"] == perc]
        sns.lineplot(x=subset[df.columns[0]], y=subset["Measurement"], label=perc, **line_styles[perc])

    plt.xlabel(df.columns[0])
    plt.ylabel("Measurement (mm)")
    plt.title(f"Plot for {csv_name}")
    plt.legend(title="Percentile")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    for csv_ in glob.glob("tables/*.csv"):
        plot_size_graph(csv_)


if __name__ == "__main__":
    main()
