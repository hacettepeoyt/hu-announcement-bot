#!/usr/bin/env python3

"""Ensures config defined config parameters in config.py are identical to the ones in the NixOS module."""

import ast
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class NoDefault:
    def __eq__(self, o: Any) -> bool:
        return isinstance(o, NoDefault)

    def __repr__(self) -> str:
        return "@NO_DEFAULT@"


class ComplicatedDefault:
    def __eq__(self, o: Any) -> bool:
        return isinstance(o, ComplicatedDefault)

    def __repr__(self) -> str:
        return "@COMPLICATED_DEFAULT@"


@dataclass(eq=True, order=True)
class ConfigKey:
    key: str
    default: Any


def parse_config_keys(module: ast.Module) -> list[ConfigKey]:
    keys: list[ConfigKey] = []

    for child in ast.walk(module):
        if isinstance(child, ast.Subscript):
            # config[key]
            if not isinstance(child.value, ast.Name) or child.value.id != "config":
                continue

            assert isinstance(child.slice, ast.Constant) and isinstance(child.slice.value, str)
            keys.append(ConfigKey(child.slice.value, NoDefault()))
        elif isinstance(child, ast.Call):
            # config.get(key, ...)
            if not isinstance(child.func, ast.Attribute) or child.func.attr != "get" or not isinstance(child.func.value, ast.Name) or child.func.value.id != "config":
                continue

            assert isinstance(child.args[0], ast.Constant) and isinstance(child.args[0].value, str)
            if len(child.args) == 2:
                # We have a default if we're here.
                try:
                    keys.append(ConfigKey(child.args[0].value, ast.literal_eval(child.args[1])))
                except ValueError:
                    # Literal eval might fail.
                    keys.append(ConfigKey(child.args[0].value, ComplicatedDefault()))
            else:
                keys.append(ConfigKey(child.args[0].value, NoDefault()))

    return keys


def parse_nix_keys(flake_path: Path) -> list[ConfigKey]:
    obj: dict[str, Any] = json.loads(subprocess.check_output([
        "nix", "eval", "--impure", "--json", "--expr", f'builtins.getFlake "{flake_path}"', "--apply",
        """flake: (
            builtins.mapAttrs (name: value:
                let eval = builtins.tryEval (value.default or { nodefault = true; });
                in if eval.success then eval.value else { complicateddefault = true; }
            ) (
                builtins.elemAt (
                    flake.outputs.nixosModules { lib = flake.inputs.nixpkgs.lib; config = throw "not full eval"; pkgs = {}; }).options.services.hu-announcement-bot.settings.type.getSubModules
                    0
                ).options
            )"""
    ], encoding="utf-8"))

    keys: list[ConfigKey] = []
    for key, default in obj.items():
        if isinstance(default, dict):
            if default.get("nodefault"):
                keys.append(ConfigKey(key, NoDefault()))
                continue
            elif default.get("complicateddefault"):
                keys.append(ConfigKey(key, ComplicatedDefault()))
                continue
        keys.append(ConfigKey(key, default))

    return keys


def main() -> bool:
    config_path: Path = Path(__file__).parents[1] / "src" / "config.py"

    config_keys: list[ConfigKey] = parse_config_keys(ast.parse(config_path.read_text()))
    config_keys.sort(reverse=True)
    config_key_set: set[str] = set(map(lambda c: c.key, config_keys))

    nix_keys: list[ConfigKey] = parse_nix_keys(Path(__file__).parents[1])
    nix_keys.sort(reverse=True)
    nix_key_set: set[str] = set(map(lambda c: c.key, nix_keys))

    if config_key_set != nix_key_set:
        print("ERROR: Either config and nix keys are not same.")

        if nix_key_set - config_key_set:
            print("       Following keys are present in flake.nix but not in config.py:")
            print("       - ", end="")
            print(*(nix_key_set - config_key_set), sep=', ')

        if config_key_set - nix_key_set:
            print("       Following keys are present in config.py but not in flake.nix:")
            print("       - ", end="")
            print(*(config_key_set - nix_key_set), sep=', ')

        return False

    for (config_key, nix_key) in zip(config_keys, nix_keys):
        if config_key.default != nix_key.default and nix_key.default != ComplicatedDefault():
            print("ERROR: Default mismatch:", "key:", config_key.key, "config.py:", config_key.default, "flake.nix:", nix_key.default)
            return False

    return True


if __name__ == "__main__":
    sys.exit(int(not main()))
