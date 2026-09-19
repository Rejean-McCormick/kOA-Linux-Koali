"""Partition pytest commands; unrun VM tests are never passing evidence."""
from pathlib import Path


def is_qemu(command):
    return any(Path(item).name.startswith("test_qemu_") for item in command)


def partition(root, commands, required, scope):
    selected, omitted = [], []
    for command in commands:
        if command[1:3] != ["-m", "pytest"]:
            (omitted if scope == "qemu" else selected).append(command)
            continue
        options, local, qemu = [], [], []
        for item in command:
            path = root / item
            if item.startswith("tests/"):
                paths = sorted(path.rglob("test_*.py")) if path.is_dir() else [path]
                for test in paths:
                    relative = test.relative_to(root).as_posix()
                    (qemu if test.name.startswith("test_qemu_") else local).append(relative)
            else:
                options.append(item)
        for group, kind in ((local, "local"), (qemu, "qemu")):
            if group:
                (selected if scope in ("all", kind) else omitted).append([*options, *group])
    if scope == "local":
        required = [p for p in required if not Path(p).name.startswith("test_qemu_")]
    elif scope == "qemu":
        required = [item for command in selected for item in command if item.startswith("tests/")]
    return selected, required, omitted
