- # ecat_grpc_client

`ecat_grpc_client` is a Python package that provides a gRPC client for EtherCAT communication tasks. This package simplifies the interaction with EtherCAT devices by providing an easy-to-use API for various EtherCAT-related operations.
## Installation

To install `ecat_grpc_client`, simply run:

```bash
pip install ecat_grpc_client
```


## Dependencies

The `ecat_grpc_client` package depends on the following libraries:
- grpcio

Make sure you have them installed in your Python environment.
## Usage

Here's a quick example to get you started:

```python
import sys
from ecat_grpc_client import GRPCECatTask as ecat_client
import sys, json, grpc, time
from motordriver_utils import *

ecat = ecat_client('192.168.214.20') # ecat
```



For more detailed usage instructions, refer to the [API documentation](https://chat.openai.com/chat/link-to-api-docs) .
## API Overview

The `ecat_grpc_client` package provides a `GRPCECatTask` class with the following methods:
- `get_master_status()`
- `get_slave_status()`
- `get_rxdomain_status()`
- `get_txdomain_status()`
- `is_system_ready()`
- `set_servo(slave_idx, state)`
- `set_md_rx_pdo(slave_idx, controlWord, modeOp, targetPos, targetVel, targetTor)`
- `get_md_rx_pdo(slave_idx)`
- `get_md_tx_pdo(slave_idx)`
- `get_md_di(slave_idx)`
- `get_error_code(slave_idx)`
- `get_max_torque(slave_idx)`
- `get_max_motor_speed(slave_idx)`
- `set_max_torque(slave_idx, value)`
- `set_max_motor_speed(slave_idx, value)`
- `get_ioboard_do()`
- `get_ioboard_di()`
- `set_ioboard_do(do_idx, do_val)`
- `set_ioboard_dos(do_vals)`
- `reset_welcon(slave_idx)`
- `get_error_code(slave_idx)`
- `get_core_temp1(slave_idx)`
- `get_core_temp2(slave_idx)`
- `get_core_temp3(slave_idx)`
- `get_maxTorque(slave_idx)`
- `get_profileVel(slave_idx)`
- `get_profileAcc(slave_idx)`
- `get_profileDec(slave_idx)`
- `set_maxTorque(slave_idx, value)`
- `set_profileVel(slave_idx, value)`
- `set_profileAcc(slave_idx, value)`
- `set_profileDec(slave_idx, value)`
## License

This project is licensed under the MIT License. See the [LICENSE](https://chat.openai.com/chat/LICENSE)  file for details.
## Contributing

We welcome contributions! If you would like to improve this package or report any issues, please open a pull request or create an issue on the GitHub repository.
## Contact

For questions or suggestions, please contact the package author at `youngjin.heo@neuromeka.com`.
