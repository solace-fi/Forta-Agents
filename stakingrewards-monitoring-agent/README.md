# StakingRewards Monitoring Agent

## Description

This agent monitors when `setRewards(uint256 rewardPerSecond_)` or `setTimes(uint256 startTime_, uint256 endTime_)` are
called on StakingRewards contract. Also listen for `RewardsSet(uint256 rewardPerSecond)`
and `FarmTimesSet(uint256 startTime, uint256 endTime)` events.

## Supported Chains

- Ethereum

## Alerts

- STAKINGREWARDS-EVENT
    - Fired when `RewardsSet` or `FarmTimesSet` were emitted.
    - Severity is always set to "info"
    - Type is always set to "info"
    - Metadata contains:
        - `event` - name of the emitted event
        - event inputs: `rewardPerSecond` or (`startTime` and `endTime`)


- STAKINGREWARDS-FUNCTION
    - Fired when `setRewards()` or `setTimes()` are called.
    - Severity is always set to "info"
    - Type is always set to "info"
    - Metadata contains:
        - `function` - name of the function
        - function inputs: `rewardPerSecond_` or (`startTime_` and `endTime_`)

## Tests

There are 6 tests that should pass:

- `test_returns_empty_findings_if_there_is_no_target_event_in_the_logs()`
- `test_returns_empty_findings_if_the_contract_address_is_not_stakingrewards()`
- `test_returns_findings_for_rewardset_event()`
- `test_returns_findings_for_farmtimeset_event()`
- `test_returns_findings_for_setrewards_function()`
- `test_returns_findings_for_settimes_function()`

## Test Data

```bash
❯ npx forta-agent@latest run --tx 0xa117319020d0f7e80e674463725071d5027c23c4a4edb1928ff7d2e1f8912027
(<Function setTimes(uint256,uint256)>,
 {'endTime_': 115792089237316195423570985008687907853269984665640564039457584007913129639935,
  'startTime_': 1642701600})
2 findings for transaction 0xa117319020d0f7e80e674463725071d5027c23c4a4edb1928ff7d2e1f8912027 {
  "name": "StakingRewards Event Alert",
  "description": "Contract event FarmTimesSet was emitted by 0x501ace3d42f9c8723b108d4fbe29989060a91411",
  "alertId": "STAKINGREWARDS-EVENT",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "event": "FarmTimesSet",
    "startTime": 1642701600,
    "endTime": 1.157920892373162e+77
  }
},{
  "name": "StakingRewards Function Alert",
  "description": "Contract function setTimes was called",
  "alertId": "STAKINGREWARDS-FUNCTION",
  "protocol": "ethereum",
  "severity": "Info",
  "type": "Info",
  "metadata": {
    "function": "setTimes",
    "startTime_": 1642701600,
    "endTime_": 1.157920892373162e+77
  }
}
```
