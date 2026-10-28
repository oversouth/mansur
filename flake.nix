
{
  description = "Mansur Python + PostgreSQL + Docker environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python312;
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          python
          uv
          postgresql
          docker
          docker-compose
          git
          coreutils
          gnugrep
        ];

        shellHook = ''
          echo ""
          echo "=== Mansur development environment ==="

          # Python virtual environment
          if [ ! -x .venv/bin/python ]; then
            echo "Creating Python virtual environment..."
            uv venv .venv --python ${python}/bin/python || \
              echo "WARNING: Failed to create venv"
          fi

          if [ -x .venv/bin/python ]; then
            source .venv/bin/activate

            # Synchronize dependencies from requirements.txt
            if [ -f requirements.txt ]; then
              echo "Checking Python dependencies..."
              uv pip sync --python "$PWD/.venv/bin/python" \
                -r requirements.txt || \
                echo "WARNING: Dependency installation failed"
            fi

            python -m pip check 2>/dev/null || true
          fi

          # PostgreSQL configuration
          export PGDATA="$PWD/.nix-postgres"
          export PGHOST="$PWD/.nix-postgres-socket"
          export PGPORT=55432
          export PGUSER="$USER"
          export PGDATABASE=mansur_db

          mkdir -p "$PGHOST"
          chmod 700 "$PGHOST"

          # Initialize the database on first launch
          if [ ! -f "$PGDATA/PG_VERSION" ]; then
            echo "Initializing PostgreSQL..."

            if initdb -D "$PGDATA" \
              --auth-local=trust \
              --auth-host=reject \
              --no-locale; then
              echo "PostgreSQL initialized."
            else
              echo "WARNING: PostgreSQL initialization failed"
            fi
          fi

          # Start PostgreSQL if it isn't running
          if [ -f "$PGDATA/PG_VERSION" ]; then
            if ! pg_ctl -D "$PGDATA" status >/dev/null 2>&1; then
              echo "Starting PostgreSQL..."

              pg_ctl -D "$PGDATA" \
                -l "$PWD/.nix-postgres.log" \
                -o "-k $PGHOST -p $PGPORT -c listen_addresses="
                -w start || \
                echo "WARNING: PostgreSQL failed to start"
            fi

            # Create the project database if missing
            if pg_ctl -D "$PGDATA" status >/dev/null 2>&1; then
              if ! psql -d postgres -tAc \
                "SELECT 1 FROM pg_database WHERE datname = 'mansur_db'" \
                2>/dev/null | grep -q 1; then
                createdb mansur_db || \
                  echo "WARNING: Database creation failed"
              fi
            fi
          fi

          echo ""
          echo "=== Environment status ==="
          echo "Python: $(python --version 2>&1)"
          echo "PostgreSQL client: $(psql --version 2>&1)"
          echo "Docker: $(docker --version 2>&1)"
          echo ""
          echo "Database: $PGDATABASE"
          echo "Socket:   $PGHOST"
          echo "Port:     $PGPORT"
          echo ""
          echo "Run your application with: python main.py"
          echo "Exit with: exit"
          echo ""
        '';
      };
    };
}
