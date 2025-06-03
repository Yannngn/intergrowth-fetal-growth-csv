import csv
from decimal import Decimal


def decimal_log(x: Decimal) -> Decimal:
    return x.ln()


def decimal_sqrt(x: Decimal) -> Decimal:
    return x.sqrt()


def decimal_exp(x: Decimal) -> Decimal:
    return x.exp()


def decimal_pow(x: Decimal, y: Decimal) -> Decimal:
    return x**y


def get_lambda_ga(gestational_age_weeks: int) -> Decimal:
    decimal_ga = Decimal(gestational_age_weeks)
    ga_div_10 = decimal_ga / Decimal("10")

    return (
        Decimal("9.43643")
        + Decimal("9.41579") * decimal_pow(ga_div_10, Decimal("-2"))
        - Decimal("83.54220") * decimal_log(ga_div_10) * decimal_pow(ga_div_10, Decimal("-2"))
    )


def get_mu_ga(gestational_age_weeks: int) -> Decimal:
    decimal_ga = Decimal(gestational_age_weeks)

    return Decimal("-2.42272") + Decimal("1.86478") * decimal_ga.sqrt() - Decimal("1.93299e-5") * decimal_pow(decimal_ga, Decimal("3"))


def get_sigma_ga(gestational_age_weeks: int) -> Decimal:
    decimal_ga = Decimal(gestational_age_weeks)
    ga_div_10 = decimal_ga / Decimal("10")

    return (
        Decimal("0.0193557")
        + Decimal("0.0310716") * ga_div_10 ** Decimal("-2")
        - Decimal("0.0657587") * decimal_log(ga_div_10) * ga_div_10 ** Decimal("-2")
    )


def z_score_for_fetal_weight(gestational_age_weeks: int, estimated_weight_g: Decimal) -> Decimal:
    lambda_ga = get_lambda_ga(gestational_age_weeks)

    mu_ga = get_mu_ga(gestational_age_weeks)

    sigma_ga = get_sigma_ga(gestational_age_weeks)

    y = decimal_log(estimated_weight_g)

    if lambda_ga == 0:
        return (y - mu_ga) / sigma_ga
    else:
        numerator = decimal_exp(lambda_ga * (y - mu_ga)) - Decimal("1")
        denominator = sigma_ga * lambda_ga
        return numerator / denominator


def fetal_weight_from_z_score(gestational_age_weeks: int, z: Decimal) -> Decimal:
    lambda_ga = get_lambda_ga(gestational_age_weeks)

    mu_ga = get_mu_ga(gestational_age_weeks)

    sigma_ga = get_sigma_ga(gestational_age_weeks)

    if lambda_ga == 0:
        y = mu_ga * decimal_exp(z * sigma_ga)
    else:
        y = mu_ga * decimal_pow(z * sigma_ga * lambda_ga + Decimal("1"), decimal_pow(lambda_ga, Decimal("-1")))

    return decimal_exp(y)


def main():
    with open("tables/estimated_fetal_weight_g_weeks.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Week", "L", "M", "S", "SD3neg", "SD2neg", "SD1neg", "SD0", "SD1", "SD2", "SD3"])
        for ga in range(14, 42):
            row: list = [ga]

            row.append(get_lambda_ga(ga).exp())
            row.append(get_mu_ga(ga).exp())
            row.append(get_sigma_ga(ga).exp())

            for z in range(-3, 4):
                weight = fetal_weight_from_z_score(ga, Decimal(z))
                row.append(round((weight), 2))
            writer.writerow(row)


if __name__ == "__main__":
    main()
