"""Check a PartCAD assembly for overlapping parts, cheapest checks first.

1. Export the placed assembly to STEP and compare every pair's bounding box.
   Pairs whose boxes don't meet can't overlap.
2. Measure exact overlap volumes for the candidate pairs that involve --parts.
3. With --full: measure all candidate pairs, then run
   `pc test --assembly -f interference` as the final gate.

Run it with a Python that has CadQuery's OCP, from anywhere in the repo:

    python hardware/tools/check_overlaps.py reactor-unit --list
    python hardware/tools/check_overlaps.py reactor-unit --parts 1/3/16 1/3/17
    python hardware/tools/check_overlaps.py heating-unit --full

The STEP export loses instance names, so parts are identified by their
position in the assembly tree (e.g. 1/3/16). The order follows the links
in the .assy files; use --list to see each part's bounding box.
"""

import argparse
import itertools
import subprocess
import sys
import tempfile
from pathlib import Path

from OCP.Bnd import Bnd_Box
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_Label, TDF_LabelSequence
from OCP.TDocStd import TDocStd_Document
from OCP.TopLoc import TopLoc_Location
from OCP.XCAFDoc import XCAFDoc_DocumentTool

REPO_ROOT = Path(__file__).resolve().parents[2]

# PartCAD's interference test uses the same floor to absorb boolean noise.
DEFAULT_MIN_VOLUME = 0.05


def export_step(pc, package, assembly, out_dir):
    subprocess.run(
        [pc, "--no-ansi", "export", "-a", "-t", "step", "-O", str(out_dir), f"{package}:{assembly}"],
        cwd=REPO_ROOT,
        check=True,
    )
    return Path(out_dir) / f"{assembly}.step"


def read_parts(step_path):
    """Return {tree path: placed shape} for every leaf part in the STEP file."""
    doc = TDocStd_Document(TCollection_ExtendedString("doc"))
    reader = STEPCAFControl_Reader()
    reader.ReadFile(str(step_path))
    reader.Transfer(doc)
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    parts = {}

    def walk(label, location, path):
        if tool.IsAssembly_s(label):
            components = TDF_LabelSequence()
            tool.GetComponents_s(label, components)
            for i in range(1, components.Length() + 1):
                component = components.Value(i)
                referred = TDF_Label()
                tool.GetReferredShape_s(component, referred)
                walk(referred, location * tool.GetLocation_s(component), path + [str(i)])
        else:
            parts["/".join(path)] = tool.GetShape_s(label).Moved(location)

    roots = TDF_LabelSequence()
    tool.GetFreeShapes(roots)
    for i in range(1, roots.Length() + 1):
        walk(roots.Value(i), TopLoc_Location(), [str(i)])
    return dict(sorted(parts.items(), key=lambda item: [int(p) for p in item[0].split("/")]))


def bounding_box(shape):
    box = Bnd_Box()
    BRepBndLib.Add_s(shape, box)
    return box.Get()


def boxes_meet(a, b):
    return not (a[0] > b[3] or b[0] > a[3] or a[1] > b[4] or b[1] > a[4] or a[2] > b[5] or b[2] > a[5])


def overlap_volume(a, b):
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(BRepAlgoAPI_Common(a, b).Shape(), props)
    return props.Mass()


def involves(key, prefixes):
    return any(key == p or key.startswith(p + "/") for p in prefixes)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("assembly", help="assembly name in the package, e.g. reactor-unit")
    parser.add_argument("--package", default="v6", help="PartCAD package (default: v6)")
    parser.add_argument("--step", help="use an existing STEP export instead of exporting")
    parser.add_argument("--parts", nargs="+", default=[], help="tree paths to check exactly, e.g. 1/3/16")
    parser.add_argument("--full", action="store_true", help="check all candidate pairs and run pc test")
    parser.add_argument("--list", action="store_true", help="print every part's bounding box")
    parser.add_argument("--min-volume", type=float, default=DEFAULT_MIN_VOLUME, help="mm^3 below which an overlap is noise")
    parser.add_argument("--pc", default="pc", help="PartCAD command (default: pc)")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        step = Path(args.step) if args.step else export_step(args.pc, args.package, args.assembly, tmp)
        parts = read_parts(step)

    boxes = {key: bounding_box(shape) for key, shape in parts.items()}
    if args.list:
        for key, b in boxes.items():
            print("%-14s x[%8.1f, %8.1f] y[%8.1f, %8.1f] z[%8.1f, %8.1f]" % (key, b[0], b[3], b[1], b[4], b[2], b[5]))

    candidates = [(a, b) for a, b in itertools.combinations(parts, 2) if boxes_meet(boxes[a], boxes[b])]
    print("tier 1: %d parts, %d of %d pairs have touching bounding boxes"
          % (len(parts), len(candidates), len(parts) * (len(parts) - 1) // 2))

    if args.full:
        pairs = candidates
    else:
        pairs = [(a, b) for a, b in candidates if involves(a, args.parts) or involves(b, args.parts)]
    if not pairs:
        print("tier 2: nothing to measure; pass --parts or --full")
        return 0

    print("tier %d: measuring %d candidate pairs" % (3 if args.full else 2, len(pairs)))
    found = 0
    for a, b in pairs:
        volume = overlap_volume(parts[a], parts[b])
        if volume > args.min_volume:
            found += 1
            print("  overlap %s x %s: %.2f mm^3" % (a, b, volume), flush=True)
    print("  %d overlapping pairs" % found)

    status = 1 if found else 0
    if args.full:
        print("tier 3: pc test --assembly -f interference %s:%s" % (args.package, args.assembly))
        test = subprocess.run(
            [args.pc, "--no-ansi", "test", "--assembly", "-f", "interference", f"{args.package}:{args.assembly}"],
            cwd=REPO_ROOT,
        )
        status = status or test.returncode
    return status


if __name__ == "__main__":
    sys.exit(main())
