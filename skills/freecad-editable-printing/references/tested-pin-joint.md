# Accepted hammer-installed PLA pin joint

Load for comparable one-time joints with a transverse pin through interlocking tabs. This is an optional worked reference, not a default clearance rule.

## Evidence

Recorded 2026-09-16. User report: **"had to hammer it in but it holds the joints together well"**. After discussing reduced pin dimensions, the user chose **"ok let's not change. keep this."** Preserve the tested pin. The suggested smaller shafts and four-sided tip taper were not implemented or tested.

This establishes qualitative acceptance of one local coupon. Insertion force, printed dimensions, removal, repeated assembly, long-term pin retention, creep, rated strength and full-holder performance were not measured. Hammer installation is an observed result, not a universal assembly instruction.

## Assets

- [Editable coupon](../assets/pin-joint/accepted-pin.FCStd): exact archived test CAD. Finished objects: `TestFront`, `TestRear`, `Right26Pin`. The source holder history remains for native editability; other objects are hidden. Copy before editing.
- [Test print project](../assets/pin-joint/pin-test.3mf): three single-color parts in the tested orientation.
- [Test record](../assets/pin-joint/test-record.json): setup, dimensions, transforms and source hashes.

The CAD is the dimensional authority. This reference intentionally retains the tested crop rather than replacing it with a newly approximated joint.

## Mechanism and dimensions

The rear tongue enters between two front cheeks. A transverse pin prevents front/back separation by bearing against the hole walls. Pin friction resists backing out; the head limits insertion depth. There is no snap catch.

Coordinates are inherited from the holder: x across width/pin axis, y front-to-back, z height. All dimensions below are mm.

| Feature | Tested geometry |
|---|---|
| Coupon crop | x 24..31.4, z 18..34; full original thickness |
| Shaft / bore cross-section | **1.8 in y × 2.4 in z**, **0 nominal clearance** |
| Shaft envelope before head | x 27.2..30.8, y 1.2..3.0, z 24.8..27.2 |
| Tip | First 0.35 of length tapers in z only; end width 1.7 in z |
| Head | x 30.8..31.4, y 1.2..3.0, z 24.3..27.7 |
| Rear tongue | x 28.3..30.1, y 0.3..4.5, z 22..30 |
| Tongue pocket | x 28.2..30.2, y 0.15..4.32, z 21.85..30.15 |
| Front cheeks | Nominal 1.2 along x; outer head recess reduces local bearing length |

Zero clearance describes matching CAD surfaces, not measured fit or a guarantee for other geometries. Insert the pin from the outer x side after the halves are seated.

## Print conditions and reuse

Bambu A1, 0.2 mm nozzle, PLA (brand/grade unrecorded), 0.10 mm layers, four walls, 15% gyroid, Arachne. Supports, brim and prime tower OFF. Single color.

Front exterior y=-6.1 and rear exterior y=6.1 face the bed. The pin lies on y=1.2 with its length parallel to the bed. Preserve these orientations and bed-to-hole distances for a close reproduction; the bore roofs are short bridges.

Reuse where one-time tight assembly and side access suit the design. Check the enclosing walls, insertion access and load direction when integrating. Do not claim hand assembly or loosen the pin automatically. Do not compare fit variants in a receiver already altered by forced insertion as though it were fresh.
