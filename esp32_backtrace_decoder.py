import subprocess
import sys
import os

# Statikus addr2line elérési út
ADDR2LINE = r"C:\llvm-mingw-20241203-msvcrt-i686\bin\addr2line.exe"

def decode_backtrace(addr2line_path, elf_file, backtrace):
    # Split backtrace into addresses
    addresses = [addr.split(":")[0] for addr in backtrace.split()]
    
    # Decode each address using addr2line
    decoded = []
    for addr in addresses:
        result = subprocess.run(
            [addr2line_path, "-e", elf_file, addr],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            decoded.append(f"{addr} -> {result.stdout.strip()}")
        else:
            decoded.append(f"{addr} -> Error: {result.stderr.strip()}")
    return decoded

def main():
    if len(sys.argv) != 3:
        print("Usage: python esp32_backtrace_decoder.py <path_to_elf> <backtrace>")
        sys.exit(1)
    
    # Parse command-line arguments
    elf_file = sys.argv[1]
    backtrace = sys.argv[2]
    
    # Validate ELF file
    if not os.path.isfile(elf_file):
        print(f"Error: ELF file not found at {elf_file}")
        sys.exit(1)
    
    # Decode the backtrace
    decoded_backtrace = decode_backtrace(ADDR2LINE, elf_file, backtrace)
    
    # Print the results
    print("\nDecoded Backtrace:")
    for line in decoded_backtrace:
        print(line)

if __name__ == "__main__":
    main()