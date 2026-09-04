# ==============================================================================
# EthernetMAC-test Makefile
# ==============================================================================

# --- IP Configuration ---
GEN_TOOL  := liteeth_gen
CONFIG    := config.yaml
CORE_NAME := liteeth_core
# ------------------------

BUILD_DIR := ./build
CORE_FILE := $(BUILD_DIR)/gateware/$(CORE_NAME).v

.PHONY: all clean check_venv test

all: $(CORE_NAME)

# 1. Safety check: Fail fast if the user forgot to activate the venv
check_venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "ERROR: No active Python virtual environment detected."; \
		echo "Please activate your LiteX venv first:"; \
		echo "  . ~/LiteX_install/litex-venv/bin/activate"; \
		exit 1; \
	fi
	@echo "Venv active: $$VIRTUAL_ENV"

# 2. Generation target
$(CORE_NAME): $(CORE_FILE)

$(CORE_FILE): check_venv
	@echo "=================================================================="
	@echo " Generating $(CORE_NAME) using $(GEN_TOOL)"
	@echo "=================================================================="
	@command -v $(GEN_TOOL) >/dev/null 2>&1 || { echo "ERROR: '$(GEN_TOOL)' not found.\nPlease activate your LiteX venv first."; exit 1; }
	$(GEN_TOOL) $(CONFIG) --no-compile --output-dir $(BUILD_DIR) --name $(CORE_NAME)
	@echo "=================================================================="
	@echo "Success! Find your RTL at: $(CURDIR)/$(BUILD_DIR)/gateware/$(CORE_NAME).v"

# 3. Simulation / Test target: Compiles core and primitives, checks compilation status
test: check_venv
	@if [ ! -f "$(CORE_FILE)" ]; then \
		echo "Core RTL not found. Triggering build first..."; \
		$(MAKE) $(CORE_NAME); \
	fi
	@if iverilog -o sim_out -s $(CORE_NAME) $(CORE_FILE) ../../primitives/*.v; then \
		echo ""; \
		echo "=================================================================="; \
		echo "'$(CORE_NAME)' compilation SUCESSFUL!"; \
		echo "=================================================================="; \
	else \
		echo ""; \
		echo "=================================================================="; \
		echo "'$(CORE_NAME)' compilation FAILED!"; \
		echo "=================================================================="; \
		rm -f sim_out; \
		exit 1; \
	fi

clean:
	@echo "Cleaning $(BUILD_DIR)..."
	@rm -rf $(BUILD_DIR) sim_out
