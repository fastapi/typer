import typer


def name_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if ctx.resilient_parsing:
        return
    typer.echo(f"Validating param: {param.name}")
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value


def main(name: str = typer.Option(..., callback=name_callback)):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
