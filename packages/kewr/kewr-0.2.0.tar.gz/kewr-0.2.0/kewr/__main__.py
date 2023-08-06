import subprocess
import warnings
from pathlib import Path

import click
import yaml


def is_config_valid(data):
    NECESSARY_FORMAT = {
        "name": "str",
        "help": "str",
        "cmd": "str",
        "deps": [],
        "outs": [],
    }
    stages = data["stages"]
    try:
        for s in stages:
            if not all([i in s.keys() for i in NECESSARY_FORMAT.keys()]):
                return False
            for k, v in s.items():
                if not isinstance(v, type(NECESSARY_FORMAT[k])):
                    return False
        return True
    except Exception as e:
        print(f"config not valid, key error {e}")
        return False


def load_config():
    file_path = Path().cwd() / "kewr_config.yaml"
    try:
        with file_path.open(mode="rb") as file:
            data = yaml.safe_load(file)
        assert is_config_valid(data), "config format validation error"
        return data
    except FileNotFoundError as e:
        print(e)
    except AssertionError as e:
        print(e)


def check_dependencies(stage_data):
    return all([Path(d).exists() for d in stage_data["deps"]])


def check_outputs(stage_data):
    return all([Path(d).exists() for d in stage_data["outs"]])


def _run(cmd):
    subprocess.run(cmd, check=True)


@click.group()
def cli():
    """A simple python script runner"""
    pass


def run_stage(data, force):
    click.echo(f"Running stage {data['name']}")
    if (not check_outputs(data)) or force:
        assert check_dependencies(
            data
        ), f"Missing dependencies! Ensure dependencies {' '.join(data['deps'])} are present"
        command = data["cmd"].split()
        _run(command)
        assert check_outputs(
            data
        ), "Missing outputs! Stage did not complete successfully"
        click.echo(f"Stage {data['name']} completed successfully")
    else:
        click.echo(f"All stage outputs present, skipping stage {data['name']}")


EXAMPLE = """variables:
  var1: x

stages:
  - name: stage1
    help: "description of what the stage does"
    cmd: python ex.py
    deps: 
      - dla
    outs:
      - fjk
  - name: stage2
    help: "description of what the stage does"
    cmd: python ex.py
    deps: 
      - dla
    outs:
      - fjk
    """


@cli.command()
def create():
    """Create a new config"""
    out_path = Path().cwd() / "kewr_config.yaml"
    if out_path.exists():
        warnings.warn("config file already exists in this location", UserWarning)
    else:
        with open(out_path, "w") as file:
            file.write(EXAMPLE)
        click.echo("Created new config")


@cli.command()
def list():
    """List stages"""
    stages = load_config()["stages"]
    for s in stages:
        click.echo(f"{s['name']} : {s['help']}")


@cli.command()
@click.argument("stage", type=str, nargs=-1)
@click.option("-f", "--force", is_flag=True, help="force running of each stage")
def run(stage, force):
    """Run specified STAGE, or list of stages, or all stages with 'all'

    python -m kewr run stage_1         #runs stage_1 only

    python -m kewr run stage_1 stage_2 #runs stage_1 then stage_2

    python -m kewr run all             #runs all stages
    """
    stages = load_config()["stages"]
    all_stage_names = [i["name"] for i in stages]
    allowed_stages = all_stage_names + ["all"]
    false_stages = [s for s in stage if s not in allowed_stages]
    assert (
        not false_stages
    ), f"{false_stages} not a recognized stage, available stages are: {', '.join(allowed_stages)}"
    if "all" in stage:
        stages_to_run = all_stage_names
    else:
        stages_to_run = stage
    for s in stages:
        if s["name"] in stages_to_run:
            run_stage(s, force)


if __name__ == "__main__":
    cli()
