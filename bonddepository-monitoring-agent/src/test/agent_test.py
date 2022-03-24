import eth_abi
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from eth_utils import encode_hex, keccak
from src.agent import handle_transaction

from src.constants import BONDDEPOSITORY_CONTRACT

TELLERADDED = "TellerAdded(address)"
TELLERREMOWED = "TellerRemoved(address)"

all_events = [TELLERADDED, TELLERREMOWED]

ONE_ADDRESS = "0x1111111111111111111111111111111111111111"
TWO_ADDRESS = "0x2222222222222222222222222222222222222222"


def generate_event(event: str, contract_address: str):
    hash = keccak(text=event)
    data = eth_abi.encode_abi([], [])
    data = encode_hex(data)
    teller = eth_abi.encode_abi(["address"], [ONE_ADDRESS])
    teller = encode_hex(teller)
    topics = [hash, teller]
    return {'topics': topics,
            'data': data,
            'address': contract_address}


class TestBondDepositoryAgent:
    def test_returns_empty_findings_if_there_is_no_target_event_in_the_logs(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            }})

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_empty_findings_if_the_contract_address_is_not_bonddepository(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            },
            'receipt': {
                'logs': [generate_event(TELLERADDED, TWO_ADDRESS)]}})

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_findings_for_telleradded_event(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            },
            'receipt': {
                'logs': [generate_event(TELLERADDED, BONDDEPOSITORY_CONTRACT)]}})

        findings = handle_transaction(tx_event)
        assert len(findings) != 0
        for finding in findings:
            assert finding.alert_id == 'BOND-DEPOSITORY-TELLER-ADDED'
            assert finding.description == f'Contract event TellerAdded was emitted by {BONDDEPOSITORY_CONTRACT}'
            assert finding.metadata == {'teller': ONE_ADDRESS}
            assert finding.name == 'BondDepository TellerAdded Event Alert'
            assert finding.severity == FindingSeverity.Info
            assert finding.type == FindingType.Info

    def test_returns_findings_for_tellerremowed_event(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            },
            'receipt': {
                'logs': [generate_event(TELLERREMOWED, BONDDEPOSITORY_CONTRACT)]}})

        findings = handle_transaction(tx_event)
        assert len(findings) != 0
        for finding in findings:
            assert finding.alert_id == 'BOND-DEPOSITORY-TELLER-REMOVED'
            assert finding.description == f'Contract event TellerRemoved was emitted by {BONDDEPOSITORY_CONTRACT}'
            assert finding.metadata == {'teller': ONE_ADDRESS}
            assert finding.name == 'BondDepository TellerRemoved Event Alert'
            assert finding.severity == FindingSeverity.Info
            assert finding.type == FindingType.Info
