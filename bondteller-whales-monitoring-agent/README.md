# BondTeller Whales Monitoring Agent

## Description

This agent emits an alert when there is a large deposit in one of the BondTeller contracts.

## Supported Chains

- Ethereum

## Alerts

- SOLACE-BONDTELLER-WHALE
    - Fired when a transaction contains Transfer event with the value greater than the threshold, emitted by the SOLACE token contract and where the transfer receiver is BondTeller contract
    - Severity depends on the value:
        - `Info` when the value is greater than 1kk but smaller than 10kk
        - `Medium` when the value is greater than 10kk but smaller than 100kk
        - `High` when the value is greater than 100kk but smaller than 1kkk
        - `Critical` when the value is greater than 1kkk
    - Type is always set to "info"
    - Metadata contains:
        - `whale` - transaction initiator
        - `value` - amount of SOLACE tokens
        - `contract_address` - address of the BondTeller contract
        - `contract` - name of the BondTeller contract (DAI, ETH, USDC etc.)

## Tests

There are 7 tests that should pass:

- `test_returns_empty_findings_if_transfer_was_emitted_not_by_the_solace()`
- `test_returns_empty_findings_if_value_below_threshold()`
- `test_returns_empty_findings_if_the_transaction_is_not_related_to_the_bondteller()`
- `test_returns_info_finding_if_value_above_threshold()`
- `test_returns_medium_finding_if_value_above_threshold()`
- `test_returns_high_finding_if_value_above_threshold()`
- `test_returns_critical_finding_if_value_above_threshold()`

## Test Data

The agent can be verified on the next transaction if the threshold is lowered to 3000 SOLACE tokens:

```bash
❯ npx forta-agent@latest run --tx 0x2d0d95a52813d527a8d793b594ea2040c0e9d48131fd43ff11885d1c98953603
1 findings for transaction 0x2d0d95a52813d527a8d793b594ea2040c0e9d48131fd43ff11885d1c98953603 {
  "name": "BondTeller Whale Deposit Alert",
  "description": "Address 0xca1d1a11074b1d86ac3fbd44771c7043126839c9 created a large deposit that provoked the minting of SOLACE tokens in the amount of 3000",
  "alertId": "SOLACE-BONDTELLER-WHALE",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "whale": "0xca1d1a11074b1d86ac3fbd44771c7043126839c9",
    "value": "3000000000000000000000",
    "contract_address": "0x501ACe5CeEc693Df03198755ee80d4CE0b5c55fE",
    "contract": "USDT"
  }
}
```
