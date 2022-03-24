import eth_abi
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from eth_utils import encode_hex, function_abi_to_4byte_selector, keccak
from src.agent import handle_transaction, SETREWARD_ABI, SETTIMES_ABI

from src.constants import STAKINGREWARDS_CONTRACT

REWARDSSET = "RewardsSet(uint256)"
FARMTIMESET = "FarmTimesSet(uint256,uint256)"

all_events = [REWARDSSET, FARMTIMESET]
functions_abi = [SETREWARD_ABI, SETTIMES_ABI]

ONE_ADDRESS = "0x1111111111111111111111111111111111111111"
TWO_ADDRESS = "0x2222222222222222222222222222222222222222"


def rewardset_event(contract_address: str):
    hash = keccak(text=REWARDSSET)
    data = eth_abi.encode_abi(["uint256"], [0])
    data = encode_hex(data)
    topics = [hash]
    return {'topics': topics,
            'data': data,
            'address': contract_address}


def farmtimeset_event(contract_address: str):
    hash = keccak(text=FARMTIMESET)
    data = eth_abi.encode_abi(["uint256", "uint256"], [0, 0])
    data = encode_hex(data)
    topics = [hash]
    return {'topics': topics,
            'data': data,
            'address': contract_address}


func = function_abi_to_4byte_selector(SETREWARD_ABI)
params = eth_abi.encode_abi(["uint256"], [0])
setrewards_data = encode_hex(func + params)

func = function_abi_to_4byte_selector(SETTIMES_ABI)
params = eth_abi.encode_abi(["uint256", "uint256"], [0, 0])
settime_data = encode_hex(func + params)


class TestSolaceWhalesAgent:
    def test_returns_empty_findings_if_there_is_no_target_event_in_the_logs(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            }})

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_empty_findings_if_the_contract_address_is_not_stakingrewards(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            },
            'receipt': {
                'logs': [rewardset_event(TWO_ADDRESS)]}})

        findings = handle_transaction(tx_event)
        assert len(findings) == 0

    def test_returns_findings_for_rewardset_event(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            },
            'receipt': {
                'logs': [rewardset_event(STAKINGREWARDS_CONTRACT)]}})

        findings = handle_transaction(tx_event)
        assert len(findings) != 0
        for finding in findings:
            assert finding.alert_id == 'STAKINGREWARDS-EVENT'
            assert finding.description == f'Contract event RewardsSet was emitted by {STAKINGREWARDS_CONTRACT}'
            assert finding.metadata == {'event': 'RewardsSet', 'rewardPerSecond': 0}
            assert finding.name == 'StakingRewards Event Alert'
            assert finding.severity == FindingSeverity.Info
            assert finding.type == FindingType.Info

    def test_returns_findings_for_farmtimeset_event(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': TWO_ADDRESS,
                'hash': "0"
            },
            'receipt': {
                'logs': [farmtimeset_event(STAKINGREWARDS_CONTRACT)]}})

        findings = handle_transaction(tx_event)
        assert len(findings) != 0
        for finding in findings:
            assert finding.alert_id == 'STAKINGREWARDS-EVENT'
            assert finding.description == f'Contract event FarmTimesSet was emitted by {STAKINGREWARDS_CONTRACT}'
            assert finding.metadata == {'event': 'FarmTimesSet', 'endTime': 0, 'startTime': 0}
            assert finding.name == 'StakingRewards Event Alert'
            assert finding.severity == FindingSeverity.Info
            assert finding.type == FindingType.Info

    def test_returns_findings_for_setrewards_function(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': STAKINGREWARDS_CONTRACT,
                'hash': "0",
                'data': setrewards_data
            }})

        findings = handle_transaction(tx_event)
        assert len(findings) != 0
        for finding in findings:
            assert finding.alert_id == 'STAKINGREWARDS-FUNCTION'
            assert finding.description == f'Contract function setRewards was called'
            assert finding.metadata == {'function': 'setRewards', 'rewardPerSecond_': 0}
            assert finding.name == 'StakingRewards Function Alert'
            assert finding.severity == FindingSeverity.Info
            assert finding.type == FindingType.Info

    def test_returns_findings_for_settimes_function(self):
        tx_event = create_transaction_event({
            'transaction': {
                'from': ONE_ADDRESS,
                'to': STAKINGREWARDS_CONTRACT,
                'hash': "0",
                'data': settime_data
            }})

        findings = handle_transaction(tx_event)
        assert len(findings) != 0
        for finding in findings:
            assert finding.alert_id == 'STAKINGREWARDS-FUNCTION'
            assert finding.description == f'Contract function setTimes was called'
            assert finding.metadata == {'function': 'setTimes', 'endTime_': 0, 'startTime_': 0}
            assert finding.name == 'StakingRewards Function Alert'
            assert finding.severity == FindingSeverity.Info
            assert finding.type == FindingType.Info
