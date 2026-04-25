{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    postgresql
    python311
    python311Packages.pip
    python311Packages.virtualenv
    python311Packages.psycopg2
  ];

  shellHook = ''
    echo "[ OK ] Python"
    echo "[ OK ] PostgreSQL"
  '';
}
