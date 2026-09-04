# ==============================================================================
# Generic LiteX Standalone IP Generator
# ==============================================================================

# --- IP Configuration ---
GEN_CMD   := python3 gen.py
# CORE_NAME: Change this to whatever you want the .v file to be named
CORE_NAME := hypermem_controller
# ------------------------

BUILD_DIR := ./build
CORE_FILE := $(BUILD_DIR)/gateware/$(CORE_NAME).v

.PHONY: all clean check_venv install_reqs test

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

# 2. Dependency injection: Install from requirements.txt if it exists
install_reqs: check_venv
	@if [ -f "requirements.txt" ]; then \
		echo "Installing dependencies from requirements.txt..."; \
		pip install -q --upgrade -r requirements.txt; \
	else \
		echo "No requirements.txt found, skipping dependency install."; \
	fi

# 3. Generation: Runs only AFTER dependencies are satisfied
$(CORE_NAME): $(CORE_FILE)

$(CORE_FILE): install_reqs
	@echo "=================================================================="
	@echo " Generating $(CORE_NAME)"
	@echo "=================================================================="
	CORE_NAME=$(CORE_NAME) $(GEN_CMD)
	@echo "=================================================================="
	@echo "Success! Find your RTL at: $(CURDIR)/$(BUILD_DIR)/gateware/$(CORE_NAME).v"

# 4. Simulation / Test target: Compiles core and primitives, checks compilation status
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
