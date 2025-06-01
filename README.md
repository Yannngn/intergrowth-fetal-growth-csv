# INTERGROWTH 21st FETAL GROWTH CSV DATA

<!-- badges: start -->

[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

<!-- badges: end -->

This repository contains data files and sanity check plots related to the **INTERGROWTH-21st** project. The CSV files are derived from publicly available INTERGROWTH-21st PDF documents and include key datasets used for analysis. The accompanying graphs provide visual sanity checks to validate the integrity and consistency of the imported data.

## Equations

The estimated fetal weight in grams per week was calculated with the equation provided by the source

**Table S1: Equations for parameters and computation of Z-scores and centiles for estimated fetal weight according to gestational age**

**Skewness**  
λ(GA) = 9.43643 + 9.41579 × (GA/10)<sup>−2</sup> − 83.54220 × log(GA/10) × (GA/10)<sup>−2</sup>

**Mean**  
μ(GA) = −2.42272 + 1.86478 × GA<sup>0.5</sup> − 1.93299e−5 × GA<sup>3</sup>

**Coefficient of variation**  
σ(GA) = 0.0193557 + 0.0310716 × (GA/10)<sup>−2</sup> − 0.0657587 × log(GA/10) × (GA/10)<sup>−2</sup>

**Z-score**  
Let Y = log(EFW)

- If λ(GA) = 0:  
   Z(GA) = σ(GA)<sup>−1</sup> × log[Y / μ(GA)]
- If λ(GA) ≠ 0:  
   Z(GA) = [σ(GA) × λ(GA)]<sup>−1</sup> × [(Y / μ(GA))<sup>λ(GA)</sup> − 1]

**Centiles**  
Z<sub>α</sub> defined by Pr(z ≤ Z<sub>α</sub>) = α for z ~ N(0,1), i.e. Z<sub>α</sub> = Φ<sup>−1</sup>(α)

- If λ(GA) = 0:  
   log[C<sub>α</sub>(GA)] = μ(GA) × exp[σ(GA) × Z<sub>α</sub>]
- If λ(GA) ≠ 0:  
   log[C<sub>α</sub>(GA)] = μ(GA) × [Z<sub>α</sub> × σ(GA) × λ(GA) + 1]<sup>1/λ(GA)</sup>

_GA: gestational age in exact weeks; EFW: estimated fetal weight in grams. The log function denotes the natural logarithm (base e)._

## Contents

- **CSV files**: Data extracted from INTERGROWTH-21st PDFs.
- **Graphs**: Plots for verifying data correctness.

## Usage

Use the CSV files for further analysis or modeling. Refer to the graphs to ensure the data has been correctly processed and imported.

## Source

INTERGROWTH-21st public datasets (PDFs).

## License

The data and documentation in this directory are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.  
If you use this data, please cite the original INTERGROWTH-21st publication as indicated above.

Any code or scripts are licensed under the MIT License.

## Citation

Stirnemann, J., Salomon, L.J., & Papageorghiou, A.T. (2020). INTERGROWTH-21st standards for Hadlock's estimation of fetal weight. _Ultrasound Obstet Gynecol_, 56: 946-948. [https://doi.org/10.1002/uog.22000](https://doi.org/10.1002/uog.22000)
