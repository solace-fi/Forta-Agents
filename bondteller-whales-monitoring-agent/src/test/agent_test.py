import random
import eth_abi
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from src.constants import BONDTELLER_CONTRACTS, NULL_ADDRESS, SOLACE_CONTRACT
from eth_utils import keccak, encode_hex
from src.agent import handle_transaction

TRANSFER = "Transfer(address,address,uint256)"
ONE_ADDRESS = "0x1111111111111111111111111111111111111111"
TWO_ADDRESS = "0x2222222222222222222222222222222222222222"


def transfer_event(from_, to, value: int, contract_address: str):
    hash = keccak(text=TRANSFER)
    data = eth_abi.encode_abi(["uint256"], [value])
    data = encode_hex(data)
    from_ = eth_abi.encode_abi(["address"], [from_])
    from_ = encode_hex(from_)
    to = eth_abi.encode_abi(["address"], [to])
    to = encode_hex(to)
    topics = [hash, from_, to]
    return {'topics': topics,
            'data': data,
            'address': contract_address}


class TestSolaceWhalesAgent:
    def test_returns_empty_findings_if_transfer_was_emitted_not_by_the_solace(self):
        bondteller = random.choice(list(BONDTELLER_CONTRACTS.values()))
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': bondteller,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(NULL_ADDRESS, bondteller, 9999999999 * 10 ** 18, ONE_ADDRESS)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_empty_findings_if_value_below_threshold(self):
        bondteller = random.choice(list(BONDTELLER_CONTRACTS.values()))
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': bondteller,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(NULL_ADDRESS, bondteller, 1, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_empty_findings_if_the_transaction_is_not_related_to_the_bondteller(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(NULL_ADDRESS, TWO_ADDRESS, 9999999999 * 10 ** 18, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_info_finding_if_value_above_threshold(self):
        bondteller = random.choice(list(BONDTELLER_CONTRACTS.values()))
        value = 1000001 * 10 ** 18
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': bondteller,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(NULL_ADDRESS, bondteller, value, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 1
        for finding in findings:
            assert finding.alert_id == 'SOLACE-BONDTELLER-WHALE'
            assert finding.description == f'Address {ONE_ADDRESS} created a ' \
                                          'large deposit that provoked the minting of SOLACE tokens in ' \
                                          'the amount of 1000001'
            assert finding.metadata == {'whale': ONE_ADDRESS, 'value': str(value), 'contract_address': bondteller,
                                        'contract': list(BONDTELLER_CONTRACTS.keys())[
                                            [x.lower() for x in BONDTELLER_CONTRACTS.values()].index(
                                                bondteller.lower())]}
            assert finding.name == 'BondTeller Whale Deposit Alert'
            assert finding.protocol == 'ethereum'
            assert finding.severity == FindingSeverity.Info
            assert finding.type == FindingType.Info

    def test_returns_medium_finding_if_value_above_threshold(self):
        bondteller = random.choice(list(BONDTELLER_CONTRACTS.values()))
        value = 10000001 * 10 ** 18
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': bondteller,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(NULL_ADDRESS, bondteller, value, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        pprint(vars(findings[0]))
        assert len(findings) == 1
        for finding in findings:
            assert finding.alert_id == 'SOLACE-BONDTELLER-WHALE'
            assert finding.description == f'Address {ONE_ADDRESS} created a ' \
                                          'large deposit that provoked the minting of SOLACE tokens in ' \
                                          'the amount of 10000001'
            assert finding.metadata == {'whale': ONE_ADDRESS, 'value': str(value), 'contract_address': bondteller,
                                        'contract': list(BONDTELLER_CONTRACTS.keys())[
                                            [x.lower() for x in BONDTELLER_CONTRACTS.values()].index(
                                                bondteller.lower())]}
            assert finding.name == 'BondTeller Whale Deposit Alert'
            assert finding.protocol == 'ethereum'
            assert finding.severity == FindingSeverity.Medium
            assert finding.type == FindingType.Info

    def test_returns_high_finding_if_value_above_threshold(self):
        bondteller = random.choice(list(BONDTELLER_CONTRACTS.values()))
        value = 100000001 * 10 ** 18
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': bondteller,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(NULL_ADDRESS, bondteller, value, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        pprint(vars(findings[0]))
        assert len(findings) == 1
        for finding in findings:
            assert finding.alert_id == 'SOLACE-BONDTELLER-WHALE'
            assert finding.description == f'Address {ONE_ADDRESS} created a ' \
                                          'large deposit that provoked the minting of SOLACE tokens in ' \
                                          'the amount of 100000001'
            assert finding.metadata == {'whale': ONE_ADDRESS, 'value': str(value), 'contract_address': bondteller,
                                        'contract': list(BONDTELLER_CONTRACTS.keys())[
                                            [x.lower() for x in BONDTELLER_CONTRACTS.values()].index(
                                                bondteller.lower())]}
            assert finding.name == 'BondTeller Whale Deposit Alert'
            assert finding.protocol == 'ethereum'
            assert finding.severity == FindingSeverity.High
            assert finding.type == FindingType.Info

    def test_returns_critical_finding_if_value_above_threshold(self):
        bondteller = random.choice(list(BONDTELLER_CONTRACTS.values()))
        value = 1000000001 * 10 ** 18
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': bondteller,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(NULL_ADDRESS, bondteller, value, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 1
        for finding in findings:
            assert finding.alert_id == 'SOLACE-BONDTELLER-WHALE'
            assert finding.description == f'Address {ONE_ADDRESS} created a ' \
                                          'large deposit that provoked the minting of SOLACE tokens in ' \
                                          'the amount of 1000000001'
            assert finding.metadata == {'whale': ONE_ADDRESS, 'value': str(value), 'contract_address': bondteller,
                                        'contract': list(BONDTELLER_CONTRACTS.keys())[
                                            [x.lower() for x in BONDTELLER_CONTRACTS.values()].index(
                                                bondteller.lower())]}
            assert finding.name == 'BondTeller Whale Deposit Alert'
            assert finding.protocol == 'ethereum'
            assert finding.severity == FindingSeverity.Critical
            assert finding.type == FindingType.Info
