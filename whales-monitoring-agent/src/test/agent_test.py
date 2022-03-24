import eth_abi
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from src.constants import SOLACE_CONTRACT, DECIMALS
from eth_utils import keccak, encode_hex
from src.agent import handle_transaction

TRANSFER = "Transfer(address,address,uint256)"
FROM_ADDRESS = "0x1111111111111111111111111111111111111111"
TO_ADDRESS = "0x2222222222222222222222222222222222222222"


def transfer_event(value: int, contract_address: str):
    hash = keccak(text=TRANSFER)
    data = eth_abi.encode_abi(["uint256"], [value])
    data = encode_hex(data)
    from_ = eth_abi.encode_abi(["address"], [FROM_ADDRESS])
    from_ = encode_hex(from_)
    to = eth_abi.encode_abi(["address"], [TO_ADDRESS])
    to = encode_hex(to)
    topics = [hash, from_, to]
    return {'topics': topics,
            'data': data,
            'address': contract_address}


class TestSolaceWhalesAgent:
    def test_returns_empty_findings_if_value_below_threshold(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': FROM_ADDRESS,
                'to': SOLACE_CONTRACT,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(999999, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_empty_findings_if_the_contract_is_not_solace(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': FROM_ADDRESS,
                'to': SOLACE_CONTRACT,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(999999000000000000000000, TO_ADDRESS)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_info_finding_if_value_above_threshold(self):
        value = 1000001000000000000000000
        tx_event = create_transaction_event({
            'transaction': {
                'from': FROM_ADDRESS,
                'to': SOLACE_CONTRACT,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(value, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 1
        for finding in findings:
            assert finding.alert_id == 'SOLACE-WHALE'
            assert finding.description == f'Address {FROM_ADDRESS} transferred to address {TO_ADDRESS} ' \
                                          f'SOLACE in the amount of {str(value)[:-DECIMALS]}'
            assert finding.metadata == {'from': FROM_ADDRESS, 'to': TO_ADDRESS, 'value': str(value)}
            assert finding.name == 'Solace Large Transfer Alert'
            assert finding.protocol == 'ethereum'
            assert finding.severity == FindingSeverity.Info
            assert finding.type == FindingType.Info

    def test_returns_medium_finding_if_value_above_threshold(self):
        value = 10000001000000000000000000
        tx_event = create_transaction_event({
            'transaction': {
                'from': FROM_ADDRESS,
                'to': SOLACE_CONTRACT,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(value, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 1
        for finding in findings:
            assert finding.alert_id == 'SOLACE-WHALE'
            assert finding.description == f'Address {FROM_ADDRESS} transferred to address {TO_ADDRESS} ' \
                                          f'SOLACE in the amount of {str(value)[:-DECIMALS]}'
            assert finding.metadata == {'from': FROM_ADDRESS, 'to': TO_ADDRESS, 'value': str(value)}
            assert finding.name == 'Solace Large Transfer Alert'
            assert finding.protocol == 'ethereum'
            assert finding.severity == FindingSeverity.Medium
            assert finding.type == FindingType.Info

    def test_returns_high_finding_if_value_above_threshold(self):
        value = 100000001000000000000000000
        tx_event = create_transaction_event({
            'transaction': {
                'from': FROM_ADDRESS,
                'to': SOLACE_CONTRACT,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(value, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 1
        for finding in findings:
            assert finding.alert_id == 'SOLACE-WHALE'
            assert finding.description == f'Address {FROM_ADDRESS} transferred to address {TO_ADDRESS} ' \
                                          f'SOLACE in the amount of {str(value)[:-DECIMALS]}'
            assert finding.metadata == {'from': FROM_ADDRESS, 'to': TO_ADDRESS, 'value': str(value)}
            assert finding.name == 'Solace Large Transfer Alert'
            assert finding.protocol == 'ethereum'
            assert finding.severity == FindingSeverity.High
            assert finding.type == FindingType.Info

    def test_returns_critical_finding_if_value_above_threshold(self):
        value = 1000000001000000000000000000
        tx_event = create_transaction_event({
            'transaction': {
                'from': FROM_ADDRESS,
                'to': SOLACE_CONTRACT,
                'hash': "0"
            },
            'receipt': {
                'logs': [transfer_event(value, SOLACE_CONTRACT)]}
        })

        findings = handle_transaction(tx_event)
        assert len(findings) == 1
        for finding in findings:
            assert finding.alert_id == 'SOLACE-WHALE'
            assert finding.description == f'Address {FROM_ADDRESS} transferred to address {TO_ADDRESS} ' \
                                          f'SOLACE in the amount of {str(value)[:-DECIMALS]}'
            assert finding.metadata == {'from': FROM_ADDRESS, 'to': TO_ADDRESS, 'value': str(value)}
            assert finding.name == 'Solace Large Transfer Alert'
            assert finding.protocol == 'ethereum'
            assert finding.severity == FindingSeverity.Critical
            assert finding.type == FindingType.Info
