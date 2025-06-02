import glob

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def estimate_lms(sds, values):
    """
    Estimate LMS parameters from given SD scores and values.
    Uses nonlinear optimization to fit the Box-Cox (LMS) model:
    value = M * (1 + L * S * z) ** (1 / L)  if L != 0
    value = M * exp(S * z)                  if L == 0
    """
    sds = np.array(sds)
    values = np.array(values)

    def lms_loss(params):
        L, M, S = params
        # Avoid invalid values
        if M <= 0 or S <= 0:
            return np.inf
        if abs(L) < 1e-6:
            pred = M * np.exp(S * sds)
        else:
            pred = M * np.power(1 + L * S * sds, 1 / L)
        return np.sum((pred - values) ** 2)

    # Initial guesses
    M0 = values[3]  # SD0
    S0 = (values[4] - values[2]) / (2 * M0)  # Approximate S
    L0 = 0.1  # Small value for L

    res = minimize(
        lms_loss,
        x0=[L0, M0, S0],
        bounds=[(-2, 2), (1e-3, None), (1e-6, None)],
        method="L-BFGS-B",
    )
    L, M, S = res.x
    return float(L), float(M), float(S)


def process_file(input_csv, output_csv):
    # Read and clean header
    df = pd.read_csv(input_csv)
    # Rename columns
    rename_map = {
        df.columns[0]: "Week",
        "-3 SD (mm)": "SD3neg",
        "-2 SD (mm)": "SD2neg",
        "-1 SD (mm)": "SD1neg",
        "0 SD (mm)": "SD0",
        "1 SD (mm)": "SD1",
        "2 SD (mm)": "SD2",
        "3 SD (mm)": "SD3",
        "-3 SD (g)": "SD3neg",
        "-2 SD (g)": "SD2neg",
        "-1 SD (g)": "SD1neg",
        "0 SD (g)": "SD0",
        "1 SD (g)": "SD1",
        "2 SD (g)": "SD2",
        "3 SD (g)": "SD3",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Prepare output
    output = []
    for _, row in df.iterrows():
        week = row["Week"]
        sds = [-3, -2, -1, 0, 1, 2, 3]
        values = [row[f"SD{n if n >= 0 else str(abs(n)) + 'neg'}"] for n in sds]
        L, M, S = estimate_lms(sds, values)
        output.append(
            {
                "Week": week,
                "L": L,
                "M": M,
                "S": S,
                "SD3neg": values[0],
                "SD2neg": values[1],
                "SD1neg": values[2],
                "SD0": values[3],
                "SD1": values[4],
                "SD2": values[5],
                "SD3": values[6],
            }
        )

    out_df = pd.DataFrame(output)
    out_df.to_csv(output_csv, index=False)


def main():
    for csv_ in glob.glob("original/*.csv"):
        process_file(csv_, csv_.replace("original", "tables"))


if __name__ == "__main__":
    main()
