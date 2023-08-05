from typing import Optional, List, Dict, Any

from sapiopylib.rest.DataMgmtService import DataMgmtServer

from sapiopylib.rest.ELNService import ElnManager

from sapiopylib.rest.DataRecordManagerService import DataRecordManager

from sapiopylib.rest.pojo.DataRecord import DataRecord

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.eln.ElnExperiment import ElnExperiment, ELNExperimentParser
from sapiopylib.rest.pojo.eln.ExperimentEntry import ExperimentEntry, ExperimentEntryParser
from sapiopylib.rest.pojo.reportbuilder.VeloxReportBuilder import RbTemplatePopulatorData, VeloxReportBuilderParser
from sapiopylib.rest.pojo.webhook.ClientCallbackResult import ClientCallbackResultParser, AbstractClientCallbackResult
from sapiopylib.rest.pojo.webhook.VeloxRules import VeloxTypedRuleResult, ElnEntryRecordResult, VeloxRuleParser
from sapiopylib.rest.pojo.webhook.WebhookEnums import WebhookEndpointType
from sapiopylib.rest.utils.Protocols import AbstractProtocol, ElnExperimentProtocol, \
    AbstractStep, ElnEntryStep


class SapioWebhookContext:
    """
    The webhook context structure after receiving a request from Sapio Informatics Platform.

    Obtain your context variables here.
    """
    user: SapioUser

    data_record_manager: DataRecordManager
    eln_manager: ElnManager
    active_protocol: Optional[AbstractProtocol]
    active_step: AbstractStep

    end_point_type: WebhookEndpointType

    data_record: Optional[DataRecord]
    base_data_record: Optional[DataRecord]
    data_record_list: Optional[List[DataRecord]]
    data_type_name: Optional[str]
    data_field_name: Optional[str]

    velox_on_save_result_map: Optional[Dict[int, List[VeloxTypedRuleResult]]]
    velox_eln_rule_result_map: Optional[Dict[str, List[ElnEntryRecordResult]]]

    experiment_entry_list: Optional[List[ExperimentEntry]]
    experiment_entry: Optional[ExperimentEntry]
    eln_experiment: Optional[ElnExperiment]
    client_callback_result: Optional[AbstractClientCallbackResult]
    is_client_callback_available: bool

    report_builder_template_populator_data: Optional[RbTemplatePopulatorData]

    field_map_list: Optional[List[Dict[str, Any]]]
    field_map: Optional[Dict[str, Any]]
    selected_field_map_index_list: Optional[List[int]]

    def __init__(self, user: SapioUser, end_point_type: WebhookEndpointType):
        self.user = user
        self.end_point_type = end_point_type
        self.data_record_manager = DataMgmtServer.get_data_record_manager(user)
        self.eln_manager = DataMgmtServer.get_eln_manager(user)


