# Physically accepted PLA rail-and-latch reference: A

Read this when designing a comparable sliding joint with a one-time latch, or when a user asks to reuse the successful cardholder clip. This is a worked starting point, not a default for every clip.

## Evidence and scope

Recorded 2026-09-15. After printing the short-flap A/B coupon, the user reported **"A works well"** and selected A. This is qualitative physical acceptance of **A, the one-dot slider**, on the matching short-flap base. B was not selected or reported successful. Earlier, longer-flap and looser-clearance variants were not the accepted reference.

The test covers a short single-rail coupon intended for one-time assembly. It does not establish a rated load, insertion force, cycle life, creep resistance, environmental performance, two-rail alignment, long-rail friction, or the complete cardholder. Do not describe those as validated. The full holder still requires integration and fit checks.

## Reusable assets

- [Editable accepted A model](../assets/slide-latch-a/accepted-a.FCStd): native sketches, pads, pockets and parameter sheet; only the base and A slider remain. Copy before editing. Finished bodies are `RailBase` and `RailSlider`.
- [Test record](../assets/slide-latch-a/test-record.json): dimensions, print setup and exact scope of the user report. It is not an export manifest.

Use the model as the dimensional authority. Do not regenerate it from screenshots or conflate A with an earlier coupon. Preserve the constrained profiles when adapting it. Some sketches use Block constraints; release/edit those deliberately. The parameter sheet is not a guarantee that arbitrary dimension combinations work.

## Print conditions of the accepted coupon

Bambu A1, physical **0.2 mm nozzle**, PLA (brand/grade unrecorded), **0.10 mm layers**, four walls, 15% gyroid, Arachne. Supports, brim and prime tower OFF. One material/color; the single recessed dot identifies A.

Base prints on its broad exterior face at z=0, with the spring/channel upward. Slider prints upside down on its flat exterior face at z=8.3, with tongue/crossbar building upward. Both orientations keep the long spring direction in the layer plane. These are part-specific conditions, not universal PLA settings.

## Accepted dimensions (mm)

| Feature | Value |
|---|---:|
| Free flap length, width, thickness | **22 x 10 x 1.4** |
| Flap root / free end, y coordinates | 14 / 36 |
| Tooth shoulder distance from root | **14** (not the full 22 mm free length) |
| Dovetail tongue engagement length | **13.5** |
| Nominal rail x clearance per side | **0.10** |
| Nominal tongue-to-channel floor gap | **0.10** |
| Crossbar width x / length along slide / height | **10.9 / 3.0 / 6.9** |
| Crossbar underside / flap surface, z | **1.4 / 1.4** |
| Nominal gap beneath crossbar | **0** |
| Nominal gap at either notch end | **0** |
| Nominal tooth engagement | **2.0** |

Zero gaps mean touching nominal CAD surfaces, not intentional material overlap. Printed dimensions were not measured. The user's successful fit does not make zero clearance universally transferable to another printer, nozzle, material, orientation or joint length. The x clearance is measured horizontally at corresponding z values, not normal to the sloped faces.

## Geometry and axes

Native coordinates: x across the coupon, y along sliding, z through thickness. Dimensions below capture the functional profiles; inspect the native model for support geometry.

- Base envelope: x=-6..13.6, y=0..42, floor z=0..2. Free leaf x=-5..5, y=14..36, thickness 1.4. Slots isolate the leaf; its root is at y=14.
- Tooth profile in (y,z): `(22,1.1), (26.5,3.4), (28,3.4), (28,1.1)`, extruded across x=-5..5. The sloped entry permits assembly; the y=28 face is the square retaining shoulder.
- Pad beyond the tooth: x=-5..5, y=31..36, z=1.1..3.2. The crossbar seats in the interval y=28..31. Although a pad remains, easy disassembly was explicitly not a requirement.
- Crossbar: x=-5..5.9, y=28..31, z=1.4..8.3. It contacts the flap nominally and fills the notch lengthwise.
- Rail center x=9.8. Female cutter profile in (x offset,z): `(-2.5,2.3), (2.5,2.3), (1,3.8), (1,6.5), (-1,6.5), (-1,3.8)`. Cutter runs y=16..40; the housing top is z=6, with an end stop beyond y=40.
- Male profile: `(-2.3,2.4), (2.3,2.4), (0.9,3.8), (0.9,6.4), (-0.9,6.4), (-0.9,3.8)`, at the same center. Tongue runs y=16..29.5. The upper slider plate occupies z=6.3..8.3.

The dovetails resist separation normal to the faces; the square tooth/crossbar stop sliding withdrawal. The broad, shorter flap was selected after the user disliked motion in the longer flap. Tightening rail clearance alone did not address that complaint.

## Assembly constraint worth preserving

The deep crossbar cannot be dragged over the thick root of the base. Place it **just past the root on the thin leaf**, with the tongue tip before the channel entrance, then feed the rail and slide toward the tooth. In the coupon this starts with slider y offset approximately **-13.75 mm**. The tongue was shortened specifically to allow this starting placement. Check available placement access when integrating the joint into a larger assembly.

Hold the base at its sides with room beneath the leaf for insertion deflection. A lowered-tooth envelope was checked digitally, but no beam deformation simulation or force measurement was performed. One-time assembly acceptance does not establish repeated-use durability.

## Reuse efficiently

Start with this geometry when the load direction and assembly access suit it. Preserve the contact profiles, root-to-tooth distance, print orientation and clearances for a close reproduction. If those change, check the affected sliding/placement paths and spring behavior; use a representative local test where uncertainty remains. Do not silently apply this zero-gap joint to every clip.

Use a shorter single-rail coupon before printing a complete assembly. Keep variants physically identifiable (A used one recessed dot). For irreversible catches, one base cannot independently test multiple fully locked variants; compare partial rail fit first or provide separate bases when full comparisons are required. Reuse the scripted export pipeline and compact reports rather than rewriting FreeCAD/Bambu packaging code.
