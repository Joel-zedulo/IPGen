# IPGen

Standalone LiteX IP core generation for Wishbone-based SoC integration.

Each subfolder is a self-contained IP generator with identical structure:

- `config.yaml` — Core parameters
- `gen.py` — Python generator (reads config, invokes LiteX)
- `Makefile` — Build system with venv check and auto dependency install
- `requirements.txt` — Extra Python dependencies (if needed)

## Available Cores

| Folder | Core | Bus | PHY |
|---|---|---|---|
| `EthernetMAC-test/` | LiteEth MAC | Wishbone | MII |
| `QSPI_Flash_Controller/` | QSPI NOR Flash Controller | Wishbone | QSPI x4 |
| `HyperMem_Controller/` | LiteHyperMem Controller | Wishbone | HyperRAM DDR |

## Usage

```bash
source ~/LiteX_install/litex-venv/bin/activate
cd <core_folder>
make                  # Build all three cores
make QSPI_Flash_Controller             # Build only QSPI flash controller
make clean            # Clean all cores
make help             # List targets
```

All cores use `vendor: lattice` for portable, vendor-neutral RTL output.
