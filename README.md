# Material Multipliers and Learning Curves

Data, figures and calculation scripts for the 1cFE post [Material Multipliers and Learning Curves](https://1cf.energy/material-multipliers-and-learning-curves/) (Damien Scott, September 2026). The post's text is included as published.

## Contents

- `post-learning-rates.md`: the post as published, with relative links to the figures.
- `figs/`: the six figures in PNG and editable SVG. Figure 1 (FOAK-to-NOAK demand support) is two panels in one image.
- `data/`: the data behind each figure (CSV and JSON), the Figure 1 model assumptions and checks, the Figure 2 source inputs (source locations, arithmetic, cost boundaries and limitations for each case), the component screening bands, the REBCO worked example, the policy scale comparison, `learning-models.md` (the eight equations with calculation details) and `source-notes.md` (sources and cost boundaries by figure).
- `make_charts.py` and `make_demand_figure.py`: rebuild the figures and their CSVs from the inputs.
- `make_product_inputs_figure.py`: rebuild the updated Figure 2 comparison of a US passenger car and single-family house, using `data/fig2_us_product_inputs.json`. Outputs use the `fig2_us_product_inputs` filename so the earlier figure and article remain intact.

## What the numbers are

Figure 1 is a hypothetical deployment and demand-support model; its costs, learning rates and market sizes are chosen illustrations, documented in `data/fig1_model_assumptions.md`. Figure 2 reports three sourced cost-to-material ratios (a modeled steel tank, a mass-produced passenger car and a Raptor engine nozzle jacket) with different accounting boundaries, recorded in `data/fig2_source_inputs.json`. The component screening bands (Figure 4) are author-chosen assumptions to test, with a zero-learning comparison for every component. The historical learning rates and IRENA cost endpoints keep their source definitions, units and price years. The REBCO example is a hypothetical calculation with its inputs in `data/rebco_worked_example.csv`.

The updated Figure 2 uses whole US products in separate panels: a car's selling price divided by raw-material value (about 13×), and a house's hard construction cost divided by purchased material and component cost (about 2×). The house ratio is not a raw-material multiplier. Neither ratio measures removable cost. Source locations and accounting limits are in `data/fig2_us_product_inputs.json`.

## Rebuild

Python 3 with Pillow. From this directory:

```sh
python3 make_charts.py
python3 make_product_inputs_figure.py
```

`make_charts.py` also runs `make_demand_figure.py` for Figure 1. Both scripts resolve paths relative to themselves and fall back to system fonts if the macOS fonts they prefer are absent.

## Corrections

Changes after publication are recorded in this repository's history, and substantive ones are listed here with the date and reason. Questions and corrections are welcome through https://1cf.energy/contact/ or an issue on this repository.

- 29 September 2026: Added a US whole-product version of Figure 2 with a car and a house. Separate panels distinguish raw materials from purchased construction inputs. The earlier figure, its source data and the article text are retained unchanged.

## License

MIT. See `LICENSE`.
