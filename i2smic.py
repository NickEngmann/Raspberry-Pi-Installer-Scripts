try:
    from adafruit_shell import Shell
except ImportError:
    raise RuntimeError("The library 'adafruit_shell' was not found. To install, try typing: sudo pip3 install adafruit-python-shell")

shell = Shell()

def main():
    shell.clear()
    print("""This script downloads and installs
I2S microphone support.
""")
    if not shell.is_raspberry_pi():
        shell.bail("Non-Raspberry Pi board detected.")
    pi_model = shell.get_board_model()
    print("{} detected.\n".format(pi_model))
    if pi_model in ("RASPBERRY_PI_ZERO", "RASPBERRY_PI_ZERO_W"):
        pimodel_select = 0
    elif pi_model in ("RASPBERRY_PI_2B", "RASPBERRY_PI_3B", "RASPBERRY_PI_3B_PLUS", "RASPBERRY_PI_3A_PLUS", "RASPBERRY_PI_ZERO_2_W"):
        pimodel_select = 1
    elif pi_model in ("RASPBERRY_PI_4B", "RASPBERRY_PI_CM4", "RASPBERRY_PI_400"):
        pimodel_select = 2
    else:
        shell.bail("Unsupported Pi board detected.")

    print("""
Installing...""")

    # Build and install the module
    shell.chdir("./i2s_mic_module")
    shell.run_command("make clean")
    shell.run_command("make")
    shell.run_command("make install")

    shell.write_text_file(
        "/etc/modules-load.d/snd-i2smic-rpi.conf",
        "snd-i2smic-rpi"
    )
    shell.write_text_file(
        "/etc/modprobe.d/snd-i2smic-rpi.conf",
        "options snd-i2smic-rpi rpi_platform_generation={}".format(pimodel_select)
    )

    # Enable I2S overlay
    shell.run_command("sed -i -e 's/#dtparam=i2s/dtparam=i2s/g' /boot/config.txt")

    # Done
    print("""DONE.

Settings take effect on next boot.
""")
    #shell.prompt_reboot()

# Main function
if __name__ == "__main__":
    shell.require_root()
    main()