class SapioWebhookContextParser:
    @staticmethod
    def parse_endpoint_type_from_display_name(endpoint_type_display_name: str):
        for endpoint in WebhookEndpointType:
            if endpoint.display_name == endpoint_type_display_name:
                return endpoint
        return None

    @staticmethod
    def parse_webhook(json_dct: Dict[str, Any],
                      timeout_seconds=60,
                      verify_ssl_cert=True) -> SapioWebhookContext:
        endpoint_type_display_name = json_dct.get('endpointType')
        end_point_type = SapioWebhookContextParser.parse_endpoint_type_from_display_name(endpoint_type_display_name)
        webservice_url: str = json_dct.get('webserviceUrl')
        # Remove trailing "/"
        if webservice_url.endswith('/'):
            webservice_url = webservice_url[:-len('/')]
        api_token: str = json_dct.get('webhookApiToken')
        username: str = json_dct.get('username')
        app_guid: str = json_dct.get('appGuid')
        user: SapioUser = SapioUser(url=webservice_url, verify_ssl_cert=verify_ssl_cert,
                                    timeout_seconds=timeout_seconds, api_token=api_token,
                                    username=username, guid=app_guid)
        data_record: Optional[DataRecord] = None
        if json_dct.get('dataRecordPojo') is not None:
            data_record = DataRecord.from_json(json_dct.get('dataRecordPojo'))
        base_data_record: Optional[DataRecord] = None
        if json_dct.get('baseDataRecordPojo') is not None:
            base_data_record = DataRecord.from_json(json_dct.get('baseDataRecordPojo'))
        data_record_list: Optional[List[DataRecord]] = None
        if json_dct.get('dataRecordPojoList') is not None:
            data_record_list = [DataRecord.from_json(x) for x in json_dct.get('dataRecordPojoList')]
        data_type_name: Optional[str] = json_dct.get('dataTypeName')
        data_field_name: Optional[str] = json_dct.get('dataFieldName')

        velox_on_save_result_map: Optional[Dict[int, List[VeloxTypedRuleResult]]] = None
        if json_dct.get('veloxOnSaveResultMap') is not None:
            velox_on_save_result_map = dict()
            pojo_map: Dict[int, List[Dict[str, Any]]] = json_dct.get('veloxOnSaveResultMap')
            for key, value in pojo_map.items():
                result_list: List[VeloxTypedRuleResult] = [VeloxRuleParser.parse_velox_typed_rule_result(x)
                                                           for x in value]
                velox_on_save_result_map[key] = result_list
        velox_eln_rule_result_map: Optional[Dict[str, List[ElnEntryRecordResult]]] = None
        if json_dct.get('veloxElnRuleResultMap') is not None:
            velox_eln_rule_result_map = dict()
            pojo_map: Dict[str, List[Dict[str, Any]]] = json_dct.get('veloxElnRuleResultMap')
            for key, value in pojo_map.items():
                result_list: List[ElnEntryRecordResult] = [VeloxRuleParser.parse_eln_record_result(x) for x in value]
                velox_eln_rule_result_map[key] = result_list

        experiment_entry_list: Optional[List[ExperimentEntry]] = None
        if json_dct.get('elnExperimentEntryPojoList') is not None:
            experiment_entry_list = [ExperimentEntryParser.parse_experiment_entry(x) for
                                     x in json_dct.get('elnExperimentEntryPojoList')]
        experiment_entry: Optional[ExperimentEntry] = None
        if json_dct.get('elnExperimentEntryPojo') is not None:
            experiment_entry = ExperimentEntryParser.parse_experiment_entry(json_dct.get('elnExperimentEntryPojo'))
        notebook_experiment: Optional[ElnExperiment] = None
        if json_dct.get('notebookExperimentPojo') is not None:
            notebook_experiment = ELNExperimentParser.parse_eln_experiment(json_dct.get('notebookExperimentPojo'))
        client_callback_result: Optional[AbstractClientCallbackResult] = None
        if json_dct.get('clientCallbackResult') is not None:
            client_callback_result = ClientCallbackResultParser.parse_client_callback_result(
                json_dct.get('clientCallbackResult'))
        is_client_callback_available: bool = json_dct.get('clientCallbackAvailable')

        report_builder_template_populator_data: Optional[RbTemplatePopulatorData] = None
        if json_dct.get('rbTemplatePopulatorDataPojo') is not None:
            report_builder_template_populator_data = VeloxReportBuilderParser.parse_template_populator_data(
                json_dct.get('rbTemplatePopulatorDataPojo'))

        field_map_list: Optional[List[Dict[str, Any]]] = json_dct.get('fieldMapList')
        field_map: Optional[Dict[str, Any]] = json_dct.get('fieldMap')
        selected_field_map_index_list: Optional[List[int]] = json_dct.get('selectedFieldMapIdxList')

        ret: SapioWebhookContext = SapioWebhookContext(user, end_point_type)
        ret.data_record = data_record
        ret.base_data_record = base_data_record
        ret.data_record_list = data_record_list
        ret.data_type_name = data_type_name
        ret.data_field_name = data_field_name
        ret.velox_on_save_result_map = velox_on_save_result_map
        ret.velox_eln_rule_result_map = velox_eln_rule_result_map
        ret.experiment_entry_list = experiment_entry_list
        ret.experiment_entry = experiment_entry
        ret.eln_experiment = notebook_experiment
        ret.client_callback_result = client_callback_result
        ret.is_client_callback_available = is_client_callback_available
        ret.report_builder_template_populator_data = report_builder_template_populator_data
        ret.field_map_list = field_map_list
        ret.field_map = field_map
        ret.selected_field_map_index_list = selected_field_map_index_list

        if ret.eln_experiment is not None:
            ret.active_protocol = ElnExperimentProtocol(eln_experiment=ret.eln_experiment, user=ret.user)
            if ret.experiment_entry is not None:
                ret.active_step = ElnEntryStep(protocol=ret.active_protocol, eln_entry=ret.experiment_entry)

        return ret
