import random
import eth_abi
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from eth_utils import encode_hex, event_abi_to_log_topic, function_abi_to_4byte_selector
from src.agent import handle_transaction, PAUSED_ABI, UNPAUSED_ABI, TERMSSET_ABI, FEESSET_ABI, ADDRESSESSET_ABI, \
    UNPAUSE_ABI, PAUSE_ABI, SETTERMS_ABI, SETFEES_ABI, SETADDRESSES_ABI

from src.constants import BONDTELLER_CONTRACTS

PAUSED = "Paused()"
UNPAUSED = "Unpaused()"
TERMSSET = "TermsSet()"
FEESSET = "FeesSet()"
ADDRESSESSET = "AddressesSet()"

all_events = [PAUSED, UNPAUSED, TERMSSET, FEESSET, ADDRESSESSET]
all_events_abi = [PAUSED_ABI, UNPAUSED_ABI, TERMSSET_ABI, FEESSET_ABI, ADDRESSESSET_ABI]
functions_abi = [UNPAUSE_ABI, PAUSE_ABI]

FROM_ADDRESS = "0x1111111111111111111111111111111111111111"
TO_ADDRESS = "0x2222222222222222222222222222222222222222"


def create_event(event, contract_address):
    data = eth_abi.encode_abi([], [])
    data = encode_hex(data)
    topics = [event_abi_to_log_topic(event)]
    return {'topics': topics,
            'data': data,
            'address': contract_address}


class TestSolaceWhalesAgent:
    def test_returns_empty_findings_if_there_is_no_target_event_in_the_logs(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': FROM_ADDRESS,
                'to': TO_ADDRESS,
                'hash': "0"
            }})

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_empty_findings_if_the_contract_address_is_not_bondteller(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': FROM_ADDRESS,
                'to': TO_ADDRESS,
                'hash': "0"
            },
            'receipt': {
                'logs': [create_event(random.choice(all_events_abi), TO_ADDRESS)]}})

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_findings_for_every_bondteller_contract(self):
        for address in list(BONDTELLER_CONTRACTS.values()):
            tx_event = create_transaction_event({
                'transaction': {
                    'from': FROM_ADDRESS,
                    'to': TO_ADDRESS,
                    'hash': "0"
                },
                'receipt': {
                    'logs': [create_event(random.choice(all_events_abi), address)]}})

            findings = handle_transaction(tx_event)
            assert len(findings) != 0

    def test_returns_findings_for_every_target_event(self):
        for event in all_events_abi:
            contract_address = random.choice(list(BONDTELLER_CONTRACTS.values()))
            tx_event = create_transaction_event({
                'transaction': {
                    'from': FROM_ADDRESS,
                    'to': TO_ADDRESS,
                    'hash': "0"
                },
                'receipt': {
                    'logs': [create_event(event, contract_address)]}})

            findings = handle_transaction(tx_event)
            assert len(findings) != 0
            for finding in findings:
                assert finding.alert_id == 'BONDTELLER-EVENT'
                assert finding.description == f'Contract event {event.get("name")} was emitted by {contract_address}'
                assert finding.metadata == {'event': event.get("name"), 'contract_address': contract_address,
                                            'contract': list(BONDTELLER_CONTRACTS.keys())[
                                                list(BONDTELLER_CONTRACTS.values()).index(contract_address)]}
                assert finding.name == 'BondTeller Basic Event Alert'
                assert finding.severity == FindingSeverity.Info
                assert finding.type == FindingType.Info

    def test_returns_findings_for_target_functions(self):
        for function in functions_abi:
            print(function)
            tx_event = create_transaction_event({
                'transaction': {
                    'from': FROM_ADDRESS,
                    'to': random.choice(list(BONDTELLER_CONTRACTS.values())),
                    'data': encode_hex(function_abi_to_4byte_selector(function))
                }})

            findings = handle_transaction(tx_event)
            assert len(findings) != 0
            for finding in findings:
                assert finding.alert_id == 'BONDTELLER-FUNCTION'
                assert finding.description == f'Contract function {function.get("name")} was called'
                assert finding.metadata == {'function': function.get("name")}
                assert finding.name == 'BondTeller Basic Function Alert'
                assert finding.severity == FindingSeverity.Info
                assert finding.type == FindingType.Info
