# s7-output-control

s7-output-control is a Python tool designed for interacting with Siemens PLCs using the Snap7 library.
It allows users to set specific outputs (Qx.x) and read the status of all outputs in a table format.
Ideal for testing, monitoring, and simple automation tasks with Siemens PLCs.

## Compatibility

This tool is only compatible with Siemens PLCs that allow S7Comm protocol.
It is the case for older PLC models like S7-300, S7-400 and by activating mixed commnunication mode on S7-1200 and S7-1500.
S7CommPlus is currently not supported.

## Features

- **Set Output State**: Toggle individual outputs on or off.
- **Monitor Output States**: Display current output states in an intuitive table view.
- **Customizable Control**: Specify PLC connection parameters, output byte and bit, toggle duration, and read range.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/PluggeRo/s7-ouput-control.git
cd s7-output-control
```

2. Activate virtual env:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python s7-output-control.py --ip <PLC_IP> --rack <RACK> --slot <SLOT> --byte <BYTE> --bit <BIT> --num_bytes <NUM_OUTPUT_BYTES> --value <0|1>
```

**Example**: To trigger output `Q0.1`, set `--byte 0` and `--bit 1`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please fork the repository, create a branch, and submit a pull request.
