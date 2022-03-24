import json
import forta_agent
from forta_agent import Finding, FindingType
from src.constants import SOLACE_CONTRACT, TRANSFER_AMOUNT_TH_INFO, DECIMALS
from src.utils import extract_argument, get_severity

with open("./src/ABI/abi.json", 'r') as abi_file:  # get abi from the file
    solace_abi = json.load(abi_file)

# get the event Transfer(address indexed from, address indexed to, uint value)
TRANSFER_ABI = next((x for x in solace_abi if x.get('name', "") == "Transfer"), None)


def handle_transaction(transaction_event: forta_agent.transaction_event.TransactionEvent):
    findings = []

    # filter transaction events where Transfer event is in the log with SOLACE_CONTRACT address
    for event in transaction_event.filter_log(json.dumps(TRANSFER_ABI), SOLACE_CONTRACT):

        # extract the value of the transfer
        value = extract_argument(event, 'value')

        # emit the alert if the value is bigger than the threshold
        if value > TRANSFER_AMOUNT_TH_INFO:
            from_ = extract_argument(event, 'from')
            to = extract_argument(event, 'to')
            findings.append(Finding({
                'name': 'Solace Large Transfer Alert',
                'description': f'Address {from_} transferred to address {to} SOLACE in the '
                               f'amount of {str(value)[:-DECIMALS]}',
                'alert_id': 'SOLACE-WHALE',
                'type': FindingType.Info,
                'severity': get_severity(value),  # determine the severity level of the finding
                'metadata': {
                    'from': from_,
                    'to': to,
                    'value': str(value),
                }
            }))

    return findings
