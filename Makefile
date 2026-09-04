# Automatically discover any subdirectory inside the cores/ directory
CORES := $(notdir $(wildcard cores/*))

.PHONY: all clean test help $(CORES)

all: $(CORES)

# Forward any core target into the cores/ subdirectory
$(CORES):
	@if [ ! -d "cores/$@" ]; then \
		echo "ERROR: Core '$@' does not exist in cores/"; \
		exit 1; \
	fi
	@echo "========================================"
	@echo " Building core: $@"
	@echo "========================================"
	$(MAKE) -C cores/$@

clean:
	@for core in $(CORES); do \
		echo "Cleaning $$core..."; \
		$(MAKE) -C cores/$$core clean; \
	done

test:
	@for core in $(CORES); do \
		echo "Testing $$core..."; \
		$(MAKE) -C cores/$$core test; \
	done

help:
	@echo "Targets:"
	@echo "   make                Build all discovered cores"
	@echo "   make <core>         Build a specific core ($(CORES))"
	@echo "   make test           Test all discovered cores"
	@echo "   make clean          Clean all discovered cores"
	@echo "   make help           Show this help"
