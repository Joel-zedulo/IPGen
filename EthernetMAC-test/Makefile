# ==============================================================================
# Generic LiteX Standalone IP Generator
# ==============================================================================
# Usage:
#   make          -> Generates the Verilog core
#   make clean    -> Deletes the build folder
#
# Prerequisite: Ensure your LiteX venv is active!
#   . ~/LiteX_install/litex-venv/bin/activate
# ==============================================================================

# --- IP Configuration (Change these for QSPI/HyperBus) ---
GEN_TOOL  := liteeth_gen
CONFIG    := config.yaml
CORE_NAME := liteeth_core
# ---------------------------------------------------------

BUILD_DIR := ./build

.PHONY: all clean

all: $(CORE_NAME)

$(CORE_NAME):
	@echo "=================================================================="
	@echo " Generating $(CORE_NAME) using $(GEN_TOOL)"
	@echo "=================================================================="
	@command -v $(GEN_TOOL) >/dev/null 2>&1 || { echo "ERROR: '$(GEN_TOOL)' not found.\nPlease activate your LiteX venv first:\n  . ~/LiteX_install/litex-venv/bin/activate"; exit 1; }
	$(GEN_TOOL) $(CONFIG) --no-compile --output-dir $(BUILD_DIR) --name $(CORE_NAME)
	@echo "=================================================================="
	@echo "Success! Find your RTL at: $(CURDIR)/$(BUILD_DIR)/gateware/$(CORE_NAME).v"

clean:
	@echo "Cleaning $(BUILD_DIR)..."
	rm -rf $(BUILD_DIR)
