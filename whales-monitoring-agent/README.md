# Solace Whale Monitoring Agent

## Description

This agent emits an alert when there is a large transfer of SOLACE in the logs.

## Supported Chains

- Ethereum

## Alerts

- SOLACE-WHALE
    - Fired when a transaction contains Transfer event with the value greater than threshold.
    - Severity depends on the value:
        - `Info` when the value is greater than 1kk but smaller than 10kk
        - `Medium` when the value is greater than 10kk but smaller than 100kk
        - `High` when the value is greater than 100kk but smaller than 1kkk
        - `Critical` when the value is greater than 1kkk
    - Type is always set to "info"
    - Metadata contains:
        - `from` - transfer sender
        - `to` - transfer target
        - `value` - amount of SOLACE tokens

## Tests

There are 6 tests that should pass:

- `test_returns_empty_findings_if_value_below_threshold()`
- `test_returns_empty_findings_if_the_contract_is_not_solace()`
- `test_returns_info_finding_if_value_above_threshold()`
- `test_returns_medium_finding_if_value_above_threshold()`
- `test_returns_high_finding_if_value_above_threshold()`
- `test_returns_critical_finding_if_value_above_threshold()`

## Test Data

The last 25 event from the SOLACE contract were checked:

```bash
❯ npx forta-agent@latest run --tx 0xee3c8ffdd4694bf446ea882fb787ac5cfc4ab7a6b2590fa0307e106e7c750c39
1 findings for transaction 0xee3c8ffdd4694bf446ea882fb787ac5cfc4ab7a6b2590fa0307e106e7c750c39 {
  "name": "Solace Large Transfer Alert",
  "description": "Address 0x501AcE0e8D16B92236763E2dEd7aE3bc2DFfA276 transferred to address 0x40ec5B33f54e0E8A33A975908C5BA1c14e5BbbDf SOLACE in the amount of 7000000",
  "alertId": "SOLACE-WHALE",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "from": "0x501AcE0e8D16B92236763E2dEd7aE3bc2DFfA276",
    "to": "0x40ec5B33f54e0E8A33A975908C5BA1c14e5BbbDf",
    "value": "7000000000000000000000000"
  }
}
❯ npx forta-agent@latest run --tx 0xce7e427cb3ef7a0447e15377aea069cc33bad5bf395e91a0493889a0e89824e2
1 findings for transaction 0xce7e427cb3ef7a0447e15377aea069cc33bad5bf395e91a0493889a0e89824e2 {
  "name": "Solace Large Transfer Alert",
  "description": "Address 0x5efC0d9ee3223229Ce3b53e441016efC5BA83435 transferred to address 0x501AcE0e8D16B92236763E2dEd7aE3bc2DFfA276 SOLACE in the amount of 7000000",
  "alertId": "SOLACE-WHALE",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "from": "0x5efC0d9ee3223229Ce3b53e441016efC5BA83435",
    "to": "0x501AcE0e8D16B92236763E2dEd7aE3bc2DFfA276",
    "value": "7000000000000000000000000"
  }
}

```
