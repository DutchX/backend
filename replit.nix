{ pkgs }: {
    deps = [
      pkgs.libev
      pkgs.cowsay
    ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.libev
    ];
  };
}