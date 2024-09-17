{ pkgs, lib, config, inputs, ... }:

{

  # https://devenv.sh/packages/
  packages = [ pkgs.git ];

  # https://devenv.sh/languages/
  languages = {
    python = {
      enable = true;
      venv = {
        enable = true;
        requirements = ''
        -e .
        ${(builtins.readFile ./requirements-docs.txt)}
        ${(builtins.readFile ./requirements-tests.txt)}

        pre-commit >=2.17.0,<4.0.0
        '';
      };
    };
  };

  # https://devenv.sh/scripts/
  scripts = {
    format.exec = ''
    bash scripts/format.sh
    '';
    test.exec = ''
    bash scripts/test-cov-html.sh
    '';
  };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    format
    test
  '';

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
