# Slicer project workflows

Select the slicer from the current request, then conversation history or saved memory. Ask when the preference is unknown or ambiguous. Use the matching workflow below with the installed application's supported interfaces.

Preserve user-specified settings and choose compatible values for the rest. Confirm hardware details when they affect profiles or fine features. Group compatible parts onto plates with sufficient spacing, and use separate projects when nozzle or process differences require them.

## Bambu Studio

Use Save Project or the supported CLI project exporter to create `.3mf`. The CLI provides `--load-settings`, `--load-filaments`, and `--export-3mf`; load complete machine/process and filament configurations and verify options against the installed version.

Preserve assembly alignment and assign each part's filament slot. Inspect `Metadata/project_settings.config` and `Metadata/model_settings.config` as supplemental evidence, then reopen the project to verify effective settings and part assignments.

Preserve preset-override metadata as well as setting values. In Bambu projects, `different_settings_to_system` records semicolon-separated setting keys in this order: process, each filament, printer. Register the intended process overrides in the first entry, preserve the other entries, and check that the native exporter retains them. An empty override list can let desktop preset loading replace custom values even when command-line slicing uses them correctly. Pin the intended overrides rather than every field in a resolved system preset.

Verify desktop Open Project behavior for settings persistence; a command-line reopen or successful slice alone does not establish it. Check walls, infill density/pattern, wall generator, supports and gaps, and brim against the delivered settings. If desktop verification is unavailable, explicitly report that limit and request a focused user check. Preserve a user-saved project and its material/preset choices when repairing metadata; save the correction separately and identify any restored values.

Source: [Bambu Studio CLI](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage).
Preset-loading behavior: [PresetBundle.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PresetBundle.cpp), [Preset.cpp](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/Preset.cpp).

## OrcaSlicer

Use File > Save Project for `.3mf` and File > Open Project to restore it. CLI automation can use `--export-3mf` with settings-loading options confirmed through the installed help.

Check printer/nozzle, process values, filament slots, part assignments, modifiers, and plate placement. Resolve profile differences when starting from another slicer's file and save a native Orca project.

Sources: [Import/export](https://github.com/OrcaSlicer/OrcaSlicer/wiki/import_export), [CLI actions](https://github.com/OrcaSlicer/OrcaSlicer/wiki/cli_actions).

## PrusaSlicer

Use File > Save Project as to create `.3mf` with objects, settings, and modifiers. Reopen the complete project and verify printer/nozzle, print and filament settings, per-object overrides, supports, and extruder assignments.

For automation, inspect the installed CLI help and verify effective configuration values after export. Use the GUI save route when it provides more reliable preservation of project settings.

Source: [Saving projects](https://help.prusa3d.com/article/saving-projects-as-3mf_1773).

## UltiMaker Cura

Use Save Project and Cura's project `.3mf` format, sometimes named `.curaproject.3mf`. Reopen with the project's configuration and verify printer definition, nozzle/variant, material, quality, overrides, extruder assignments, modifiers, and placement.

Use Cura's own project writer or an automation path that preserves the full project. Resolve required custom definitions, materials, or plugins, then recheck effective settings after import or migration.

Sources: [Cura project writer](https://github.com/Ultimaker/Cura/blob/main/plugins/3MFWriter/ThreeMFWriter.py), [Project-saving guidance](https://community.ultimaker.com/topic/34783-3d-print-coming-out-mesh-like/).

## Check and deliver

For a newly exported plate/project, verify settings persistence in the target slicer; reuse that evidence when the project and relevant inputs are unchanged. Check actual setting values and inspect relevant layers: brim coverage and bed clearance; lettering strokes and gaps; fin foundations, interfaces, and supported overhangs. Confirm how custom fins are interpreted as model bodies or modifiers.

When changing multicolor layout or optimizing waste, compare color changes, flushed/tower material, and time estimates across useful layouts. Preserve suitable purge behavior and check appearance/material compatibility for flushing into infill or supports.

Deliver the configured 3MF alongside the CAD master and preview. Record nozzle, material, layer height, walls, infill, supports, brim, and orientation in the project manifest or guide; summarize changed settings in chat. Include brim width/gap, wall-generator mode, plate differences, and waste estimates when applicable. Identify the target slicer and distinguish recommendations from saved settings. Explain any remaining application check or project-generation blocker and the step needed to complete it.
