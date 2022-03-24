import json
import forta_agent
from forta_agent import Finding, FindingType, FindingSeverity
from src.constants import BONDDEPOSITORY_CONTRACT

with open("./src/ABI/abi.json", 'r') as abi_file:  # get abi from the file
    solace_abi = json.load(abi_file)

# event TellerAdded(address indexed teller)
TELLERADDED_ABI = next((x for x in solace_abi if x.get('name', "") == "TellerAdded"), None)
# event TellerRemoved(address indexed teller)
TELLERREMOWED_ABI = next((x for x in solace_abi if x.get('name', "") == "TellerRemoved"), None)

target_events = {
    'TellerAdded': TELLERADDED_ABI,
    'TellerRemoved': TELLERREMOWED_ABI
}


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    findings = []

    # filter transaction events where the target event is in the StakingRewards contract address
    events = transaction_event.filter_log([json.dumps(x) for x in list(target_events.values())],
                                          BONDDEPOSITORY_CONTRACT)

    # emit the alerts for the events
    for event in events:

        # get the name from the event
        event_name = event.get("event")

        if event_name == 'TellerAdded':
            findings.append(Finding({
                'name': 'BondDepository TellerAdded Event Alert',
                'description': f'Contract event {event_name} was emitted by {BONDDEPOSITORY_CONTRACT}',
                'alert_id': 'BOND-DEPOSITORY-TELLER-ADDED',
                'type': FindingType.Info,
                'severity': FindingSeverity.Info,
                'metadata': {
                    **event.get('args', {})
                }
            }))
        else:
            findings.append(Finding({
                'name': 'BondDepository TellerRemoved Event Alert',
                'description': f'Contract event {event_name} was emitted by {BONDDEPOSITORY_CONTRACT}',
                'alert_id': 'BOND-DEPOSITORY-TELLER-REMOVED',
                'type': FindingType.Info,
                'severity': FindingSeverity.Info,
                'metadata': {
                    **event.get('args', {})
                }
            }))

    return findings
