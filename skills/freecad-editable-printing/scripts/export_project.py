"""Manifest-driven FreeCAD/Bambu export. Standard library only in this process."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import zipfile
from xml.etree import ElementTree as ET


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, data):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, indent=2), encoding='utf-8')
    temp.replace(path)


def run(manifest, force=False):
    manifest = Path(manifest).resolve()
    m = read(manifest)
    assert m.get('schema_version') == 1, 'Unsupported manifest schema_version'
    names = [p['name'] for obj in m['objects'] for p in obj['parts']]
    assert names and len(set(names)) == len(names), 'Part names must be nonempty and unique'
    root = manifest.parent
    resolve = lambda p: (root / p).resolve()
    work = resolve(m.get('work', '.export'))
    work.mkdir(parents=True, exist_ok=True)
    lock = work / 'export.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.close(fd)
    started = time.monotonic()
    status = work / 'status.json'
    report = {'status': 'running', 'stage': 'preflight', 'log': str(work / 'export.log')}
    def stage(name):
        report.update(stage=name, elapsed_seconds=round(time.monotonic()-started, 1))
        write(status, report)
    try:
        source = resolve(m['source'])
        cad = resolve(m['outputs']['freecad'])
        project = resolve(m['outputs']['bambu'])
        preview = resolve(m['outputs']['preview'])
        assert source != cad, 'Use a separate output CAD path to preserve the source.'
        outputs = [cad, project, preview]
        assert len(set(outputs)) == 3, 'Output paths must be distinct.'
        for path in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
        b = m['bambu']
        inputs = [manifest, source, Path(__file__), Path(__file__).with_name('freecad_export.py'), Path(__file__).with_name('render_preview.py')]
        inputs += [resolve(b[k]) for k in ('machine', 'process')]
        inputs += [resolve(p) for p in b['filaments']]
        inputs += [resolve(p) for p in m.get('dependencies', [])]
        h = hashlib.sha256()
        for p in inputs:
            h.update(str(p).encode()); h.update(p.read_bytes())
        for exe in (m['freecad_python'], b['executable']):
            p = resolve(exe); s = p.stat()
            h.update(f'{p}:{s.st_size}:{s.st_mtime_ns}'.encode())
        fingerprint = h.hexdigest()
        old = read(work/'result.json') if (work/'result.json').exists() else {}
        def hashes():
            return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}
        if not force and old.get('fingerprint') == fingerprint and all(p.exists() for p in outputs) and old.get('output_hashes') == hashes():
            report.update(status='cached', stage='complete', outputs=[str(p) for p in outputs])
            write(status, report)
            return report
        env = dict(os.environ, QT_QPA_PLATFORM='offscreen')
        with (work/'export.log').open('w', encoding='utf-8') as log:
            def command(args):
                subprocess.run([str(a) for a in args], cwd=work, env=env, stdout=log,
                               stderr=subprocess.STDOUT, check=True,
                               timeout=m.get('timeout_seconds', 1800),
                               creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            stage('freecad')
            command([resolve(m['freecad_python']), Path(__file__).with_name('freecad_export.py'), manifest])
            stage('bambu-export')
            executable = resolve(b['executable'])
            staged = work/'native.3mf'
            staged.unlink(missing_ok=True)
            args = [executable, '--load-settings', ';'.join(str(resolve(b[k])) for k in ('machine', 'process')),
                    '--load-filaments', ';'.join(str(resolve(p)) for p in b['filaments']), '--arrange', '0']
            if b.get('slice', True):
                args += ['--slice', '0']
            command(args + ['--export-3mf', staged, '--export-settings', work/'effective.json', work/'geometry.3mf'])
            stage('verify-settings')
            overrides = b.get('process_overrides', {})
            patched = work/'patched.tmp'
            with zipfile.ZipFile(staged) as src, zipfile.ZipFile(patched, 'w', zipfile.ZIP_DEFLATED) as dst:
                settings = json.loads(src.read('Metadata/project_settings.config'))
                markers = settings.get('different_settings_to_system', [])
                if not isinstance(markers, list):
                    raise ValueError('Unexpected Bambu override metadata type')
                if not markers:
                    markers = [''] * (len(b['filaments']) + 2)
                markers[0] = ';'.join(sorted(set(filter(None, markers[0].split(';'))) | set(overrides)))
                settings['different_settings_to_system'] = markers
                for k, v in overrides.items():
                    assert settings.get(k) == v, f'Exported setting mismatch: {k}'
                for item in src.infolist():
                    dst.writestr(item, json.dumps(settings) if item.filename == 'Metadata/project_settings.config' else src.read(item.filename))
            patched.replace(staged)
            reopened = work/'reopened.json'
            reopened.unlink(missing_ok=True)
            command([executable, '--export-settings', reopened, staged])
            effective = read(reopened)
            for k, v in {**b.get('expected_settings', {}), **overrides}.items():
                assert effective.get(k) == v, f'Reopened setting mismatch: {k}: {effective.get(k)!r} != {v!r}'
            with zipfile.ZipFile(staged) as z:
                config = ET.fromstring(z.read('Metadata/model_settings.config'))
                actual = {}
                for obj in config.findall('object'):
                    inherited = {e.get('key'): e.get('value') for e in obj.findall('metadata')}
                    for part in obj.findall('part') or [obj]:
                        meta = {**inherited, **{e.get('key'): e.get('value') for e in part.findall('metadata')}}
                        if 'name' in meta and 'extruder' in meta:
                            actual[meta['name']] = int(meta['extruder'])
                for obj in m['objects']:
                    for part in obj['parts']:
                        assert actual.get(part['name']) == part['extruder'], f'Missing/changed filament assignment: {part["name"]}'
                gcodes = [n for n in z.namelist() if n.endswith('.gcode')]
                if b.get('slice', True):
                    assert gcodes, 'Native project contains no sliced plate'
                for name in gcodes:
                    text = z.read(name).decode('utf-8', errors='replace')
                    for feature in b.get('forbidden_features', []):
                        assert not any(line.startswith('; FEATURE:') and feature.lower() in line.lower() for line in text.splitlines()), f'Unexpected {feature} toolpaths'
            stage('publish')
            staged.replace(project)
            (work/'geometry.3mf').unlink(missing_ok=True)
            report.update(status='ok', stage='complete', fingerprint=fingerprint,
                          output_hashes=hashes(), outputs=[str(p) for p in outputs],
                          desktop_verified=False, elapsed_seconds=round(time.monotonic()-started, 1))
            write(work/'result.json', report)
            write(status, report)
            return report
    except Exception as exc:
        report.update(status='error', error=str(exc), elapsed_seconds=round(time.monotonic()-started, 1))
        write(status, report)
        raise
    finally:
        lock.unlink(missing_ok=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest'); p.add_argument('--force', action='store_true')
    a = p.parse_args()
    try:
        result = run(a.manifest, a.force)
        print(json.dumps({k: v for k, v in result.items() if k not in ('fingerprint', 'output_hashes')}))
    except Exception as exc:
        print(json.dumps({'status': 'error', 'error': str(exc), 'hint': 'Read work/status.json and the end of work/export.log.'}))
        sys.exit(1)
