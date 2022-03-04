# Induced Fit Docking Dataset

Reconstruct (partial) data set used to validate Induced Fit Docking (IFD).

> Sherman, W., Day, T., Jacobson, M. P., Friesner, R. A., & Farid, R. (2006). Novel procedure for modeling ligand/receptor induced fit effects. Journal of medicinal chemistry, 49(2), 534-553.

If you use the data in this repository, don't forget to cite the paper above.

## Notes

Visually, the poses in structures `3pgh` and `1cx2` (chain `A`) do not appear to correspond to the ones in Fig. 6 and Fig. 7. For `3pgh` the cognate ligand pose is the same, while the non-cognate ligand is different, which is not a problem since it will be sampled during docking.

Structures `1dba` and `1dm2` (*apo* structures) have been omitted on purpose because there is not ligand in the binding site (useful to automatically define the search space for docking).

## Dependencies

* [pandas](https://pandas.pydata.org/)
* [ProDy](http://prody.csb.pitt.edu/index.html)
