---
name: freecad-editable-printing
description: Design and revise functional parts intended for 3D printing, using human-editable FreeCAD models by default. Use for printable objects, enclosures, holders, mounts, assemblies, fit and support design, and slicer projects. Honor an explicitly requested CAD framework.
---

# Functional 3D printing

Deliver an editable `.FCStd` master, a configured slicer-project `.3mf`, a finished preview, and concise editing and printing instructions. Honor the user's requested output formats; provide additional exports when requested.

## Establish the setup

Use the current request first, then conversation history or available saved memory for printer, nozzle, material, and slicer preferences. Ask which slicer the user uses when the preference is missing or ambiguous. A printer brand or installed application alone is insufficient evidence of preference. Continue independent CAD work while awaiting answers.

Establish dimensions, mating interfaces, intended use, and critical loads. Distinguish measured dimensions, sourced specifications, and assumptions. Ask concise questions when missing information materially affects the design.

Discover FreeCAD's installation, version, and working Python API. Use its Python environment or a FreeCAD macro. Discover the selected slicer's supported interfaces when preparing the print project.

## Editable modeling

Use native bodies, constrained sketches, and standard features. Give features meaningful names and expose useful dimensions through spreadsheet aliases with units and descriptions. Drive mating parts from shared parameters; specify whether clearance is per side or total.

Fully constrain sketches where practical and explain intentional freedom. Prefer origin planes and expression-driven placements when they make revisions more stable. Document usable parameter relationships and check critical dimensions.

Treat human-edited CAD and slicer files as the starting point for revisions. Preserve those edits and save proposed revisions separately unless overwriting is requested.

The [enclosure example](scripts/build_enclosure.py) and [presentation helper](scripts/save_presentation.py) demonstrate this workflow. Copy both to a fresh output folder before running: they write beside themselves and replace previous example outputs. Complete preview and slicer-project preparation after generating the example CAD.

## Print settings and adhesion

Preserve user-specified settings. Recommend and apply suitable values for unspecified settings using compatible presets and part-specific adjustments. Explain consequential choices briefly and proceed with routine settings. Resolve conflicts between requested settings, geometry, and hardware with the user.

Ask about installed or available nozzles when detail or profile compatibility depends on them. Establish availability of a smaller nozzle before preparing a project around it. Apply the chosen settings to the slicer project.

Consider a brim explicitly for small contact areas, tall/narrow parts, thin upright edges, separate islands, and custom support fins. After an adhesion failure, revisit bed contact and brim settings alongside plate cleanliness, plate/material profiles, first-layer quality, temperature, and leveling as relevant.

Choose brim type, width, and object gap for the footprint, material, nozzle, plate, and removal needs. Inspect first-layer coverage, usable-bed clearance, and access for removal. Check that the brim anchors the intended parts and support bases.

## Strength and assemblies

Establish force direction, relevant magnitude, sustained or repeated loading, and attachment points. Consider bending, twisting, pull-out, and stress concentrations at holes, joints, corners, and thin transitions.

Orient critical loads favorably relative to layer strength. Use appropriate walls, ribs, gussets, fillets, and joints; check load transfer through fasteners and connections. Select material for temperature, sustained-load creep, and repeated flexing as applicable. Explain strength/printability tradeoffs and use physical tests to establish uncertain performance.

Break complex designs into components and develop them one at a time. Define shared dimensions, mating interfaces, clearances, and assembly order first. Check components individually, then verify alignment, interference, assembly access, and combined function.

Split physical prints when size, orientation, supports, material, maintenance, or assembly justify it. Design alignment and joining features with suitable tolerances. Group compatible parts across as many plates as needed, preserving intended dimensions, quantities, labels, orientation, and bed clearance. Use native multi-plate projects or separate projects according to the slicer's capabilities and setting scope. Report plate contents and assembly instructions.

## Typography and fine details

Choose fonts for the object's aesthetic, tone, and visual references. Consider weight, proportions, spacing, alignment, and the surrounding design. Preserve requested typography; use a focused question or comparison when it resolves a meaningful preference.

Assess actual stroke widths, serifs, gaps, enclosed openings, and relief depth against the nozzle, extrusion widths, layer height, and orientation. Small text may require a finer nozzle than 0.4 mm. Discuss a compatible smaller nozzle or changes to letter size, weight, or detail when needed.

Consider Arachne or an equivalent variable-width wall generator when available. Inspect sliced lettering for missing strokes, merged letters, closed openings, and lost inlay boundaries. Choose the mode that preserves the intended detail and report it. Use a lettering test piece when print quality remains uncertain.

## Multicolor efficiency

Plan color placement to reduce changes across layers. Compare orientations, accents confined to fewer layers, separate colored inserts, and batching compatible copies. Preserve appearance, fit, strength, and surface quality; resolve consequential assembly or aesthetic changes with the user.

