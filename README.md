# Material Multipliers and Learning Curves

Data, figures and calculation scripts for the 1cFE post [Material Multipliers and Learning Curves](https://1cf.energy/material-multipliers-and-learning-curves/) (Damien Scott, September 2026). The post's text is included as published.

## Contents

- `post-learning-rates.md`: the post as published, with relative links to the figures.
- `figs/`: the six figures in PNG and editable SVG. Figure 1 (FOAK-to-NOAK demand support) is two panels in one image.
- `data/`: the data behind each figure (CSV and JSON), the Figure 1 model assumptions and checks, the Figure 2 source inputs (source locations, arithmetic, cost boundaries and limitations for each case), the component screening bands, the REBCO worked example, the policy scale comparison, `learning-models.md` (the eight equations with calculation details) and `source-notes.md` (sources and cost boundaries by figure).
- `make_charts.py` and `make_demand_figure.py`: rebuild the figures and their CSVs from the inputs.

## What the numbers are

Figure 1 is a hypothetical deployment and demand-support model; its costs, learning rates and market sizes are chosen illustrations, documented in `data/fig1_model_assumptions.md`. Figure 2 reports three sourced cost-to-material ratios (a modeled steel tank, a mass-produced passenger car and a Raptor engine nozzle jacket) with different accounting boundaries, recorded in `data/fig2_source_inputs.json`. The component screening bands (Figure 4) are author-chosen assumptions to test, with a zero-learning comparison for every component. The historical learning rates and IRENA cost endpoints keep their source definitions, units and price years. The REBCO example is a hypothetical calculation with its inputs in `data/rebco_worked_example.csv`.

## Rebuild

Python 3 with Pillow. From this directory:

```sh
python3 make_charts.py
```

`make_charts.py` also runs `make_demand_figure.py` for Figure 1. Both scripts resolve paths relative to themselves and fall back to system fonts if the macOS fonts they prefer are absent.

## Corrections

Changes after publication are recorded in this repository's history, and substantive ones are listed here with the date and reason. Questions and corrections are welcome through https://1cf.energy/contact/ or an issue on this repository.

## License

MIT. See `LICENSE`.
