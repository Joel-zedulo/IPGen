# ==============================================================================
# IPGen - Top-Level Makefile
# ==============================================================================

CORES := EthernetMAC-test QSPI_Flash_Controller HyperMem_Controller

.PHONY: all clean help $(CORES)

all: $(CORES)

$(CORES):
	@echo "========================================"
	@echo " Building $@"
	@echo "========================================"
	$(MAKE) -C $@

clean:
	@for core in $(CORES); do \
		echo "Cleaning $$core..."; \
		$(MAKE) -C $$core clean; \
	done

help:
	@echo "Targets:"
	@echo "  make              Build all cores"
	@echo "  make <core>       Build specific core ($(CORES))"
	@echo "  make clean        Clean all cores"
	@echo "  make help         Show this help"
