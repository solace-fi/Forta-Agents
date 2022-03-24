import json
import forta_agent
from forta_agent import Finding, FindingType, FindingSeverity
from src.constants import BONDTELLER_CONTRACTS

with open("./src/ABI/abi.json", 'r') as abi_file:  # get abi from the file
    solace_abi = json.load(abi_file)

# event Paused()
UNPAUSED_ABI = next((x for x in solace_abi if x.get('name', "") == "Unpaused"), None)
# event Unpaused()
PAUSED_ABI = next((x for x in solace_abi if x.get('name', "") == "Paused"), None)
# event TermsSet()
TERMSSET_ABI = next((x for x in solace_abi if x.get('name', "") == "TermsSet"), None)
# event FeesSet()
FEESSET_ABI = next((x for x in solace_abi if x.get('name', "") == "FeesSet"), None)
# event AddressesSet()
ADDRESSESSET_ABI = next((x for x in solace_abi if x.get('name', "") == "AddressesSet"), None)

# function unpause()
UNPAUSE_ABI = next((x for x in solace_abi if x.get('name', "") == "unpause"), None)
# function pause()
PAUSE_ABI = next((x for x in solace_abi if x.get('name', "") == "pause"), None)
# function setTerms(tuple(uint256 startPrice, uint256 minimumPrice, uint256 maxPayout, uint128 priceAdjNum,
# uint128 priceAdjDenom, uint256 capacity, bool capacityIsPayout, uint40 startTime, uint40 endTime,
# uint40 globalVestingTerm, uint40 halfLife))
SETTERMS_ABI = next((x for x in solace_abi if x.get('name', "") == "setTerms"), None)
# function setFees(uint256 protocolFee)
SETFEES_ABI = next((x for x in solace_abi if x.get('name', "") == "setFees"), None)
# function setAddresses(address solace_, address xsLocker_, address pool_, address dao_, address principal_,
# bool isPermittable_, address bondDepo_)
SETADDRESSES_ABI = next((x for x in solace_abi if x.get('name', "") == "setAddresses"), None)

target_events = {
    'Unpaused': UNPAUSED_ABI,
    'Paused': PAUSED_ABI,
    'TermsSet': TERMSSET_ABI,
    'FeesSet': FEESSET_ABI,
    'AddressesSet': ADDRESSESSET_ABI
}

target_functions = {
    'unpause': UNPAUSE_ABI,
    'pause': PAUSE_ABI,
    'setTerms': SETTERMS_ABI,
    'setFees': SETFEES_ABI,
    'setAddresses': SETADDRESSES_ABI
}


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    findings = []

    # filter transaction events where the target event is in the BondTeller contract address
    events = transaction_event.filter_log([json.dumps(x) for x in list(target_events.values())],
                                          list(BONDTELLER_CONTRACTS.values()))
    # filter transaction functions where the target function is in the BondTeller contract address
    functions = transaction_event.filter_function([json.dumps(x) for x in list(target_functions.values())],
                                                  list(BONDTELLER_CONTRACTS.values()))

    # emit the alerts for the events
    for event in events:
        contract_address = event.get("address")
        findings.append(Finding({
            'name': 'BondTeller Basic Event Alert',
            'description': f'Contract event {event.get("event")} was emitted by {contract_address}',
            'alert_id': 'BONDTELLER-EVENT',
            'type': FindingType.Info,
            'severity': FindingSeverity.Info,
            'metadata': {
                'event': event.get("event"),
                'contract_address': event.get("address"),
                'contract': list(BONDTELLER_CONTRACTS.keys())[
                    [x.lower() for x in BONDTELLER_CONTRACTS.values()].index(contract_address)]
            }
        }))

    # emit the alerts for the functions
    for function in functions:
        findings.append(Finding({
            'name': 'BondTeller Basic Function Alert',
            'description': f'Contract function {function[0].fn_name} was called',
            'alert_id': 'BONDTELLER-FUNCTION',
            'type': FindingType.Info,
            'severity': FindingSeverity.Info,
            'metadata': {
                'function': function[0].fn_name,
            }
        }))

    return findings
