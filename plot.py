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

    df_melted = df.melt(id_vars=[df.columns[0]], var_name="Percentile", value_name="Measurement")

    line_styles = {
        "-3 SD (mm)": {"color": "#ff0000", "linestyle": ":", "linewidth": 1},  # red
        "-2 SD (mm)": {"color": "#ff7f0e", "linestyle": "--", "linewidth": 1},  # orange
        "-1 SD (mm)": {"color": "#808080", "linestyle": "-.", "linewidth": 1},  # gray
        "0 SD (mm)": {"color": "#000000", "linestyle": "-", "linewidth": 1.5},  # black
        "1 SD (mm)": {"color": "#808080", "linestyle": "-.", "linewidth": 1},  # gray
        "2 SD (mm)": {"color": "#ff7f0e", "linestyle": "--", "linewidth": 1},  # orange
        "3 SD (mm)": {"color": "#ff0000", "linestyle": ":", "linewidth": 1},  # red
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


def plot_weight_graph(csv_path, output_dir="graphs"):
    sns.set_theme(style="whitegrid")

    csv_name = os.path.splitext(os.path.basename(csv_path))[0]

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{csv_name}.png")

    df = pd.read_csv(csv_path)
    df_melted = df.melt(id_vars=[df.columns[0]], var_name="Percentile", value_name="Measurement (g)")

    line_styles = {
        "-3 SD (g)": {"color": "#ff0000", "linestyle": ":", "linewidth": 1},
        "-2 SD (g)": {"color": "#ff7f0e", "linestyle": "--", "linewidth": 1},
        "-1 SD (g)": {"color": "#808080", "linestyle": "-.", "linewidth": 1},
        "0 SD (g)": {"color": "#000000", "linestyle": "-", "linewidth": 1.5},
        "1 SD (g)": {"color": "#808080", "linestyle": "-.", "linewidth": 1},
        "2 SD (g)": {"color": "#ff7f0e", "linestyle": "--", "linewidth": 1},
        "3 SD (g)": {"color": "#ff0000", "linestyle": ":", "linewidth": 1},
    }

    x_col = df.columns[0]
    x_vals = df[x_col]
    n = len(x_vals)
    splits = [0, n // 3, 2 * n // 3, n]

    _, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    for i in range(3):
        ax = axes[i]
        x_start, x_end = splits[i], splits[i + 1]
        x_range = x_vals.iloc[x_start:x_end]
        for perc in df_melted["Percentile"].unique():
            subset = df_melted[(df_melted["Percentile"] == perc) & (df_melted[x_col].between(x_range.iloc[0], x_range.iloc[-1]))]
            sns.lineplot(
                x=subset[x_col],
                y=subset["Measurement (g)"],
                label=perc if i == 0 else None,
                ax=ax,
                **line_styles[perc],
            )
        ax.set_xlabel(x_col)
        if i == 0:
            ax.set_ylabel("Measurement (g)")
            ax.set_title(f"Plot for {csv_name}")
        else:
            ax.set_ylabel("")
            ax.set_title("")
        if i == 0:
            ax.legend(title="Percentile")
        else:
            legend = ax.get_legend()
            if legend is not None:
                legend.remove()

        ax.grid(True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    for csv_ in glob.glob("tables/*.csv"):
        if csv_.endswith("g_weeks.csv"):
            plot_weight_graph(csv_)
            continue

        plot_size_graph(csv_)


if __name__ == "__main__":
    main()
