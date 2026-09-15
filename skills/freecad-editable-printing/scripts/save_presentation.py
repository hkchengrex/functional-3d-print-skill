"""Persist and verify native FreeCAD visibility and camera; preserve geometry."""
from pathlib import Path
import json
import os
import re
import zipfile

# A GUI document is required even when the modeling process runs unattended.
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import FreeCAD as App
import FreeCADGui as Gui


def save_presentation(path):
    path = Path(path).resolve()
    Gui.showMainWindow()
    window = Gui.getMainWindow()
    window.resize(1400, 900)
    window.hide()
    doc = App.openDocument(str(path))
    before = {b.Name: b.Shape.Volume for b in (doc.Enclosure, doc.Lid)}
    for obj in doc.Objects:
        if obj.ViewObject is not None:
            obj.ViewObject.Visibility = False
    for body, color in [(doc.Enclosure, (0.23, 0.55, 0.71)),
                        (doc.Lid, (0.87, 0.61, 0.25))]:
        body.ViewObject.Visibility = True
        body.Tip.ViewObject.Visibility = True
        for obj in (body, body.Tip):
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.LineColor = (0.18, 0.23, 0.28)
            obj.ViewObject.DisplayMode = 'Flat Lines'
    doc.recompute()
    view = Gui.activeDocument().activeView()
    view.setAnimationEnabled(False)
    view.viewAxonometric()
    Gui.updateGui()
    view.fitAll()
    camera = view.getCamera()
    doc.save()
    App.closeDocument(doc.Name)
    with zipfile.ZipFile(path) as archive:
        assert 'GuiDocument.xml' in archive.namelist(), 'Missing GUI persistence'
        gui_xml = archive.read('GuiDocument.xml').decode()
        assert 'Camera' in gui_xml, 'Missing saved camera'
    doc = App.openDocument(str(path))
    reopened_camera = Gui.activeDocument().activeView().getCamera()
    visible = {}
    for body in (doc.Enclosure, doc.Lid):
        visible[body.Name] = bool(body.ViewObject.Visibility)
        visible[body.Tip.Name] = bool(body.Tip.ViewObject.Visibility)
        assert visible[body.Name] and visible[body.Tip.Name]
        assert abs(before[body.Name]-body.Shape.Volume) < 1e-6
    def numbers(value):
        return [float(n) for n in re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', value)]
    original, restored = numbers(camera), numbers(reopened_camera)
    assert len(original) == len(restored)
    assert all(abs(a-b) < 1e-5 for a,b in zip(original,restored)), 'Camera changed on reopening'
    assert float(re.search(r'height ([\d.]+)', reopened_camera)[1]) < 200, 'View is too distant for this example'
    report = {'gui_document_present': True, 'visible_after_reopen': visible,
              'camera_persisted_within_1e-5': True, 'camera': reopened_camera,
              'geometry_volumes_unchanged': True}
    (path.parent / 'presentation_validation.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    App.closeDocument(doc.Name)


if __name__ == '__main__':
    import sys
    save_presentation(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name('editable_enclosure.FCStd'))
