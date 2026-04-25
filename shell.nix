{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    postgresql
    python311
    python311Packages.pip
    python311Packages.virtualenv
    stdenv.cc.cc.lib
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
    echo "[ OK ] Python 3.11"
    echo "[ OK ] PostgreSQL"
  '';
}