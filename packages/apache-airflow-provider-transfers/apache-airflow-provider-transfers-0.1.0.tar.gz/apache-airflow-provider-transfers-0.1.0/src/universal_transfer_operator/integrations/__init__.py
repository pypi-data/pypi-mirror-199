import importlib

from airflow.hooks.base import BaseHook

from universal_transfer_operator.constants import IngestorSupported
from universal_transfer_operator.integrations.base import TransferIntegration, TransferIntegrationOptions
from universal_transfer_operator.utils import get_class_name

CUSTOM_INGESTION_TYPE_TO_MODULE_PATH = {"fivetran": "universal_transfer_operator.integrations.fivetran"}


def get_transfer_integration(transfer_params: TransferIntegrationOptions) -> TransferIntegration:
    """
    Given a transfer_params return the associated TransferIntegrations class.

    :param transfer_params: kwargs to be used by methods involved in transfer using FiveTran.
    """
    thirdparty_conn_id = transfer_params.conn_id

    if thirdparty_conn_id is None:
        raise ValueError("Connection id for integration is not specified.")
    thirdparty_conn_type = BaseHook.get_connection(thirdparty_conn_id).conn_type
    if thirdparty_conn_type not in {item.value for item in IngestorSupported}:
        raise ValueError("Ingestion platform not yet supported.")

    module_path = CUSTOM_INGESTION_TYPE_TO_MODULE_PATH[thirdparty_conn_type]
    module = importlib.import_module(module_path)
    class_name = get_class_name(module_ref=module, suffix="Integration")
    transfer_integrations: TransferIntegration = getattr(module, class_name)(transfer_params)
    return transfer_integrations
