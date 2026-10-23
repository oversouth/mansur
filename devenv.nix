{ pkgs, ... }: {
  # 1. Python configuration
  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ./requirements.txt; 
    };
  };
  # 2. PostgreSQL Service
  # This spins up an isolated postgres instance inside your project shell automatically
  services.postgres = {
    enable = true;
    initialDatabases = [
      { name = "mansur_db"; }
    ];
  };
# Docker setup,not as a service since without a service it can work rootless
  packages = [
    pkgs.docker
    pkgs.docker-compose
  ];

}
