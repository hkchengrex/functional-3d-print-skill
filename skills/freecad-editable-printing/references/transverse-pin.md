# PLA transverse pin joint for force assembly

Load for comparable one-time joints with a transverse pin through interlocking tabs. This is an optional worked reference, not a default clearance rule.

## Use and limits

Use for a compact, rigid connection intended for one-time force assembly. The zero-clearance fit can require hammer installation; do not specify it as a hand-press fit. Preserve the shaft dimensions when reproducing this fit.

No rated insertion force, strength, cycle life or long-term retention is specified. Evaluate those requirements for the target application.

## Assets

- [Design parameters](../assets/pin-joint/design-parameters.json): mechanical dimensions.

Use the dimensions below and the design parameters to construct native editable features. CAD and slicer outputs stay in the local project, outside the repository.

## Mechanism and dimensions

The rear tongue enters between two front cheeks. A transverse pin prevents front/back separation by bearing against the hole walls. Pin friction resists backing out; the head limits insertion depth. There is no snap catch.

Coordinates: x along the pin axis, y along the tongue insertion direction, z across the joint. All dimensions below are mm.

| Feature | Geometry |
|---|---|
| Shaft / bore cross-section | **1.8 in y × 2.4 in z**, **0 nominal clearance** |
| Shaft envelope before head | x 27.2..30.8, y 1.2..3.0, z 24.8..27.2 |
| Tip | First 0.35 of length tapers in z only; end width 1.7 in z |
| Head | x 30.8..31.4, y 1.2..3.0, z 24.3..27.7 |
| Rear tongue | x 28.3..30.1, y 0.3..4.5, z 22..30 |
| Tongue pocket | x 28.2..30.2, y 0.15..4.32, z 21.85..30.15 |
| Front cheeks | Nominal 1.2 along x; outer head recess reduces local bearing length |

Zero clearance describes matching CAD surfaces, not measured fit or a guarantee for other geometries. Insert the pin from the outer x side after the halves are seated.

## Design constraints

Provide side access for pin insertion and sufficient wall thickness around the bore. The tongue and cheeks carry separation loads through the pin; friction retains the pin along its axis. Use a separate retaining feature if friction alone is insufficient. Choose a different fit when hand assembly or repeated removal is required.
