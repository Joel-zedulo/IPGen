import yaml
import subprocess
import sys
import os
import shutil

def main():
    # 1. Get the desired output name from the Makefile environment
    # Default to litespi_core if not set
    core_name = os.environ.get("CORE_NAME", "litespi_core")
    default_gen_name = "litespi_core" # litespi_gen's hardcoded default output name

    # 2. Load config
    try:
        with open("config.yaml") as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        sys.exit("Error: config.yaml not found")

    # 3. Build the CLI command for litespi_gen
    cmd = ["litespi_gen"]

    # Map YAML keys to CLI arguments
    args_map = {
        "clk_freq": "--clk-freq",
        "vendor": "--vendor",
        "module": "--module",
        "mode": "--mode",
        "rate": "--rate",
        "divisor": "--divisor",
        "bus_standard": "--bus-standard",
        "bus_endianness": "--bus-endianness",
    }

    for key, flag in args_map.items():
        if key in cfg:
            # Ensure strings like "1:1" are passed correctly
            cmd.extend([flag, str(cfg[key])])

    if cfg.get("with_master"):
        cmd.append("--with-master")

    if cfg.get("sim"):
        cmd.append("--sim")

    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    # 4. Handle renaming if the Makefile requested a different name
    # litespi_gen always outputs build/gateware/litespi_core.v
    default_path = os.path.join("build", "gateware", f"{default_gen_name}.v")
    target_path = os.path.join("build", "gateware", f"{core_name}.v")

    if core_name != default_gen_name:
        if os.path.exists(default_path):
            shutil.move(default_path, target_path)
            with open(target_path, 'r') as f:
                content = f.read()
            content = content.replace(default_gen_name, core_name)
            with open(target_path, 'w') as f:
                f.write(content)
            print(f"Renamed {default_gen_name} -> {core_name} (module + all references)")
        else:
            print(f"Warning: Could not find {default_path} to rename.")

if __name__ == "__main__":
    main()
