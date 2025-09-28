from shutil import rmtree

from click import command, option, pass_obj

from pokemanager.cli.utils import CLIRuntime


@command()
@option("-f", "--force", is_flag=True)
@pass_obj
def clean(rt: CLIRuntime, force: bool):
    """Clean your system of pokemanager files."""
    print("running clean")
    rt.verb("Cleaning...")

    if force:
        rt.vverb("Cleaning is forced!")
        rt.vverb("Deleting configuration...")
        rt.config_file.unlink(missing_ok=True)
        rt.vverb("Deleting application data...")
        rmtree(rt.appdata_path, ignore_errors=True)
        return

    while True:
        del_config = input("Delete configuration? (y/N): ").strip().lower() or "n"
        match del_config:
            case "y":
                rt.vverb("Deleting configuration...")
                rt.config_file.unlink(missing_ok=True)
                break
            case "n":
                break
            case _:
                continue

    while True:
        del_data = input("Delete application data? (y/N): ").strip().lower() or "n"
        match del_data:
            case "y":
                rt.vverb("Deleting application data...")
                rmtree(rt.appdata_path, ignore_errors=True)
                break
            case "n":
                break
            case _:
                continue

    rt.verb("Cleaning complete.")
