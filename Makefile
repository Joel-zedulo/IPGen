CORES := EthernetMAC-test QSPI_Flash_Controller HyperMem_Controller

.PHONY: all clean test help $(CORES)

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

test:
	@for core in $(CORES); do \
		echo "Testing $$core..."; \
		$(MAKE) -C $$core test; \
	done

help:
	@echo "Targets:"
	@echo "   make               Build all cores"
	@echo "   make <core>        Build specific core ($(CORES))"
	@echo "   make test          Test all cores"
	@echo "   make clean         Clean all cores"
	@echo "   make help          Show this help"
