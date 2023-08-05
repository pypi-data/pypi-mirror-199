from __future__ import annotations
import threading
from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List, Dict, Optional, TypeVar, Generic

from sapiopylib.rest.pojo.eln.ExperimentEntry import ExperimentEntry

from sapiopylib.rest.pojo.DataRecord import DataRecord

from sapiopylib.rest.pojo.DataRecordPaging import DataRecordPojoPageCriteria

from sapiopylib.rest.pojo.eln.ExperimentEntryCriteria import ExperimentEntryCriteriaUtil

from sapiopylib.rest.pojo.eln.SapioELNEnums import ElnExperimentStatus, ExperimentEntryStatus, ElnBaseDataType

from sapiopylib.rest.DataMgmtService import DataMgmtServer

from sapiopylib.rest.User import SapioUser

from sapiopylib.rest.pojo.eln.ElnExperiment import ElnExperiment, ElnExperimentUpdateCriteria


@total_ordering
class AbstractStep(ABC):
    """
    The protocol/step interface provides natural workflow abstraction for Sapio workflows.
    A protocol is consisted of multiple steps, in a sequential order.
    It is also a single process step for process tracking.
    A step holds the data and presentation config for a part of workflow.
    A step may be completed, active or unlocked.
    The data records that are part of the step are said to be attached to the step.
    """
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def set_name(self, new_name: str) -> None:
        pass

    @abstractmethod
    def get_data_type_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_records(self) -> List[DataRecord]:
        pass

    @abstractmethod
    def get_options(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def set_options(self, new_options: Dict[str, str]) -> None:
        pass

    @abstractmethod
    def complete_step(self) -> None:
        pass

    @abstractmethod
    def unlock_step(self) -> None:
        pass

    def __hash__(self):
        return hash(self.get_id())

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, AbstractStep):
            return False
        return self.get_id() == other.get_id()

    @abstractmethod
    def __le__(self, other):
        pass


ProtocolStepType: ProtocolStepType = TypeVar("ProtocolStepType", bound=AbstractStep)


