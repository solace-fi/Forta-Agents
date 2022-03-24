import json
import forta_agent
from forta_agent import Finding, FindingType, FindingSeverity
from src.constants import STAKINGREWARDS_CONTRACT

with open("./src/ABI/abi.json", 'r') as abi_file:  # get abi from the file
    solace_abi = json.load(abi_file)

# event RewardsSet(uint256 rewardPerSecond)
REWARDSSET_ABI = next((x for x in solace_abi if x.get('name', "") == "RewardsSet"), None)
# event FarmTimesSet(uint256 startTime, uint256 endTime)
FARMTIMESET_ABI = next((x for x in solace_abi if x.get('name', "") == "FarmTimesSet"), None)

# function setRewards(uint256 rewardPerSecond_)
SETREWARD_ABI = next((x for x in solace_abi if x.get('name', "") == "setRewards"), None)
# function setTimes(uint256 startTime_, uint256 endTime_)
SETTIMES_ABI = next((x for x in solace_abi if x.get('name', "") == "setTimes"), None)

target_events = {
    'RewardsSet': REWARDSSET_ABI,
    'FarmTimesSet': FARMTIMESET_ABI
}

target_functions = {
    'setRewards': SETREWARD_ABI,
    'setTimes': SETTIMES_ABI,
}


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    findings = []

    # filter transaction events where the target event is in the StakingRewards contract address
    events = transaction_event.filter_log([json.dumps(x) for x in list(target_events.values())],
                                          STAKINGREWARDS_CONTRACT)
    # filter transaction functions where the target function is in the StakingRewards contract address
    functions = transaction_event.filter_function([json.dumps(x) for x in list(target_functions.values())],
                                                  STAKINGREWARDS_CONTRACT)

    # emit the alerts for the events
    for event in events:
        contract_address = event.get("address")
        findings.append(Finding({
            'name': 'StakingRewards Event Alert',
            'description': f'Contract event {event.get("event")} was emitted by {contract_address}',
            'alert_id': 'STAKINGREWARDS-EVENT',
            'type': FindingType.Info,
            'severity': FindingSeverity.Info,
            'metadata': {
                'event': event.get("event"),
                **event.get('args', {})
            }
        }))

    # emit the alerts for the functions
    for function in functions:
        findings.append(Finding({
            'name': 'StakingRewards Function Alert',
            'description': f'Contract function {function[0].fn_name} was called',
            'alert_id': 'STAKINGREWARDS-FUNCTION',
            'type': FindingType.Info,
            'severity': FindingSeverity.Info,
            'metadata': {
                'function': function[0].fn_name,
                **function[1]
            }
        }))

    return findings