When slicing is available, compare color/tool changes, flushed material, prime-tower material, and time. Report meaningful tradeoffs and distinguish estimates from measurements. Preserve appropriate purge and priming behavior. Evaluate flushing into infill/supports against color bleed, appearance, and material compatibility. Check printer clearances before using sequential object printing.

## Supports

Evaluate removal access alongside support coverage before choosing orientation and support settings. For normal, tree, and custom supports, trace where they start, what surfaces they touch, and how the user will grip, break, and extract them. Check tool clearance, narrow cavities, concealed interfaces, extraction openings, and likely damage or scarring on functional and decorative surfaces.

Compare build-plate-only support with support that starts on the part when removal access matters. Verify that the selected option still covers the overhangs; changing support type or restricting its origin does not by itself establish removability. Include removal effort and supported-surface quality when weighing reduced color waste against a different print orientation.

Explain the expected removal method and any awkward or uncertain areas before final delivery. Sliced coverage and contact gaps establish digital support conditions, not easy physical removal. For uncertain extraction or interfaces, propose a representative print test; revise the support layout or discuss orientation/assembly alternatives when access is inadequate.

Propose custom fin supports when they offer a clear advantage over normal/tree supports. Consider orientation and physical splitting as alternatives. Explain the benefit and removal tradeoff for the actual part.

Map unsupported islands and overhangs, then design sufficient fin coverage and spacing. Choose the contact gap for the material, nozzle, layer height, and removal method. Give each fin a continuous printable foundation, adequate base area, thickness, and bracing. Provide removal access and document intentional breakaway contacts.

Keep sacrificial geometry clearly labeled. Verify how the slicer handles each body: ordinary model geometry and support modifiers receive different treatment. Check for accidental merging, trapped supports, damage to fine features, and duplicate generated supports. Retain normal/tree support where needed for uncovered areas.

Inspect sliced paths from each fin's foundation through its final layer and the first supported part layer. Check stability, interface gap, coverage, and bridge spans. Use a representative support test when the interface is uncertain.

## Small physical tests

For uncertain fits or unusual functional features, propose a quick representative test piece: a lip section, hole/boss, clip, hinge, sliding interface, or support contact. Define success criteria and use the user's observations to refine the design.

Keep critical dimensions, clearances, walls, and functional geometry full-size. Save material by shortening the specimen or removing unrelated geometry. Match material, nozzle, layer height, orientation, and relevant settings. Preserve representative loading or flexing geometry and explain which aspects of the full assembly the specimen evaluates.

## Preview and check

For designs with important aesthetic choices, show a focused preview early enough for the user to steer the design, before finalizing detailed CAD and the print project. Show the intended font and text, proportions, color placement, and defining styling together. Use the actual geometry when available; label an earlier concept as a concept. Ask a targeted question when a consequential aesthetic choice remains open, and continue independent work while awaiting the answer.

Keep previews selective: combine useful views, skip featureless intermediate blocks, and show revisions when they change a meaningful choice. A final delivery preview complements the early aesthetic preview. Inspect other intermediate geometry internally and include an accurate finished preview at delivery.

Save, close, and reopen the native master. Recompute and check constraints, solids, dimensions, and errors. Exercise at least two meaningful parameter variants for parametric models, verify dependent parts, restore intended values, and save again.

Check mating clearance/interference and closed meshes where meshes are used. Render actual geometry and inspect cavities, walls, details, orientation, and proportions.

Persist presentation through FreeCAD's GUI API: show intended bodies and final tips, hide intermediate features, disable scripted camera animation, select an axonometric view, and fit visible parts. Reopen to verify visibility and camera persistence with numerical tolerance. The example helper uses Qt's offscreen platform for GUI metadata; inspect preview rendering separately.

## Slicer projects and delivery

Read the selected slicer's section of [slicer-projects.md](references/slicer-projects.md) for Bambu Studio, OrcaSlicer, PrusaSlicer, or UltiMaker Cura. Establish another slicer's native project workflow when requested.

Use the selected slicer's own save/export interface with compatible printer, physical nozzle, bed, material, and process profiles. Preserve multipart alignment, modifiers, and filament/extruder assignments. Reopen the result as a project and compare effective settings, orientation, and object structure. Inspect relevant toolpaths when slicing, especially text, adhesion, and custom supports.

Deliver `.FCStd`, configured `.3mf`, and preview as direct files. Include brief parameter-editing and assembly instructions. State nozzle, material, layer height, wall count, infill, supports on/off, brim on/off, and orientation in the response. Add brim width/gap when enabled, wall-generator mode, support details, and per-plate differences when relevant. For multicolor parts, include useful change/waste estimates and the design choices that reduce them.

Clearly distinguish saved settings from recommendations and digital checks from physical observations. If a required check or project-generation step is blocked, explain what remains and what is needed to finish it. Honor explicit CAD-only requests with the selected settings presented as recommendations to apply in the slicer.
