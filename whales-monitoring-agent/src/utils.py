from forta_agent import FindingSeverity

from src.constants import TRANSFER_AMOUNT_TH_CRITICAL, TRANSFER_AMOUNT_TH_HIGH, TRANSFER_AMOUNT_TH_MEDIUM


def extract_argument(event: dict, argument: str) -> any:
    """
    the function extract specified argument from the event
    :param event: dict
    :param argument: str
    :return: argument value
    """
    return event.get('args', {}).get(argument, "")


def get_severity(amount):
    """
    the function determines the severity level of the finding
    :param amount:
    :return: FindingSeverity
    """
    if amount > TRANSFER_AMOUNT_TH_CRITICAL:
        return FindingSeverity.Critical
    elif amount > TRANSFER_AMOUNT_TH_HIGH:
        return FindingSeverity.High
    elif amount > TRANSFER_AMOUNT_TH_MEDIUM:
        return FindingSeverity.Medium
    else:
        return FindingSeverity.Info
