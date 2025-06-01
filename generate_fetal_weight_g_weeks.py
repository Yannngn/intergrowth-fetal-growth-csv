import csv
from decimal import Decimal


def decimal_log(x: Decimal) -> Decimal:
    return x.ln()


def decimal_exp(x: Decimal) -> Decimal:
    return x.exp()


def z_score_for_fetal_weight(gestational_age_weeks: int, estimated_weight_g: Decimal) -> Decimal:
    ga_div_10 = Decimal(gestational_age_weeks) / Decimal("10")

    lambda_ga = (
        Decimal("9.43643")
        + Decimal("9.41579") * ga_div_10 ** Decimal("-2")
        - Decimal("83.54220") * decimal_log(ga_div_10) * ga_div_10 ** Decimal("-2")
    )

    mu_ga = (
        Decimal("-2.42272")
        + Decimal("1.86478") * Decimal(gestational_age_weeks).sqrt()
        - Decimal("1.93299e-5") * Decimal(gestational_age_weeks) ** Decimal("3")
    )

    sigma_ga = (
        Decimal("0.0193557")
        + Decimal("0.0310716") * ga_div_10 ** Decimal("-2")
        - Decimal("0.0657587") * decimal_log(ga_div_10) * ga_div_10 ** Decimal("-2")
    )

    y = decimal_log(estimated_weight_g)

    if lambda_ga == 0:
        return (y - mu_ga) / sigma_ga
    else:
        numerator = decimal_exp(lambda_ga * (y - mu_ga)) - Decimal("1")
        denominator = sigma_ga * lambda_ga
        return numerator / denominator


def fetal_weight_from_z_score(gestational_age_weeks: int, z: Decimal) -> Decimal:
    ga_div_10 = Decimal(gestational_age_weeks) / Decimal("10")

    lambda_ga = (
        Decimal("9.43643")
        + Decimal("9.41579") * ga_div_10 ** Decimal("-2")
        - Decimal("83.54220") * decimal_log(ga_div_10) * ga_div_10 ** Decimal("-2")
    )

    mu_ga = (
        Decimal("-2.42272")
        + Decimal("1.86478") * Decimal(gestational_age_weeks).sqrt()
        - Decimal("1.93299e-5") * Decimal(gestational_age_weeks) ** Decimal("3")
    )

    sigma_ga = (
        Decimal("0.0193557")
        + Decimal("0.0310716") * ga_div_10 ** Decimal("-2")
        - Decimal("0.0657587") * decimal_log(ga_div_10) * ga_div_10 ** Decimal("-2")
    )

    if lambda_ga == 0:
        y = mu_ga + sigma_ga * z
    else:
        y = mu_ga + (decimal_log(Decimal("1") + sigma_ga * lambda_ga * z) / lambda_ga)
    return decimal_exp(y)


def main():
    with open("estimated_fetal_weight_g_weeks.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Gestational age (exact weeks)", "-3 SD (g)", "-2 SD (g)", "-1 SD (g)", "0 SD (g)", "1 SD (g)", "2 SD (g)", "3 SD (g)"]
        )
        for ga in range(14, 41):
            row: list = [ga]
            for z in range(-3, 4):
                weight = fetal_weight_from_z_score(ga, Decimal(z))
                row.append(round((weight), 2))
            writer.writerow(row)


if __name__ == "__main__":
    main()
