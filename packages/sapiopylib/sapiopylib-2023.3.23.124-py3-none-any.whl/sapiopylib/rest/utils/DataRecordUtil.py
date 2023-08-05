from typing import List, Dict, Any

from sapiopylib.rest.pojo.DataRecord import DataRecord


class DataRecordUtil:
    """
    Includes a collection of utilities that can be used for DataRecord objects.
    """
    @staticmethod
    def get_record_map_by_data_type(records: List[DataRecord]) -> Dict[str, List[DataRecord]]:
        """
        Given a list of data records, return a dict so that they key is the data type name,
        and value is a list of records of the data type.
        :param records: The list of data records to map by data type name.
        :return: A map of data records keyed by their data type name.
        """
        ret: Dict[str, List[DataRecord]] = dict()
        for record in records:
            data_type_name = record.get_data_type_name()
            if data_type_name not in ret:
                ret[data_type_name] = []
            ret[data_type_name].append(record)
        return ret

    @staticmethod
    def get_value_list(records: List[DataRecord], field_name: str) -> list:
        """
        Obtain a list of values of a data record of a data field
        :param field_name: The data field to obtain values for.
        :param records: The records to obtain values for.
        """
        return [x.get_field_value(field_name) for x in records]

    @staticmethod
    def map_records_by_value(records: List[DataRecord], field_name: str) -> Dict[Any, DataRecord]:
        """
        Assuming the values are unique among the list of data records, obtain a
        dictionary of (Value) -> (The Data Record that contains this value)
        """
        ret: Dict[Any, DataRecord] = dict()
        for record in records:
            field_value = record.get_field_value(field_name)
            ret[field_value] = record
        return ret

    @staticmethod
    def multi_map_records_by_value(records: List[DataRecord], field_name: str) -> Dict[Any, List[DataRecord]]:
        """
        Return the dictionary of (Value) -> (A list of data records that contains this value)
        """
        ret: Dict[Any, List[DataRecord]] = dict()
        for record in records:
            field_value = record.get_field_value(field_name)
            if field_value not in ret:
                ret[field_value] = []
            ret[field_value].append(record)
        return ret

