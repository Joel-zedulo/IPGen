#import yaml
#import os
#import sys
#from migen import *
#from litex.build.xilinx.platform import XilinxPlatform  # <-- Use a platform with a build backend
#from litex.soc.integration.soc_core import SoCCore
#from litex.soc.integration.builder import Builder
#from litex.soc.integration.soc import SoCRegion
#from litespi import LiteSPI
#from litespi.phy.generic import LiteSPIPHY
#from litespi.modules import MX25LM51245
#from litespi.opcodes import SpiNorFlashOpCodes as Codes
#
#def main():
#    core_name = os.environ.get("CORE_NAME", "ospi_flash_controller")
#    
#    try:
#        with open("config.yaml") as f:
#            cfg = yaml.safe_load(f)
#    except FileNotFoundError:
#        sys.exit("Error: config.yaml not found")
#
#    platform = XilinxPlatform(device="", io=[])
#
#    class OSPISoC(SoCCore):
#        def __init__(self, platform):
#            SoCCore.__init__(self, platform, 
#                             clk_freq=cfg.get("clk_freq", 50000000), 
#                             cpu_type=None, 
#                             ident="OSPI Controller", 
#                             uart_name="crossover")
#            
#            flash_module = MX25LM51245(Codes.READ_1_1_8)
#            
#            pads = Record([
#                ("cs_n", 1),
#                ("clk",  1),
#                ("dq",   8)
#            ])
#            
#            self.submodules.sfi_phy = LiteSPIPHY(
#                pads=pads,
#                flash=flash_module,
#                mode=cfg.get("mode", "x4"),
#                clk_freq=cfg.get("clk_freq", 50000000)
#            )
#            
#            self.submodules.sfi_core = LiteSPI(
#                phy=self.sfi_phy,
#                mmap_endianness="big",
#                with_master=False,
#                with_mmap=True,
#                with_csr=True
#            )
#            
#            self.bus.add_slave("sfi_core", self.sfi_core.bus, SoCRegion(origin=0x08000000, size=0x04000000))
#
#    soc = OSPISoC(platform)
#    builder = Builder(soc, output_dir="build", compile_gateware=True)
#    builder.build(build_name=core_name)
#
#if __name__ == "__main__":
#    main()


import yaml
import os
import sys
from migen import *
from litex.build.xilinx.platform import XilinxPlatform
from litex.build.generic_platform import Pins
from litex.soc.integration.soc_core import SoCCore
from litex.soc.integration.builder import Builder
from litex.soc.integration.soc import SoCRegion
from litespi import LiteSPI
from litespi.phy.generic import LiteSPIPHY
from litespi.modules import MX25LM51245
from litespi.opcodes import SpiNorFlashOpCodes as Codes

class _CRG(Module):
    def __init__(self, platform, clk_freq):
        self.rst = Signal()
        self.clock_domains.cd_sys = ClockDomain()
        
        sys_clk = platform.request("sys_clk")
        
        # Simple clock and reset buffering
        self.comb += self.cd_sys.clk.eq(sys_clk)
        self.comb += self.cd_sys.rst.eq(self.rst)

def main():
    core_name = os.environ.get("CORE_NAME", "ospi_flash_controller")
    
    try:
        with open("config.yaml") as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        sys.exit("Error: config.yaml not found")

    clk_freq = cfg.get("clk_freq", 50000000)

    io = [
        ("sys_clk", 0, Pins(1))
    ]

    platform = XilinxPlatform("", io=io, toolchain="vivado")
    platform.add_platform_command("create_clock -name sys_clk -period {:.3f} [get_ports sys_clk]".format(1e9 / clk_freq))

    class OSPISoC(SoCCore):
        def __init__(self, platform):
            SoCCore.__init__(self, platform, 
                             clk_freq=clk_freq, 
                             cpu_type=None, 
                             ident="OSPI Controller", 
                             uart_name="crossover")
            
            self.submodules.crg = _CRG(platform, clk_freq)

            flash_module = MX25LM51245(Codes.READ_1_1_8)
            
            pads = Record([
                ("cs_n", 1),
                ("clk",  1),
                ("dq",   8)
            ])
            
            self.submodules.sfi_phy = LiteSPIPHY(
                pads=pads,
                flash=flash_module,
                mode=cfg.get("mode", "x4"),
                clk_freq=clk_freq
            )
            
            self.submodules.sfi_core = LiteSPI(
                phy=self.sfi_phy,
                mmap_endianness="big",
                with_master=False,
                with_mmap=True,
                with_csr=True
            )
            
            self.bus.add_slave("sfi_core", self.sfi_core.bus, SoCRegion(origin=0x08000000, size=0x04000000))

    soc = OSPISoC(platform)
    builder = Builder(soc, output_dir="build", compile_gateware=False)
    builder.build(build_name=core_name)

if __name__ == "__main__":
    main()
