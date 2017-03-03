{ stdenv, bash, python35 }:

stdenv.mkDerivation {
  name = "fznode";
  src = ./fznode;
  inherit python35;
  builder = builtins.toFile "builder.sh" ''
    source $stdenv/setup
    mkdir -p $out/bin
    sed "1c#!$python35/bin/python" $src > $out/bin/fznode
    chmod +x $out/bin/fznode
  '';
}