@total_ordering
class AbstractProtocol(Generic[ProtocolStepType], ABC):
    """
    The protocol/step interface provides natural workflow abstraction for Sapio workflows.
    A protocol is consisted of multiple steps, in a sequential order.
    It is also a single process step for process tracking.
    A protocol may be completed, cancelled, or in progress.
    A step holds the data and presentation config for a part of workflow.
    The data records that are part of the step are said to be attached to the step.
    """
    @abstractmethod
    def complete_protocol(self) -> None:
        """
        Completing the protocol will complete the current ELN workflow.
        If there are any process-tracking enabled records, these records will advance into the next process step.
        """
        pass

    @abstractmethod
    def cancel_protocol(self) -> None:
        """
        Cancel the protocol will fail the current ELN workflow.
        If there are any process-tracking enabled records, these records will return to the previous return point.
        A return point is a configured process step to return to, in case a tracked record has failed a process step.
        """
        pass

    @abstractmethod
    def get_sorted_step_list(self) -> List[ProtocolStepType]:
        """
        Get the steps within this protocol in sequential order.
        """
        pass

    @abstractmethod
    def get_data_type_name(self) -> str:
        """
        Get the data type that holds the metadata for this protocol.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the protocol.
        """
        pass

    @abstractmethod
    def set_name(self, new_name: str) -> None:
        """
        Set the name of the protocol.
        """
        pass

    @abstractmethod
    def get_id(self) -> int:
        """
        Get the unique, system-wide identifier for the protocol.
        """
        pass

    @abstractmethod
    def get_options(self) -> Dict[str, str]:
        """
        Get the user-invisible options for the protocol. These can be used for certain plugins.
        """
        pass

    @abstractmethod
    def set_options(self, new_options:  Dict[str, str]) -> None:
        """
        Set the user-invisible options for the protocol. These can be used for certain plugins.
        """
        pass

    @abstractmethod
    def invalidate(self) -> None:
        """
        Invalidate the current cache, in case the data that is not part of the metadata has changed.
        """
        pass

    def get_first_step_of_type(self, data_type_name: str) -> Optional[ProtocolStepType]:
        """
        Get the first step in the protocol that attaches records of a particular data type.
        """
        target_base_type: ElnBaseDataType = ElnBaseDataType.get_base_type(data_type_name)
        steps = self.get_sorted_step_list()
        for step in steps:
            if data_type_name in step.get_data_type_names():
                return step
            if target_base_type is not None and \
                    target_base_type in [ElnBaseDataType.get_base_type(x) for x in step.get_data_type_names()]:
                return step
        return None

    def get_last_step_of_type(self, data_type_name: str) -> Optional[ProtocolStepType]:
        """
        Get the last step in the protocol that attaches records of a particular data type.
        """
        target_base_type: ElnBaseDataType = ElnBaseDataType.get_base_type(data_type_name)
        steps = reversed(self.get_sorted_step_list())
        for step in steps:
            if data_type_name in step.get_data_type_names():
                return step
            if target_base_type is not None and \
                    target_base_type in [ElnBaseDataType.get_base_type(x) for x in step.get_data_type_names()]:
                return step
        return None

    def get_next_step(self, current_step: AbstractStep, data_type_name: str) -> Optional[ProtocolStepType]:
        """
        Given the current step and a data type name to search for, find the next step after the current step by
        protocol's step sequential order that attaches records of the provided data type.
        This method will never return any steps before or at the provided step in the sequential order.
        """
        steps = self.get_sorted_step_list()
        # If this is the last step in the list, return nothing. Avoid wrapping around error when we +1.
        if steps[-1] == current_step:
            return None
        target_base_type: ElnBaseDataType = ElnBaseDataType.get_base_type(data_type_name)
        try:
            start_index = steps.index(current_step)
            for step in steps[start_index + 1:]:
                if data_type_name in step.get_data_type_names():
                    return step
                if target_base_type is not None and \
                        target_base_type in [ElnBaseDataType.get_base_type(x) for x in step.get_data_type_names()]:
                    return step
        except ValueError:
            return None
        return None

    def get_previous_step(self, current_step: AbstractStep, data_type_name: str) -> Optional[ProtocolStepType]:
        """
        Given the current step and a data type name to search for, find the previous step after the current step by
        protocol's step sequential order that attaches records of the provided data type.
        This method will never return any steps after or at the provided step in the sequential order.
        """
        steps = self.get_sorted_step_list()
        if steps[0] == current_step:
            return None
        target_base_type: ElnBaseDataType = ElnBaseDataType.get_base_type(data_type_name)
        try:
            end_index = steps.index(current_step)
            for step in steps[:end_index]:
                if data_type_name in step.get_data_type_names():
                    return step
                if target_base_type is not None and \
                        target_base_type in [ElnBaseDataType.get_base_type(x) for x in step.get_data_type_names()]:
                    return step
        except ValueError:
            return None
        return None

    def __hash__(self):
        return hash(self.get_id())

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, AbstractProtocol):
            return False
        return self.get_id() == other.get_id()

    def __le__(self, other):
        if other is None:
            return False
        if not isinstance(other, AbstractProtocol):
            return False
        return self.get_id() < other.get_id()

    def __str__(self):
        return self.get_name()

    def __len__(self):
        return self.get_sorted_step_list().__len__()

    def __iter__(self):
        return self.get_sorted_step_list().__iter__()


class ElnEntryStep(AbstractStep):
    """
    This is the ELN step implementation ELN-workflow.
    """
    eln_entry: ExperimentEntry
    protocol: ElnExperimentProtocol
    user: SapioUser

    def get_name(self) -> str:
        return self.eln_entry.entry_name

    def __init__(self, protocol: ElnExperimentProtocol,
                 eln_entry: ExperimentEntry):
        self.protocol = protocol
        self.user = protocol.user
        self.eln_entry = eln_entry

    def __le__(self, other):
        if other is None:
            return False
        if not isinstance(other, ElnEntryStep):
            return False
        protocol_step_list: List[AbstractStep] = self.protocol.get_sorted_step_list()
        try:
            return protocol_step_list.index(self) < protocol_step_list.index(other)
        except ValueError:
            return False

    def get_id(self) -> int:
        return self.eln_entry.entry_id

    def get_data_type_names(self) -> List[str]:
        if self.eln_entry.data_type_name:
            return [self.eln_entry.data_type_name]
        return []

    def get_records(self) -> List[DataRecord]:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        has_more_pages: bool = True
        next_page_criteria: Optional[DataRecordPojoPageCriteria] = None
        ret = []
        while has_more_pages:
            page_result = eln_manager.get_data_records_for_entry(self.protocol.get_id(), self.get_id(),
                                                                 paging_criteria=next_page_criteria)
            has_more_pages = page_result.is_next_page_available
            next_page_criteria = page_result.next_page_criteria
            ret.extend(page_result.result_list)
        return ret

    def get_options(self) -> Dict[str, str]:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        return eln_manager.get_experiment_entry_options(self.protocol.eln_experiment.notebook_experiment_id,
                                                        self.eln_entry.entry_id)

    def set_options(self, new_options: Dict[str, str]) -> None:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        entry_update_criteria = ExperimentEntryCriteriaUtil.create_empty_criteria(self.eln_entry)
        entry_update_criteria.entry_options_map = new_options
        eln_manager.update_experiment_entry(self.protocol.eln_experiment.notebook_experiment_id,
                                            self.eln_entry.entry_id, entry_update_criteria)

    def complete_step(self) -> None:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        eln_manager.submit_experiment_entry(self.protocol.eln_experiment.notebook_experiment_id,
                                            self.eln_entry.entry_id)

    def unlock_step(self) -> None:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        entry_update_criteria = ExperimentEntryCriteriaUtil.create_empty_criteria(self.eln_entry)
        entry_update_criteria.entry_status = ExperimentEntryStatus.UnlockedChangesRequired
        eln_manager.update_experiment_entry(self.protocol.eln_experiment.notebook_experiment_id,
                                            self.eln_entry.entry_id, entry_update_criteria)

    def set_name(self, new_name: str) -> None:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        entry_update_criteria = ExperimentEntryCriteriaUtil.create_empty_criteria(self.eln_entry)
        entry_update_criteria.entry_name = new_name
        eln_manager.update_experiment_entry(self.protocol.eln_experiment.notebook_experiment_id,
                                            self.eln_entry.entry_id, entry_update_criteria)


