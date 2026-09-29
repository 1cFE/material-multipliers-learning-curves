# Figure 1: illustrative deployment and demand-support model

Prepared 28 September 2026. All costs, rates, market sizes and operating assumptions are chosen illustrations. The model supports Figure 1 of the post.

## Cost model

For plant number n, with the first plant at n = 1:

`C(n) = max(F, C1 × (1-r)^log2(n))`

C1 is FOAK LCOE. F is the assumed mature NOAK cost floor. The learning rate r is the chosen reduction in total LCOE per doubling until the floor is reached. Costs then remain at that floor.

This simplified model is used to make the endpoints visible in the illustration. It differs from the post's residual-learning model in Figure 3, which reduces cost above a floor asymptotically. The two rate definitions are not interchangeable. The sharp transition to a flat cost at F is a schematic assumption, not a physical prediction. These whole-LCOE curves also compress construction, equipment, operations and finance into one hypothetical trajectory. A real assessment needs to model those contributions separately.

| Scenario | FOAK, $/MWh | Assumed NOAK, $/MWh | Learning rate | Last plant before a stall | First plant at or below $80/MWh | First plant at the assumed floor |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| A | 110 | 65 | 20% | No stall | 3 | 6 |
| B | 220 | 35 | 20% | 16 | 24 | 302 |
| C | 220 | 35 | 15% | 4 | 75 | 2,541 |

## Demand and funding rule

Each design is assessed separately against the same market. The scenarios do not simultaneously sell into one shared set of customers.

Customers can sign contracts for four equal-sized plants at up to $240/MWh, then another 12 at up to $140/MWh. The broad market can absorb further plants at up to $80/MWh. The figure represents this as descending willingness to pay for the next plant's contracted electricity. The baseline contains no public subsidy. Each early customer contracts for one plant's output, and no replacement of those contracts or growth of premium demand is assumed during the deployment sequence.

A new plant can proceed without support when its LCOE does not exceed the next available customer's maximum price. We assume a competitively procured contract pays only the required price, so a high customer willingness to pay does not automatically create surplus to cross-subsidize later plants. The stopping marker is on the last plant that can proceed. The next plant requires support. The next-plant rule is applied even if a cheaper later plant would become viable again after an intervening production gap.

All plants are assumed to provide 100 MW of net capacity at a 90% capacity factor, with a 20-year flat-price contract. Each contract covers:

`E = 100 MW × 8,760 hours/year × 0.90 × 20 years = 15,768,000 MWh`

For the nth plant:

`Support(n) = E × max(C(n) - P(n), 0)`

`Cumulative support(N) = sum of Support(n), for n = 1 through N`

P(n) is customer willingness to pay in the demand schedule. All dollar figures are constant 2025 dollars. Totals are undiscounted commitments over the contracts' lives. They are neither annual subsidies nor a common-date present value. There is no assumed calendar deployment schedule. The plateau in the support curve means new competitive plants require no additional support; previously signed support contracts still have to be honored.

- A requires no modeled contract-price top-up. It still needs project finance, supplier capacity and development investment.
- B receives support for plants 17 through 23. Total: $446,606,570.57.
- C receives support for plants 5 and 6, none for plants 7 through 16, and support again for plants 17 through 74. Total: $11,196,068,355.99. This causes the intermediate plateau in its cumulative-support curve.

The support calculation sums discrete plant commitments. Area under a line on the logarithmic horizontal axis does not represent a dollar budget.

The model assumes identical plant output, successful qualification, adequate supply and finance, and sufficient evidence transfer between successive plants. It excludes failed projects, supplier investment gaps, program administration, additional risk premia and limits to market size below $80/MWh. It therefore illustrates the contract-price gap under chosen assumptions, not the full public budget necessary to commercialize fusion.

## Verification

The `make_demand_figure.py` script verifies stopping points, competitive and mature-cost plant counts, monotonic costs, nonnegative support, support totals and the discontinuous support requirement for C. An independent arithmetic review confirmed those results. All plotted data can be rebuilt from the script and CSVs.
