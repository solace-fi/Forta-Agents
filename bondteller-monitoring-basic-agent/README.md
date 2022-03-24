# Solace BondTeller Basic Agent

## Description

This agent monitors when `pause()`, `unpause()`, `setTerms()`, `setFees()`, or `setAddresses()` are called on 
BondTeller contracts (important governance functions). Also listen for `Paused`, `Unpaused`, `TermsSet`, `FeesSet`, 
`AddressesSet` events.

## Supported Chains

- Ethereum

## Alerts

- BONDTELLER-EVENT
    - Fired when `Paused`, `Unpaused`, `TermsSet`, `FeesSet` or `AddressesSet` were emitted.
    - Severity is always set to "info"
    - Type is always set to "info"
    - Metadata contains:
        - `event` - name of the emitted event
        - `contract_address` - address of the contract
        - `contract` - name of the contract (DAI, ETH, USDC etc.)
      

- BONDTELLER-FUNCTION
    - Fired when `pause()`, `unpause()`, `setTerms()`, `setFees()`, or `setAddresses()` are called.
    - Severity is always set to "info"
    - Type is always set to "info"
    - Metadata contains:
        - `function` - name of the function

## Tests

There are 5 tests that should pass:

- `test_returns_empty_findings_if_there_is_no_target_event_in_the_logs()`
- `test_returns_empty_findings_if_the_contract_address_is_not_bondteller()`
- `test_returns_findings_for_every_bondteller_contract()`
- `test_returns_findings_for_every_target_event()`
- `test_returns_findings_for_target_functions()`

## Test Data

The last 2 event from the BondTellerEth contract were checked:

```bash
❯ npx forta-agent@latest run --tx 0x16e18195dd3173fb31062f0bcfa0d5fae88f57cf41450efbcdfb7c076f19ab99
2 findings for transaction 0x16e18195dd3173fb31062f0bcfa0d5fae88f57cf41450efbcdfb7c076f19ab99 {
  "name": "BondTeller Basic Event Alert",
  "description": "Contract event TermsSet was emitted by 0x501ace95141f3eb59970dd64af0405f6056fb5d8",
  "alertId": "BONDTELLER-EVENT",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "event": "TermsSet",
    "contract_address": "0x501ace95141f3eb59970dd64af0405f6056fb5d8",
    "contract": "ETH"
  }
},{
  "name": "BondTeller Basic Function Alert",
  "description": "Contract function setTerms was called",
  "alertId": "BONDTELLER-FUNCTION",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "function": "setTerms"
  }
}
❯ npx forta-agent@latest run --tx 0xedb50068241e625c7610978a27c8b3cf5ad1b6c5538bd071f6827881b1e2fb3e
2 findings for transaction 0xedb50068241e625c7610978a27c8b3cf5ad1b6c5538bd071f6827881b1e2fb3e {
  "name": "BondTeller Basic Event Alert",
  "description": "Contract event FeesSet was emitted by 0x501ace95141f3eb59970dd64af0405f6056fb5d8",
  "alertId": "BONDTELLER-EVENT",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "event": "FeesSet",
    "contract_address": "0x501ace95141f3eb59970dd64af0405f6056fb5d8",
    "contract": "ETH"
  }
},{
  "name": "BondTeller Basic Function Alert",
  "description": "Contract function setFees was called",
  "alertId": "BONDTELLER-FUNCTION",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "function": "setFees"
  }
}
```
