# Scripted FreeCAD and Bambu export

Run `scripts/export_project.py` with ordinary Python. It launches FreeCAD's bundled Python and Bambu from the manifest. The worker needs FreeCAD, NumPy and Pillow (present in the tested FreeCAD 1.1 installation); the launcher uses only the standard library. This packages an existing editable FCStd. Geometry creation remains a separate project script or CAD edit.

## Manifest

Paths are absolute or relative to the manifest. Configure once and reuse. This is a minimal single-part example; select the user's actual profiles, nozzle and preferences.

```json
{
  "schema_version": 1,
  "source": "master.FCStd",
  "work": ".export",
  "freecad_python": "C:/Program Files/FreeCAD 1.1/bin/python.exe",
  "outputs": {
    "freecad": "exports/part.FCStd",
    "bambu": "exports/part.3mf",
    "preview": "exports/preview.png"
  },
  "preserve_objects": ["Body"],
  "design_intent": ["Preserve lettering and colors."],
  "presentation": {
    "objects": ["Body"],
    "colors": {"Body": [0.2, 0.3, 0.4]}
  },
  "objects": [{
    "name": "Part",
    "position": [100, 100],
    "parts": [{
      "object": "Body", "name": "Main body", "extruder": 1,
      "transform": [1,0,0, 0,1,0, 0,0,1, 0,0,0]
    }]
  }],
  "bambu": {
    "executable": "C:/Program Files/Bambu Studio/bambu-studio.exe",
    "machine": "profiles/machine.json",
    "process": "profiles/process.json",
    "filaments": ["profiles/filament.json"],
    "process_overrides": {"wall_loops": "4"},
    "expected_settings": {"nozzle_diameter": ["0.4"]},
    "slice": true,
    "forbidden_features": []
  }
}
```

Use complete compatible resolved profiles from the installed slicer. `process_overrides` specifies intentional process changes and exact serialized values (often strings); these must already match the process profile. They are verified and registered in `different_settings_to_system`. `expected_settings` verifies additional CLI-reopened values. Preserve filament/printer override markers from native export.

Each object is a print assembly; its parts share alignment and use one-based filament slots. Part names must be unique. Transforms follow 3MF's 12-number convention: output x = x*t0+y*t3+z*t6+t9 (similarly y/z). Use rigid rotations/translations, with part minimum z >= 0; assembly `position` supplies bed x/y translation. Upper accents may begin above z=0. Bambu checks plate feasibility; inspect the final layout and relevant paths.

Optional `mesh_deflection` defaults to 0.015 mm; `timeout_seconds` to 1800 per subprocess. `dependencies` adds files to cache invalidation. `presentation` controls output CAD visibility/colors and the software-rendered axonometric preview, not print orientation. `preserve_objects` checks existence only. `design_intent` guides the agent; visual review establishes actual appearance preservation.

## Run and inspect

```text
python <skill>/scripts/export_project.py <project>/print-project.json
python <skill>/scripts/export_project.py <project>/print-project.json --force
```

Use a separate output directory for each revision. Generated outputs may be replaced on rerun; treat human-edited outputs as a new source first. Source and output CAD must differ. Native 3MF is published only after checks pass. A failure can leave new CAD/preview in the output directory; do not deliver a mixed or failed run.

One final JSON line reports `ok`, `cached`, or `error`, paths, elapsed time and log location. Progress lives in `work/status.json`, solid/mesh results in `work/cad-checks.json`. Read only the tail of `work/export.log` on failure. Avoid short repeated polling. A lock prevents concurrent runs; remove a stale lock only after confirming no exporter is running.

Cache checks manifest, CAD, profiles, helper code, explicit dependencies, tool file metadata and output hashes. This establishes unchanged inputs, not token savings. Successful CLI logs stay out of model context. A routine export uses one invocation and a short result, with a completion wait for long jobs.

Checks cover exported solids, closed tessellations, CAD reopen/visibility, settings, named filament assignments, sliced-plate presence, and optional forbidden feature labels such as `Support` or `Brim`. They do not establish mechanism travel, all interference, all lettering strokes, strength, removability or desktop Open Project persistence. Apply additional checks only when relevant to the change. `slice:false` cannot validate toolpaths. This helper supports a single plate and normal parts; use native slicer workflows for modifiers, multiple plates, or other slicers.
