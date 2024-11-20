{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.zsh
    pkgs.poetry
    pkgs.gcc
    pkgs.libffi
    pkgs.cmake
  ];

  shellHook = ''
    # Ensure Poetry uses virtual environments in the project directory
    poetry config virtualenvs.in-project true --local

    # Reinstall dependencies
    poetry install

    # Ensure the correct libstdc++ path is in LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=${pkgs.gcc.cc.lib}/lib:$LD_LIBRARY_PATH

    # Activate the Poetry-managed virtual environment
    if [ -f .venv/bin/activate ]; then
      source .venv/bin/activate
    else
      echo "Virtual environment not found. Run 'poetry install' to create it."
    fi

    # Launch Zsh
    exec zsh
  '';
}

