import argparse

import snap7
from snap7.type import Areas
from snap7.util import get_bool, set_bool
from tabulate import tabulate


class PLCController:
    def __init__(self, ip: str, rack: int, slot: int):
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()

    def connect(self):
        """Connects to the PLC."""
        try:
            self.client.connect(self.ip, self.rack, self.slot)
            if not self.client.get_connected():
                raise ConnectionError("Failed to connect to PLC.")
            print("Connected to PLC.")
        except Exception as e:
            raise ConnectionError(f"Error connecting to PLC: {e}")

    def disconnect(self):
        """Disconnects from the PLC."""
        if self.client.get_connected():
            self.client.disconnect()
            print("Disconnected from PLC.")

    def set_output(self, byte_idx: int, bit_idx: int, value: bool):
        """
        Sets a specific output (Qx.x) to a given value (True/False).
        :param byte_idx: Byte address of the output (e.g., Q0 is byte 0)
        :param bit_idx: Bit address within the byte (e.g., Q0.1 is bit 1)
        :param value: True to set the output ON, False to set it OFF
        """
        try:
            outputs = self.client.read_area(Areas.PA, 0, byte_idx, 1)
            updated_outputs = bytearray(outputs)
            set_bool(updated_outputs, 0, bit_idx, value)
            self.client.write_area(Areas.PA, 0, byte_idx, updated_outputs)
            print(f"Output Q{byte_idx}.{bit_idx} set to {value}.")
        except Exception as e:
            raise RuntimeError(f"Error setting output Q{byte_idx}.{bit_idx}: {e}")

    def read_all_outputs(self, num_bytes: int = 1):
        """
        Reads and prints the current state of outputs in a transposed table format.
        :param num_bytes: Number of output bytes to read (default is 1 byte)
        """
        try:
            outputs = self.client.read_area(Areas.PA, 0, 0, num_bytes)
            headers = [f"Q{byte_idx}.x" for byte_idx in range(num_bytes)]
            table_data = [
                [f"Qx.{bit_idx}"]
                + [
                    get_bool(outputs, byte_idx, bit_idx)
                    for byte_idx in range(num_bytes)
                ]
                for bit_idx in range(8)
            ]
            print("\nCurrent Output States:")
            print(tabulate(table_data, headers=[""] + headers, tablefmt="grid"))
        except Exception as e:
            raise RuntimeError(f"Error reading outputs: {e}")


def main(args):
    plc = PLCController(args.ip, args.rack, args.slot)

    try:
        plc.connect()

        if args.value not in [0, 1]:
            raise ValueError("Invalid value. Please set 1 for ON or 0 for OFF.")

        plc.set_output(args.byte, args.bit, bool(args.value))

        plc.read_all_outputs(args.num_bytes)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        plc.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Control a PLC output Qx.x and display the state of outputs."
    )
    parser.add_argument("--ip", type=str, required=True, help="IP address of the PLC")
    parser.add_argument(
        "--rack", type=int, required=True, help="Rack number of the PLC"
    )
    parser.add_argument(
        "--slot", type=int, required=True, help="Slot number of the PLC"
    )
    parser.add_argument("--byte", type=int, required=True, help="Output byte address")
    parser.add_argument(
        "--bit", type=int, required=True, help="Output bit address within the byte"
    )
    parser.add_argument(
        "--num_bytes",
        type=int,
        default=3,
        help="Number of output bytes to read and display",
    )
    parser.add_argument(
        "--value",
        type=int,
        choices=[0, 1],
        required=True,
        help="Value to set (1 for ON, 0 for OFF)",
    )

    args = parser.parse_args()
    main(args)
