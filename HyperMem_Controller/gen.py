import yaml
import sys
import os

from migen import *
from litex.build.generic_platform import *
from litex.build.lattice.platform import LatticePlatform
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.interconnect import wishbone
from litex.soc.integration.soc import SoCRegion

try:
    from litehyperbus.core.hyperbus import HyperRAM
except ImportError:
    print("Could not import HyperRAM. Ensure litehyperbus is installed.")
    sys.exit(1)

_io = [
    ("sys_clock", 0, Pins(1)),
    ("sys_reset", 1, Pins(1)),

    ("bus", 0,
        Subsignal("adr",   Pins(30)),
        Subsignal("dat_w", Pins(32)),
        Subsignal("dat_r", Pins(32)),
        Subsignal("sel",   Pins(4)),
        Subsignal("cyc",   Pins(1)),
        Subsignal("stb",   Pins(1)),
        Subsignal("ack",   Pins(1)),
        Subsignal("we",    Pins(1)),
        Subsignal("cti",   Pins(3)),
        Subsignal("bte",   Pins(2)),
        Subsignal("err",   Pins(1)),
    ),

    ("hyperbus", 0,
        Subsignal("cs_n",   Pins(1)),
        Subsignal("clk_p",  Pins(1)),
        Subsignal("clk_n",  Pins(1)),
        Subsignal("rwds",   Pins(1)),
        Subsignal("dq",     Pins(8)),
        Subsignal("rst_n",  Pins(1)),
    ),
]

class HyperBusSoC(SoCMini):
    def __init__(self, platform, core_config):
        clk_freq = int(float(core_config["clk_freq"]))
        SoCMini.__init__(self, platform, clk_freq=clk_freq)

        self.submodules.crg = CRG(platform.request("sys_clock"), platform.request("sys_reset"))

        pads = platform.request("hyperbus")
        self.submodules.hyperbus = HyperRAM(pads=pads)

        wb = wishbone.Interface()
        platform.add_extension(wb.get_ios("bus"))
        self.comb += wb.connect_to_pads(self.platform.request("bus"), mode="slave")
        self.bus.add_master(master=wb)

        self.bus.add_slave("hyperbus", self.hyperbus.bus, SoCRegion(
            origin = 0x10000000,
            size   = 0x10000000,
            cached = False
        ))

def main():
    try:
        with open("config.yaml") as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        sys.exit("Error: config.yaml not found")

    vendor = cfg.get("vendor", "lattice")
    device = cfg.get("device", "")

    if vendor == "lattice":
        platform = LatticePlatform(device, io=[], toolchain="diamond")
    elif vendor == "xilinx":
        from litex.build.xilinx.platform import XilinxPlatform
        platform = XilinxPlatform(device, io=[], toolchain="vivado")
    else:
        sys.exit(f"Unsupported vendor: {vendor}")

    platform.add_extension(_io)

    soc = HyperBusSoC(platform, cfg)

    builder = Builder(soc, output_dir="./build", compile_gateware=False, compile_software=False)

    core_name = os.environ.get("CORE_NAME", "hypermem_controller")

    builder.build(build_name=core_name)

if __name__ == "__main__":
    main()














#import yaml
#import sys
#import os
#
#from migen import *
#from litex.build.generic_platform import *
#from litex.build.xilinx.platform import XilinxPlatform
#from litex.soc.integration.soc_core import *
#from litex.soc.integration.builder import *
#from litex.soc.interconnect import wishbone
#from litex.soc.integration.soc import SoCRegion
#
#try:
#    from litehyperbus.core.hyperbus import HyperRAM
#except ImportError:
#    print("Could not import HyperRAM. Ensure litehyperbus is installed.")
#    sys.exit(1)
#
#_io = [
#    ("sys_clock", 0, Pins(1)),
#    ("sys_reset", 1, Pins(1)),
#
#    ("bus", 0,
#        Subsignal("adr",   Pins(30)),
#        Subsignal("dat_w", Pins(32)),
#        Subsignal("dat_r", Pins(32)),
#        Subsignal("sel",   Pins(4)),
#        Subsignal("cyc",   Pins(1)),
#        Subsignal("stb",   Pins(1)),
#        Subsignal("ack",   Pins(1)),
#        Subsignal("we",    Pins(1)),
#        Subsignal("cti",   Pins(3)),
#        Subsignal("bte",   Pins(2)),
#        Subsignal("err",   Pins(1)),
#    ),
#
#    ("hyperbus", 0,
#        Subsignal("cs_n",   Pins(1)),
#        Subsignal("clk_p",  Pins(1)),
#        Subsignal("clk_n",  Pins(1)),
#        Subsignal("rwds",   Pins(1)),
#        Subsignal("dq",     Pins(8)),
#        Subsignal("rst_n",  Pins(1)),
#    ),
#]
#
#class HyperBusSoC(SoCMini):
#    def __init__(self, platform, core_config):
#        clk_freq = int(float(core_config["clk_freq"]))
#        SoCMini.__init__(self, platform, clk_freq=clk_freq)
#
#        self.submodules.crg = CRG(platform.request("sys_clock"), platform.request("sys_reset"))
#
#        pads = platform.request("hyperbus")
#        self.submodules.hyperbus = HyperRAM(pads=pads)
#
#        wb = wishbone.Interface()
#        platform.add_extension(wb.get_ios("bus"))
#        self.comb += wb.connect_to_pads(self.platform.request("bus"), mode="slave")
#        self.bus.add_master(master=wb)
#
#        # Aligned to 256MB to avoid CSR collision at 0x0
#        self.bus.add_slave("hyperbus", self.hyperbus.bus, SoCRegion(
#            origin = 0x10000000,
#            size   = 0x10000000,
#            cached = False
#        ))
#
#def main():
#    try:
#        with open("config.yaml") as f:
#            cfg = yaml.safe_load(f)
#    except FileNotFoundError:
#        sys.exit("Error: config.yaml not found")
#
#    platform = XilinxPlatform(cfg.get("device", ""), io=[], toolchain="vivado")
#    platform.add_extension(_io)
#
#    soc = HyperBusSoC(platform, cfg)
#
#    builder = Builder(soc, output_dir="./build", compile_gateware=False, compile_software=False)
#
#    # Grab the name directly from the Makefile environment variable
#    core_name = os.environ.get("CORE_NAME", "litehyperbus_core")
#
#    builder.build(build_name=core_name)
#
#if __name__ == "__main__":
#    main()
