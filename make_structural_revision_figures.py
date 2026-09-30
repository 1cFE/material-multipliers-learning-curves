#!/usr/bin/env python3
"""Generate the figures reordered for the revised article.

Requires Python 3 and Pillow, plus the sibling make_charts.py drawing helpers.
Writes only the following files:
    figs/fig4_rebco_cost_shares.{png,svg}
    figs/fig5_component_plane.{png,svg}
    data/fig4_rebco_cost_shares.csv
    data/fig5_component_plane.csv
    data/residual_learning_sensitivity.csv

The underlying assumptions and calculations are unchanged. The original
make_charts.py entry point still reproduces the earlier numbered artifacts.
"""
import math

from make_charts import figure3, figure4, write_csv


def residual_learning_sensitivity():
    """Calculate two chosen residual-learning cases, not an AI forecast."""
    initial_cost = 10_000_000
    material_bill = 200_000
    engineering_floor = 1_000_000
    target_cost = 2_000_000
    rows = []
    for rate in (0.10, 0.20):
        doublings = math.log((target_cost - engineering_floor) /
                             (initial_cost - engineering_floor)) / math.log(1 - rate)
        rows.append({
            'component': 'hypothetical magnet',
            'initial_cost_usd': initial_cost,
            'material_bill_usd': material_bill,
            'engineering_floor_usd': engineering_floor,
            'target_cost_usd': target_cost,
            'residual_learning_rate_per_doubling': rate,
            'required_doublings': f'{doublings:.10f}',
            'cumulative_production_multiple_Q_over_Q0': f'{2 ** doublings:.10f}',
            'input_evidence_status': 'chosen_assumptions',
            'result_evidence_status': 'calculated_chosen_scenario',
            'rate_applies_to': 'cost above separately chosen engineering floor',
            'formula_D_required': 'ln((C_target-F)/(C_0-F))/ln(1-r_res)',
            'formula_Q_multiple': '2**D_required',
            'interpretation': 'sensitivity comparison, not an AI forecast or causal estimate',
        })
    write_csv('residual_learning_sensitivity.csv', rows)


if __name__ == '__main__':
    figure4(number=4, stem='fig4_rebco_cost_shares', write_worked_example=False)
    figure3(number=5, stem='fig5_component_plane', wrapped_labels=True)
    residual_learning_sensitivity()
