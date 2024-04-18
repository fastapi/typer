import typer

app = typer.Typer(pretty_exceptions_width=120)


@app.command()
def main(name: str = "morty"):
    deep_dict_or_json = {
        "this_is_a_long_key": {
            "this_is_the_next_long_key": {
                "this_is_the_next_long_key": {
                    "this_is_the_next_long_key": {
                        "this_is_the_next_long_key": {
                            "this_is_the_next_long_key": {
                                "this_is_the_next_long_key": {
                                    "this_is_the_next_long_key": {
                                        "this_is_the_next_long_key": {
                                            "this_is_the_next_long_key": {
                                                "and_once_again_a_very_long_key": {
                                                    "but_this_is_not_the_end": {
                                                        "end": True
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    print(name + deep_dict_or_json + 3)


if __name__ == "__main__":
    app()
