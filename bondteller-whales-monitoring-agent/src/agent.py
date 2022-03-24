import json
import forta_agent
from forta_agent import Finding, FindingType
from src.constants import BONDTELLER_CONTRACTS, TRANSFER_AMOUNT_TH_INFO, DECIMALS, NULL_ADDRESS, SOLACE_CONTRACT
from src.utils import extract_argument, get_severity

with open("./src/ABI/abi.json", 'r') as abi_file:  # get abi from the file
    bondteller_abi = json.load(abi_file)

# get the event Transfer(address indexed from, address indexed to, uint value)
TRANSFER_ABI = next((x for x in bondteller_abi if x.get('name', "") == "Transfer"), None)


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    findings = []

    # filter transaction events where Transfer event is in the log with SOLACE_CONTRACT address
    for event in transaction_event.filter_log(json.dumps(TRANSFER_ABI), SOLACE_CONTRACT):

        # extract the sender of the transfer
        from_ = extract_argument(event, 'from')
        if from_ != NULL_ADDRESS:  # should be 0x0 and then it means mint
            continue

        # extract the receiver of the transfer
        to = extract_argument(event, 'to')
        if to not in list(BONDTELLER_CONTRACTS.values()):  # the receiver should be one of the BondTeller contracts
            continue

        value = extract_argument(event, 'value')

        # emit the alert if the value is bigger than the threshold
        if value > TRANSFER_AMOUNT_TH_INFO:
            findings.append(Finding({
                'name': 'BondTeller Whale Deposit Alert',
                'description': f'Address {transaction_event.from_} created a large deposit that provoked the minting '
                               f'of SOLACE tokens in the '
                               f'amount of {str(value)[:-DECIMALS]}',
                'alert_id': 'SOLACE-BONDTELLER-WHALE',
                'type': FindingType.Info,
                'severity': get_severity(value),  # determine the severity level of the finding
                'metadata': {
                    'whale': transaction_event.from_,
                    'value': str(value),
                    'contract_address': to,
                    'contract': list(BONDTELLER_CONTRACTS.keys())[
                        [x.lower() for x in BONDTELLER_CONTRACTS.values()].index(to.lower())]
                }
            }))

    return findings
