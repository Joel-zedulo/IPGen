# IPGen

Standalone LiteX IP core generation for Wishbone-based SoC integration.

Each subfolder is a self-contained IP generator with identical structure:

- `config.yaml` — Core parameters
- `gen.py` — Python generator (reads config, invokes LiteX)
- `Makefile` — Build system with venv check, auto dependency install, and simulation tests
- `requirements.txt` — Extra Python dependencies (if needed)

Shared components like vendor-agnostic I/O buffers and primitives are maintained centrally under `primitives/`.

## Available Cores

| Folder | Core | Bus | PHY |
|---|---|---|---|
| `EthernetMAC-test/` | LiteEth MAC | Wishbone | MII |
| `QSPI_Flash_Controller/` | QSPI NOR Flash Controller | Wishbone | QSPI x4 |
| `HyperMem_Controller/` | LiteHyperMem Controller | Wishbone | HyperRAM DDR |

## Usage

Run commands from the **root** directory of the project:

```bash
source ~/LiteX_install/litex-venv/bin/activate

make                  # Build all cores
make <core_folder>    # Build a specific core (e.g., make QSPI_Flash_Controller)
make test             # Build and run iverilog compilation/simulation checks on all cores
make clean            # Clean build artifacts for all cores
make help             # List all available root targets

```

## Architecture
IPGen/
├── cores/
│   ├── EthernetMAC-test/
│   ├── QSPI_Flash_Controller/
│   ├── HyperMem_Controller/
│   ├── Hyperflash_Controller/
│   └── OSPI_Flash_Controller/
├── primitives/
└── Makefile

All cores utilize standard Xilinx-targeted primitives natively resolved and verified during compilation checks via the shared `primitives/` library.
