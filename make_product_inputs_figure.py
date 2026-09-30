#!/usr/bin/env python3
"""Generate the revised two-product Figure 2 without changing earlier artifacts.

Requires Python 3 and Pillow, plus the sibling make_charts.py drawing helpers.
Writes only figs/fig2_us_product_inputs.{png,svg} and
data/fig2_us_product_inputs.csv. Inputs and accounting boundaries are in
data/fig2_us_product_inputs.json.
"""
from pathlib import Path
import json

from make_charts import Figure, COLORS, INK, MUTED, GRID, write_csv


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def draw_panel(fig, *, x, title, basis, unit_note, numerator_label,
               numerator_text, input_label, input_text, input_fraction,
               ratio, ratio_label, notes, source, color):
    """Draw an independent pair of bars with its own units and boundaries."""
    width = 395
    fig.text(x, 150, title, 22, INK, bold=True)
    fig.text(x, 176, basis, 16, MUTED)
    fig.text(x, 199, unit_note, 15, MUTED)

    fig.text(x, 241, numerator_label, 17, INK)
    fig.text(x + width, 241, numerator_text, 18, color, anchor="end", bold=True)
    fig.rect(x, 255, width, 23, color)

    fig.text(x, 312, input_label, 17, INK)
    fig.text(x + width, 312, input_text, 18, color, anchor="end", bold=True)
    fig.rect(x, 326, width * input_fraction, 23, color)

    fig.text(x, 408, ratio, 36, color, bold=True)
    fig.text(x, 438, ratio_label, 17, INK)
    for y, line in zip((466, 488), notes):
        fig.text(x, y, line, 15, MUTED)
    fig.text(x, 523, source, 14, MUTED)


def main():
    records = json.loads((DATA / "fig2_us_product_inputs.json").read_text())["cases"]
    car, house = records
    assert car["is_raw_material_ratio"] is True
    assert house["is_raw_material_ratio"] is False
    assert car["numerator_value"] == 8 and car["input_value"] == 0.6
    assert house["numerator_value"] == 100 and house["input_value"] == 50

    fig = Figure(2, "SOURCED EXAMPLES",
                 "Cost and material inputs in two US products",
                 "Separate panels preserve the different accounting boundaries")
    fig.line([(500, 134), (500, 532)], GRID, 1)
    draw_panel(
        fig, x=70, title="Mass-produced passenger car",
        basis="US Department of Energy assessment · 2012",
        unit_note="Dollars per pound of vehicle",
        numerator_label="Selling price", numerator_text="$8.00/lb",
        input_label="Raw-material value", input_text="$0.60/lb",
        input_fraction=car["input_value"] / car["numerator_value"],
        ratio="≈ 13×", ratio_label="Selling price ÷ raw-material value",
        notes=("Raw-material estimate covers the car's material mix.",
               "Selling price includes distribution and margins."),
        source="Source: DOE technology assessments, p. 25.",
        color=COLORS[0],
    )
    draw_panel(
        fig, x=535, title="Single-family house construction",
        basis="US construction estimate cited by Potter · 2026",
        unit_note="Index: hard construction cost = 100",
        numerator_label="Hard construction cost", numerator_text="100",
        input_label="Purchased building inputs", input_text="≈ 50",
        input_fraction=house["input_value"] / house["numerator_value"],
        ratio="≈ 2×", ratio_label="Construction cost ÷ purchased inputs",
        notes=("Inputs include finished materials and components.",
               "This is not a raw-material ratio. Land is excluded."),
        source="Source: Potter, citing Craftsman's cost estimator.",
        color=COLORS[2],
    )
    fig.footer("Different cost and input boundaries. Neither ratio measures removable cost.")
    fig.save("fig2_us_product_inputs")

    rows = []
    for record in records:
        rows.append({
            "case_id": record["case_id"],
            "technology": record["technology"],
            "geography": record["geography"],
            "period": record["period"],
            "numerator_value": record["numerator_value"],
            "input_value": record["input_value"],
            "value_units": record["value_units"],
            "cost_to_input_ratio": f'{record["numerator_value"] / record["input_value"]:.12g}',
            "display_ratio": record["display_ratio"],
            "ratio_name": record["ratio_name"],
            "is_raw_material_ratio": str(record["is_raw_material_ratio"]).lower(),
            "numerator_boundary": record["numerator_boundary"],
            "input_boundary": record["input_boundary"],
            "formula": record["formula"],
            "evidence_status": record["evidence_status"],
            "source_urls": " | ".join(s["url"] for s in record["sources"]),
            "source_locations": " | ".join(s["location"] for s in record["sources"]),
            "limitations": record["limitations"],
        })
    write_csv("fig2_us_product_inputs.csv", rows)


if __name__ == "__main__":
    main()
