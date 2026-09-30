# Sources, cost boundaries and calculation assumptions

Prepared 24 September 2026. All numerical screening bands are chosen assumptions. Mechanism sources explain manufacturing processes and qualification constraints; they do not supply the bands.

## Figure 1: FOAK-to-NOAK deployment and demand support

All inputs are chosen illustrations. Full assumptions, the cost equation and support accounting are in `fig1_model_assumptions.md`. `make_demand_figure.py` generates the figure and three CSVs. Its simplified total-LCOE rate is distinct from the residual rate used in Figure 3. The modeled commitments cover contract-price gaps only. They do not estimate the full cost of commercializing fusion.

## Figure 2: material-multiplier calibration

Figure 2 uses an open steel water/process tank (about 1.4×), a mass-produced passenger car (about 13×) and a Raptor engine nozzle-jacket component (about 65×). The tank is a fabrication model, the car uses a selling-price estimate, and the Raptor part uses reported company estimates. The sources have different material and cost boundaries, stated in the article, figure and input data. Each case's source location, arithmetic, cost boundary and limitations are in `fig2_source_inputs.json`.

### Updated Figure 2: US whole-product comparison

`fig2_us_product_inputs.json` and its generated CSV document a separate version with two panels. The [DOE technology assessment](https://www.govinfo.gov/content/pkg/GOVPUB-E-PURL-gpo59801/pdf/GOVPUB-E-PURL-gpo59801.pdf#page=29), printed p. 25, provides the car's aggregate selling-price and raw-material estimates: $8/lb and $0.60/lb. Their ratio is 13.33, displayed as approximately 13×.

[Potter's May 2026 analysis](https://www.construction-physics.com/p/where-are-the-economies-of-scale), using Craftsman's National Construction Estimator, gives the US house's approximate 50% purchased-input share of hard construction cost. A normalized cost index of 100 divided by 50 gives approximately 2×. These indices are not dollar costs. Purchased materials and components already contain upstream manufacturing. Land and other development costs are outside the numerator. Footnote 4 explains the difference from a raw-material calculation.

The panels do not establish comparable manufacturing-efficiency scores. Both retain their source's accounting boundaries. No new figure or calculation replaces the earlier files used by the retained article.

### Medicines as an example of value beyond ingredients

[CBO (2022), Box 3](https://www.cbo.gov/publication/57772), distinguishes low incremental manufacturing costs for small-molecule brand-name drugs from the expense and risk of development and approval. It also describes the effect of market power and exclusivity on prices. Incremental manufacturing cost is broader than raw-material cost. This source supports a qualitative example, not a numerical material multiplier or a claim that every price premium represents necessary work.

## Figure 3: floors and residual learning

Reference cost index C0 = 100. The three floor indices are 10, 40 and 70. The residual learning rate is 20% per cumulative-production doubling. C(D) = F + (100-F) × 0.8^D. At eight doublings the cost indices are 25.0994944, 50.0663296 and 75.0331648.

The assumed 20% residual rate is not a fitted total-cost rate. The effective total-cost reduction for the next doubling is 0.2 × (C-F)/C. D is log2(Q/Q0), with Q and Q0 on the same qualified-production basis. The floor is fixed only within the modeled specification and price assumptions.

The post's hypothetical $10 million magnet has a $200,000 constituent-material bill and a $1 million engineering floor. M = 50. C after three and six doublings is $5.608 million and $3.359296 million. Reaching $2 million takes ln(1/9)/ln(0.8) = 9.8467 doublings, or about 920.76 times Q0.

## Figure 4: component screening scenarios

The eight rows use deliberately broad, overlapping scenario inputs. They are not observed cost ranges, confidence intervals, a supplier-price survey or measured learning curves. Values are held in the component CSV and used consistently by the plot. Every component has a separate zero-learning comparator. Its cost then remains C0; the positive-rate inversion is not applicable.

The assumptions test three kinds of starting cost structure: M = 10 to 100 for process-intensive hypotheses, M = 3 to 30 for mixed fabrication hypotheses, and M = 2 to 10 for the specified conventional-equipment hypothesis. These correspond to different assumed material shares, not measured properties of the named classes. The residual-rate bands test different possible levels of additional manufacturing improvement. They are independent of starting production, additional doublings, engineering floor, investment and plant cost share, all of which must be supplied for a plant projection.

### Cost boundaries and mechanism sources

- **HTS magnet:** qualified conductor, winding, joints and supporting structure. Refrigeration is separate. [DOE award DE-SC0023996](https://www.sbir.gov/awards/214121) distinguishes throughput, critical current, equipment and tape capacity. Its $50 million per 1,000 km/year planning baseline comes from a 2024 development plan.
- **IMG pulser assembly:** capacitors, gas switches, enclosure, connections, assembly and acceptance test. [Damideh et al. (2024)](https://www.nature.com/articles/s41598-024-67774-4) report six tested stages, 102 identical bricks and 330 GW peak electrical output. General IMG specifications in the abstract are separate from demonstrated commercial endurance.
- **IFE laser driver:** diodes, gain medium, optics, cooling and optical assembly. Target systems are separate. The [LLNL-hosted diode-pump white paper](https://lasers.llnl.gov/sites/lasers/files/2023-11/haefner-ILT-IFE-workshop-2022-1.pdf) and [LLNL's 2025 workshop report](https://lasers.llnl.gov/news/llnl-hosts-workshop-shape-future-diode-pumped-laser-technology) describe supply-chain overlap and the remaining scale and specification gaps.
- **First-wall or divertor assembly:** armor, heat sink, coolant joints and acceptance tests. The [ITER divertor description](https://www.iter.org/machine/divertor) illustrates heat-flux testing and qualification. It does not supply commercial costs or learning rates.
- **Vacuum vessel:** the specified formed structure, ports, welds, inspection and any shielding or cooling included in the account. [ITER's vessel description](https://www.iter.org/machine/vacuum-vessel) establishes the breadth of these functions. ITER is an engineering example, not an assumed commercial architecture.
- **Conventional steam balance of plant:** turbine-generator and ordinary heat-exchange equipment. Site work and novel primary-loop equipment are separate. Novel supercritical-CO2 machinery is excluded from the mature-steam hypothesis. The [STEP demonstration](https://www.gti.energy/step-demo/step-demo-project/) illustrates why those categories should remain distinct.
- **Helium cryogenic equipment:** compressor, cold box and refrigeration package. Distribution and site installation are separate. [ITER cryogenics](https://www.iter.org/machine/supporting-systems/cryogenics) illustrates temperature and heat-load requirements. LNG deployment does not directly establish experience for a helium refrigerator at a different operating temperature.
- **Tritium-processing subsystem:** a specified extraction, separation, storage or detritiation function. The breeding blanket and fuel inventory are separate. [ITER fuelling](https://www.iter.org/machine/supporting-systems/fuelling) distinguishes fuel-cycle operations that should not be merged into one interchangeable product.

The four supply-chain levels locate production experience: whole-plant, concept-specific, cross-fusion and cross-industry. A row can span multiple levels, but each process still needs its own experience unit and baseline.

## Figure 5: REBCO worked example

Chosen inputs: magnet share of initial plant capital = 0.30; tape share of initial magnet cost = 0.80; tape quantity ratio = 0.75; price-per-meter ratio = 0.80. The tape bill ratio is 0.60, magnet ratio is 0.68 and plant-capital ratio is 0.904. Savings are respectively 40%, 32% and 9.6%.

Each bar is normalized to its own reference account. No performance, integration, replacement, availability or financing improvement is assumed. The price-per-meter change excludes the critical-current gain represented by the separate quantity change. Supplier investment must be included consistently with the quoted price rather than recovered twice.

## Figure 6: published IRENA endpoints

IRENA (2025), Renewable Power Generation Costs in 2024, executive-summary Table S1, printed page 4. The price-year convention is 2024 USD. [Executive summary](https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_Summary_2025.pdf).

PV observations are $417/MWh in 2010 and $43/MWh in 2024. CSP observations are $402/MWh and $92/MWh. Reductions computed from those rounded values are 89.688% and 77.114%, displayed as 90% and 77%. The figure contains endpoints only. It supplies neither an intervening time series nor a fitted experience curve.

Values describe newly commissioned global project cohorts. CSP can include thermal storage and a different output profile. The comparison does not establish a causal effect of modularity or compare equal delivered electricity services. The article's target is $10/MWh in 2025 dollars; it does not silently rebase the historical IRENA series.

## Additional numerical examples

The early-market scenario starts at 100 cumulative units and adds 700, reaching 800. D = log2(800/100) = 3. At an assumed 20% total-cost learning rate, cost ratio = 0.8^3 = 0.512. Six doublings require 100 × 2^6 = 6,400 cumulative units. These are chosen inputs, not an estimate of any fusion supplier's market.

Sources were consulted in September 2026. Web sources carry their consultation dates in the post's references.
