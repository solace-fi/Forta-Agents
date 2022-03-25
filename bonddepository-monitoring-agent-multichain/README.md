# BondDepository Monitoring Agent

## Description

Currently deployed to https://explorer.forta.network/agent/0x4a1cd614f1b4783a3a4d2c8679323cd6e58bc3a080ee22cb23b6074ca40f2cd0

This agent monitors when `TellerAdded(address indexed teller)`
or `TellerRemoved(address indexed teller)` events are emitted by the BondDepository contract.

## Supported Chains

- Ethereum
- Polygon

## Alerts

- BOND-DEPOSITORY-TELLER-ADDED
    - Fired when `TellerAdded` was emitted.
    - Severity is always set to "info"
    - Type is always set to "info"
    - Metadata contains:
        - `teller` - teller's contract address


- BOND-DEPOSITORY-TELLER-REMOVED
    - Fired when `TellerRemoved` was emitted.
    - Severity is always set to "info"
    - Type is always set to "info"
    - Metadata contains:
        - `teller` - teller's contract address

## Tests

There are 4 tests that should pass:

- `test_returns_empty_findings_if_there_is_no_target_event_in_the_logs()`
- `test_returns_empty_findings_if_the_contract_address_is_not_bonddepository()`
- `test_returns_findings_for_telleradded_event()`
- `test_returns_findings_for_tellerremowed_event()`


## Test Data

```bash
❯ npx forta-agent@latest run --tx 0x438464e0017caeabd4f51951969480fbd4b2ab0a707ca4fc070f5fac53dac51c
1 findings for transaction 0x438464e0017caeabd4f51951969480fbd4b2ab0a707ca4fc070f5fac53dac51c {
  "name": "BondDepository TellerAdded Event Alert",
  "description": "Contract event TellerAdded was emitted by 0x501ACe2f00EC599D4FDeA408680e192f88D94D0D",
  "alertId": "BOND-DEPOSITORY-TELLER-ADDED",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "teller": "0x501aCef4F8397413C33B13cB39670aD2f17BfE62"
  }
}
❯ npx forta-agent@latest run --tx 0x849c2b5d4d2cb10775120c3936a385c5ccced6d65bda2dc6f9b74aa25a8ae5dc
1 findings for transaction 0x849c2b5d4d2cb10775120c3936a385c5ccced6d65bda2dc6f9b74aa25a8ae5dc {
  "name": "BondDepository TellerAdded Event Alert",
  "description": "Contract event TellerAdded was emitted by 0x501ACe2f00EC599D4FDeA408680e192f88D94D0D",
  "alertId": "BOND-DEPOSITORY-TELLER-ADDED",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "teller": "0x501ACe00FD8e5dB7C3be5e6D254ba4995e1B45b7"
  }
}
```
