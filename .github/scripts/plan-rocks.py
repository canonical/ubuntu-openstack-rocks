#!/usr/bin/env python3
"""List checked-in ROCK recipes and group selected names by build variant."""

import argparse
import json
import re
from pathlib import Path


def list_recipes(root: Path) -> dict[str, list[tuple[str, Path]]]:
    rocks_dir = root / "rocks"
    if not rocks_dir.is_dir():
        raise ValueError(f"ROCK recipe directory does not exist: {rocks_dir}")

    recipes: dict[str, list[tuple[str, Path]]] = {}
    for path in sorted(rocks_dir.rglob("rockcraft.yaml")):
        parts = path.relative_to(rocks_dir).parts
        rock, directories = parts[0], parts[1:-1]
        if (
            len(parts) < 2
            or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", rock)
            or len(directories) > 1
            or (directories and not re.fullmatch(r"[0-9]{2}\.[0-9]{2}", directories[0]))
            or not path.is_file()
        ):
            raise ValueError(
                f"Unrecognized ROCK recipe path {path}. Expected "
                "rocks/<name>/rockcraft.yaml or rocks/<name>/<YY.MM>/rockcraft.yaml."
            )
        variant = directories[0] if directories else "primary"
        recipes.setdefault(rock, []).append((variant, path.parent))

    for rock, variants in recipes.items():
        if len(variants) > 1 and any(variant == "primary" for variant, _ in variants):
            raise ValueError(f"{rocks_dir / rock} defines both a root recipe and base directories")
    return recipes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--rocks", help="JSON list of ROCK names")
    args = parser.parse_args()
    try:
        recipes = list_recipes(args.root)
        names = json.loads(args.rocks) if args.rocks is not None else list(recipes)
        if not isinstance(names, list) or any(
            not isinstance(name, str) or name not in recipes for name in names
        ):
            raise ValueError("Expected a JSON list of ROCKs declared on the selected ref")
    except (OSError, ValueError) as error:
        parser.error(str(error))

    names = sorted(set(names))
    builds = {}
    releases = []
    for name in names:
        for variant, path in recipes[name]:
            builds.setdefault(variant, []).append(name)
            releases.append(
                {"rock": name, "variant": variant, "path": str(path.relative_to(args.root))}
            )

    print(json.dumps({
        "rocks": names,
        "builds": [{"variant": variant, "rocks": rocks} for variant, rocks in builds.items()],
        "releases": releases,
    }))


if __name__ == "__main__":
    main()