class ElnExperimentProtocol(AbstractProtocol[ElnEntryStep]):
    """
    This is an ELN-workflow implementation of the workflow protocol.
    """
    sorted_step_list: Optional[List[ElnEntryStep]]
    eln_experiment: ElnExperiment
    user: SapioUser
    lock: threading.RLock

    def __init__(self, eln_experiment: ElnExperiment, user: SapioUser):
        self.lock = threading.RLock()
        self.eln_experiment = eln_experiment
        self.user = user
        self.sorted_step_list = None

    def invalidate(self) -> None:
        with self.lock:
            self.sorted_step_list = None

    def get_data_type_name(self) -> str:
        return self.eln_experiment.experiment_data_type_name

    def get_name(self) -> str:
        return self.eln_experiment.notebook_experiment_name

    def set_name(self, new_name: str) -> None:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        update_criteria: ElnExperimentUpdateCriteria = ElnExperimentUpdateCriteria(new_experiment_name=new_name)
        eln_manager.update_notebook_experiment(self.eln_experiment.notebook_experiment_id, update_criteria)

    def get_id(self) -> int:
        return self.eln_experiment.notebook_experiment_id

    def get_options(self) -> Dict[str, str]:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        return eln_manager.get_notebook_experiment_options(self.eln_experiment.notebook_experiment_id)

    def set_options(self, new_options:  Dict[str, str]) -> None:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        update_criteria: ElnExperimentUpdateCriteria = ElnExperimentUpdateCriteria(experiment_option_map=new_options)
        eln_manager.update_notebook_experiment(self.eln_experiment.notebook_experiment_id, update_criteria)

    def get_sorted_step_list(self) -> List[ElnEntryStep]:
        with self.lock:
            if self.sorted_step_list is not None:
                return self.sorted_step_list
            else:
                eln_manager = DataMgmtServer.get_eln_manager(self.user)
                entry_list = eln_manager.get_experiment_entry_list(self.eln_experiment.notebook_experiment_id,
                                                                   to_retrieve_field_definitions=False)
                sorted_step_list = []
                for entry in entry_list:
                    step = ElnEntryStep(self, entry)
                    sorted_step_list.append(step)
                self.sorted_step_list = sorted_step_list
                return self.sorted_step_list

    def complete_protocol(self) -> None:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        update_criteria: ElnExperimentUpdateCriteria = ElnExperimentUpdateCriteria(
            new_experiment_status=ElnExperimentStatus.Completed)
        eln_manager.update_notebook_experiment(self.eln_experiment.notebook_experiment_id, update_criteria)

    def cancel_protocol(self) -> None:
        eln_manager = DataMgmtServer.get_eln_manager(self.user)
        update_criteria: ElnExperimentUpdateCriteria = ElnExperimentUpdateCriteria(
            new_experiment_status=ElnExperimentStatus.Canceled)
        eln_manager.update_notebook_experiment(self.eln_experiment.notebook_experiment_id, update_criteria)
