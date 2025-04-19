import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Minecraft Backup Tool (CLI/GUI)"
    )
    parser.add_argument(
        "--gui", action="store_true", help="Executar interface gráfica"
    )
    args = parser.parse_args()

    if args.gui:
        from gui_main import run_gui

        run_gui()
    else:
        from cli_main import run_cli

        run_cli()


if __name__ == "__main__":
    main()
