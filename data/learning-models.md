# Learning-model equations and accounting

These are the eight equations used in the post, with calculation details and equivalent forms.

## Material multiplier

`M = C_finished / V_materials`

C_finished is the finished-component price or cost under the stated boundary. V_materials is the commodity value of its constituent materials on the same price basis. Material share is 1/M. With a fixed bill, 1 - 1/M is the mathematical maximum fractional reduction before cost falls below that bill. It is not an engineering forecast.

## Ordinary total-cost learning

`C(Q) = C0 * (Q/Q0)^(-b)`

`r = 1 - 2^(-b)`

`D = log2(Q/Q0)`

`C(D) = C0 * (1-r)^D`

C0 is cost at reference cumulative production Q0. Q is later cumulative production. D counts doublings relative to Q0. r is the fractional reduction in total cost per doubling. The production unit and cost boundary must be consistent.

If production doubles n times in a year, the corresponding annual cost reduction is:

`1 - (1-r)^n`

At r = 0.20 and n = 3, remaining cost is 0.512 and annual reduction is 0.488. The learning rate does not supply the production growth rate or calendar schedule.

## Residual learning above an engineering floor

`C(D) = F + (C0-F) * (1-r_res)^D`

`D_required = ln[(C_target-F)/(C0-F)] / ln(1-r_res)`

`Q_required = Q0 * 2^(D_required)`

F is the engineering floor under a specified design and input-price basis. r_res applies only to cost above F. The inversion requires F < C_target < C0 and 0 < r_res < 1. F is approached asymptotically. A target at or below F needs a changed floor or design, rather than a finite production requirement in this model. A published total-cost rate cannot be substituted for r_res while claiming the same fitted relationship.

For C0 = $10 million, F = $1 million and r_res = 20%, cost is $5.608 million after three doublings and $3.359296 million after six. A $2 million target needs about 9.85 doublings, or about 920 times the reference cumulative production.

Figure 3 uses this residual model with starting cost 100 and floors 10, 40 and 70. Figure 1 instead caps a hypothetical total-LCOE curve at a chosen NOAK floor. Its equation, demand rule and support calculation are documented separately in fig1_model_assumptions.md.

## Weighting component savings

If a subsystem initially accounts for share s of plant capital and its cost becomes fraction k of its initial value:

`K/K0 = (1-s) + s*k`

The REBCO example has tape quantity ratio 0.75 and price ratio 0.80, so its tape-bill ratio is 0.60. Tape accounts for 80% of magnet cost, giving magnet ratio 0.80*0.60 + 0.20 = 0.68. Magnets account for 30% of plant capital, giving plant-capital ratio 0.70 + 0.30*0.68 = 0.904. All other accounts remain fixed. Electricity cost additionally depends on output, availability, replacement, operation and financing.
