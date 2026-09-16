# PLA sliding rail with a one-time latch

Read this when designing a comparable sliding joint with a one-time latch. This is a worked starting point, not a default for every clip.

## Use and limits

Use this short single-rail joint for one-time sliding assembly with a square retaining shoulder. The dovetail resists face separation; the latch prevents sliding withdrawal. No rated load, insertion force, cycle life or creep resistance is specified. Long rails and multiple-rail assemblies require their own alignment and friction checks.

## Reusable assets

- [Design parameters](../assets/sliding-latch/design-parameters.json): mechanical dimensions.

Use the profiles and dimensions below to construct native editable features. Preserve the contact profiles when adapting the mechanism. CAD and slicer outputs stay in the local project, outside the repository.

## Dimensions (mm)

| Feature | Value |
|---|---:|
| Free flap length, width, thickness | **22 x 10 x 1.4** |
| Flap root / free end, y coordinates | 14 / 36 |
| Tooth shoulder distance from root | **14** |
| Dovetail tongue engagement length | **13.5** |
| Nominal rail x clearance per side | **0.10** |
| Nominal tongue-to-channel floor gap | **0.10** |
| Crossbar width x / length along slide / height | **10.9 / 3.0 / 6.9** |
| Crossbar underside / flap surface, z | **1.4 / 1.4** |
| Nominal gap beneath crossbar | **0** |
| Nominal gap at either notch end | **0** |
| Nominal tooth engagement | **2.0** |

Zero gaps mean touching nominal CAD surfaces, not intentional material overlap. Specify fit for the mating geometry and material. The x clearance is measured horizontally at corresponding z values, not normal to the sloped faces.

## Geometry and axes

Coordinates: x across the joint, y along sliding, z through thickness.

- Base envelope: x=-6..13.6, y=0..42, floor z=0..2. Free leaf x=-5..5, y=14..36, thickness 1.4. Slots isolate the leaf; its root is at y=14.
- Tooth profile in (y,z): `(22,1.1), (26.5,3.4), (28,3.4), (28,1.1)`, extruded across x=-5..5. The sloped entry permits assembly; the y=28 face is the square retaining shoulder.
- Pad beyond the tooth: x=-5..5, y=31..36, z=1.1..3.2. The crossbar seats in the interval y=28..31. This is intended for one-time assembly.
- Crossbar: x=-5..5.9, y=28..31, z=1.4..8.3. It contacts the flap nominally and fills the notch lengthwise.
- Rail center x=9.8. Female cutter profile in (x offset,z): `(-2.5,2.3), (2.5,2.3), (1,3.8), (1,6.5), (-1,6.5), (-1,3.8)`. Cutter runs y=16..40; the housing top is z=6, with an end stop beyond y=40.
- Male profile: `(-2.3,2.4), (2.3,2.4), (0.9,3.8), (0.9,6.4), (-0.9,6.4), (-0.9,3.8)`, at the same center. Tongue runs y=16..29.5. The upper slider plate occupies z=6.3..8.3.

The dovetails resist separation normal to the faces; the square tooth/crossbar stop sliding withdrawal. Flap length and thickness control latch compliance; tightening rail clearance alone does not stiffen the flap.

## Assembly

The deep crossbar cannot be dragged over the thick root of the base. Place it **just past the root on the thin leaf**, with the tongue tip before the channel entrance, then feed the rail and slide toward the tooth. Start with slider y offset approximately **-13.75 mm**. The tongue length allows this starting placement. Check available placement access when integrating the joint into a larger assembly.

Hold the base at its sides with room beneath the leaf for insertion deflection. Check insertion deflection and root strain when changing the spring geometry. Do not assume repeated-use durability.

## Design constraints

Preserve the contact profiles, root-to-tooth distance and clearances when adapting the mechanism. Check placement access, sliding travel and spring deflection after dimensional changes. Multiple rails need sufficient alignment tolerance to avoid binding.
