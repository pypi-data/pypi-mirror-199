# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, invalid-name, too-many-arguments, trailing-whitespace
"""Orchestrator Module: A client to interact with Orchestrator's API. This module contains different
Resources to interact at different levels.
To start it is recommended that you instantiate an :code:`Orchestrator` object, and from it instantiate other
Resources you may need along the way. For example, to get to a specific :code:`QueueItem` object, we need first to naviage to the folder where this
:code:`QueueItem` is located; then we need to the the :code:`Queue` it belongs, to finally access it.
"""

from __future__ import annotations
import os
from pprint import pprint
import datetime
from datetime import timedelta
import json
import pandas as pd
import logging
from typing import Any, Literal, Mapping, Union, List, Optional, Set, Dict
from uuid import uuid4
import asyncio
from dateutil.parser import parse

# from cron_descriptor import get_description
import httpx
from .client import Client
from .orchestrator_resource import Resource


def format_date(date_str: str) -> Any:
    """Auxiliar function to parse a date with timezone offset"""
    # tz = time.tzname[0]
    return parse(date_str)


class QueueItem(Resource):
    """Class to handle a QueueItem type Resource"""

    _type = "queue_item"
    _def_endpoint = "/odata/QueueItems({id})"

    # pylint: disable=redefined-builtin, broad-except
    def __init__(
        self,
        id: Union[int, str],
        name: str,
        client: Client,
        status: str,
        item_data: dict[str, Any],
        reference: Optional[str],
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.item_data = item_data
        self.status = status
        self.reference = reference

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.item_data

    def key(self):
        return self.item_data["Key"]

    def refresh(self):
        data = self.client.get(self._def_endpoint.format(id=self.id))
        self.item_data = data
        self.status = data["Status"]

    def _prepare_body_edit_item(
        self, priority, content: Mapping[str, Any], ref, prog: str = ""
    ):
        body = {
            "Name": self.queue.name,
            "Priority": priority,
            "SpecificContent": content,
            "Reference": ref,
            "Progress": prog,
        }
        return body

    def edit(
        self,
        content: Mapping[str, Any],
        priority: str = "",
        progress: str = "",
        reference: str = "",
    ) -> QueueItem:
        """Edits the QueueItem.
        :param content: the SpecificContent of the QueueItem
        :type content: Mapping[str, Any]
        :param priority: optional new Priority attribute
        :type priority: str
        :param progress: optional new Progress attribute
        :type progress: str
        :param reference: optional new Reference attribute
        :type reference: str
        """
        if self.status not in ("New", "Failed", "Abandoned"):
            raise TypeError("Only New, Failed and Abandoned queue items are editable.")
        if not priority:
            priority = self.item_data["Priority"]
        if not progress:
            progress = self.item_data["Progress"]
        if not reference:
            reference = self.item_data["Reference"]
        body = self._prepare_body_edit_item(priority, content, reference, progress)
        self.client.put(endpoint=self._def_endpoint.format(id=self.id), body=body)
        self.item_data["SpecificContent"] = content
        self.item_data["Priority"] = priority
        self.reference = reference
        return self

    def delete(self):
        self.client.delete(endpoint=self._def_endpoint.format(id=self.id))

    @staticmethod
    def _prepare_result_body_success() -> dict[str, Any]:
        success_body = {
            "transactionResult": {
                "IsSuccessful": True,
            }
        }
        return success_body

    @staticmethod
    def _prepare_result_body_failure(reason: str, details: str, exc: str, fail: str):
        failure_body = {
            "transactionResult": {
                "IsSuccessful": False,
                "ProcessingException": {
                    "Reason": reason,
                    "Details": details,
                    "Type": exc,
                },
                "Output": {"fail_reason": fail},
            }
        }
        return failure_body

    def set_transaction_result(
        self,
        success: bool,
        reason: str = "",
        details: str = "",
        exception_type: str = "BusinessRuleException",
        failure: str = "",
    ):
        """Sets the transaction result of a QueueItem resource.
        :param success: indicates whether the transaction has been a success. If :code:`True` then no more arguments are needed.
        :type success: bool
        :param reason: (optional) reason why the transaction failed
        :type reason: str
        :param details: (optionl) more details on why the transaction failed
        :type details: str
        :param exception_type: (optional) exception type
        :type exception_type: str
        """
        queue_item_endpoint = f"/odata/Queues({self.id})"
        uipath_svc = "/UiPathODataSvc.SetTransactionResult"
        endpoint = queue_item_endpoint + uipath_svc
        if success:
            body = self._prepare_result_body_success()
            self.status = "Successful"
        else:
            body = self._prepare_result_body_failure(
                reason, details, exception_type, failure
            )
            self.status = "Failed"
        data = self.client.post(endpoint=endpoint, body=body)
        return data


def raise_no_pool(f):
    """Raises an AttributeError if a process which calls Queue.items
    has been called without setting the QueueItem pool."""

    def wrapper(self, *args, **kwargs):
        assert isinstance(self, Queue)
        if not self.items:
            raise AttributeError(
                f"item_pool has been set to False but method '{f.__name__}' of '{type(self).__name__}' requires a QueueItems pool."
            )
        return f(self, *args, **kwargs)

    return wrapper


class Queue(Resource):
    """Class to manage a Queue type Resource"""

    _MAX_ITEMS = 1000
    _type = "queue_definition"
    _def_endpoint = "/odata/QueueDefinitions({id})"

    # pylint: disable=redefined-builtin
    def __init__(
        self,
        id: int,
        name: str,
        queue_data: Mapping[str, Any],
        client: Client,
        item_pool: bool,
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.queue_data = queue_data
        if item_pool:
            self.dataframe = asyncio.run(self.get_async_dataframe())
        else:
            self.dataframe = None
        self.new_items = asyncio.run(self.get_async_new_items())

    def info(self):
        return self.queue_data

    def key(self):
        pass

    def start_item(self, machine_identifier: str):
        current = self.new_items.pop()
        content = current.item_data
        reference = current.reference
        current.delete()  # deletes the item
        body_start = {
            "transactionData": {
                "Name": self.name,
                "RobotIdentifier": machine_identifier,
                "SpecificContent": content,
                "Reference": reference,
            }
        }
        return self._start_item(body_start)

    def _start_item(self, body_start: Mapping[str, Any]):
        endpoint = "/odata/Queues/UiPathODataSvc.StartTransaction"
        data = self.client.post(endpoint, body=body_start)
        queue_item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            status=data["Status"],
            item_data=data["SpecificContent"],
            reference=data["Reference"],
        )
        return queue_item

    def _filter_dataframe(
        self, df: pd.DataFrame, references: List[str], separator: str = "-"
    ) -> pd.DataFrame:
        """Given a dataframe of specific contents, it matches it agains the Queue and returns the original DataFrame
        minus the ones that appeared already in the Queue based on the `references` parameter provided.

        :param df: a dataframe comprising the SpecificContent attributes of the item to be processed
        :type df: pd.DataFrame
        :param references: a list of references to form the Reference attributes to match agains the Queue
        :type references: List[str]
        :param separator: a string separator used to concatenate references in case there are more than 1
        :type separator: str (default = '-')
        :returns: pandas DataFrame consisting of those rows which are not duplicates based on the references

        """
        contents = self._dataframe_to_contents(
            df,
            priority="Normal",
            references=references,
            batch_id=str(uuid4()),
            separator=separator,
        )
        df_contents = pd.DataFrame(contents)
        print(self.dataframe)
        result = df_contents[
            ~df_contents["Reference"].apply(
                lambda x: any(self.dataframe["Reference"].str.contains(x.split("#")[0]))
            )
        ]
        return pd.DataFrame(result["SpecificContent"].to_list())

    def check_duplicate(
        self, values: List[Any], separator: str = "-"
    ) -> Union[False, QueueItem]:
        """Given a list of valuesm checks whether an item already appears in the Queue with status
        other than Failed

        :param values: a list of values that form the reference of that particular item
        :type values: List[Any]
        :param separator: a separator used to concatenate the values for the reference
        :type values: str (DEFAULT = '-')
        :returns: Either a False if the item does not appear or the QueueItem if it exists
        :rtype: Union[False, QueueItem]
        """
        new_ref = ""
        for val in values:
            new_ref += val + separator
        new_ref = new_ref[:-1]
        try:
            duplicate = self.dataframe[
                self.dataframe["Reference"].str.startswith(new_ref)
            ]
            print(duplicate)
        except Exception:
            return False
        try:
            assert len(duplicate) == 1
        except AssertionError:
            raise Exception(f"Multiple results found with reference {new_ref}")
        return QueueItem(
            id=duplicate.iloc[0]["Id"],
            name=self.name,
            client=self.client,
            status=duplicate.iloc[0]["Status"],
            item_data=duplicate.iloc[0]["SpecificContent"],
            reference=duplicate.iloc[0]["Reference"],
        )

    def refresh(self):
        data = self.client.get(self._def_endpoint.format(id=self.id))
        self.queue_data = data
        if self.name != data["Name"]:
            logging.warning(
                f"User tried to overwrite Queue name <{data['Name']}> with <{self.name}>."
            )
        self.name = data["Name"]

    def _format_reference(self, sp, references, separator, batch_id) -> str:
        """Formats the Reference of a QueueItem following the format

        ```
        <ref1><separator><ref2><separator>...#<batch_id>
        ```
        """
        ref_part = ""
        for ref in references:
            try:
                ref_part += sp[ref] + separator
            except KeyError as err:
                raise KeyError(
                    f"Key {ref} not found in specific content, please check again"
                ) from err
        new_ref = ref_part[:-1] + "#" + batch_id
        return new_ref

    def _format_specific_content(
        self, sp, reference, batch_id: str
    ) -> Mapping[str, Any]:
        """Formats the specific content adding the following fields:
        1. BatchID. The `uuid4` identifying the batch upload
        2. ReferenceID. A unique `uuid4` identifier for the QueueItem
        3. ItemID. The first reference of the queueItem
        """
        new_sp = sp
        new_sp["BatchID"] = batch_id
        new_sp["ReferenceID"] = str(uuid4())
        new_sp["ItemID"] = reference
        return new_sp

    def _dataframe_to_contents(
        self,
        df: pd.DataFrame,
        priority: str,
        references: Optional[List[str]],
        batch_id: str,
        separator: str,
    ):
        """Parses the contents of a dataframe into SpecificContent attributes of QueueItems to add in bulk"""
        contents = []
        for _, row in df.iterrows():
            sp = row.to_dict()
            fmt_reference = self._format_reference(sp, references, separator, batch_id)
            fmt_sp = self._format_specific_content(sp, sp[references[0]], batch_id)
            queue_item = {
                "Name": self.name,
                "Priority": priority,
                "SpecificContent": fmt_sp,
                "Reference": fmt_reference,
            }
            contents.append(queue_item)
        return contents

    def bulk_add(
        self,
        df: pd.Dataframe,
        priority: str = "Normal",
        references: List[str] = None,
        batch_id: str = "",
        separator: str = "-",
    ):
        """Adds the contents of a DataFrame as new QueueItems to the Queue. It requires a unique identifier for the item as a reference list

        :param df: the pandas DataFrame of items to upload to the Queue. The columns will be translated to values for the SpecificContent attributes of the QueueItems
        :type df: pd.DataFrame
        :param priority: the priority to process each item (default: :code:`Normal`)
        :type priority: str
        :param references: a list of strings, each representing a key of the SpecificContent from which to form a unique identifier for the QueueItem
        :type references: List[str]
        :param batch_id: a unique identifier for the upload. In case none is provided, a default uuid4 is set
        :type batch_id: str
        :param separator: a separator character to use to separate each reference (default: :code:`-`)
        :type separator: str
        """
        endpoint = "/odata/Queues/UiPathODataSvc.BulkAddQueueItems"
        if not batch_id:
            batch_id = str(uuid4())
        contents = self._dataframe_to_contents(
            df, priority, references, batch_id, separator
        )
        body = {
            "queueName": self.name,
            "commitType": "AllOrNothing",
            "queueItems": contents,
        }
        return self.client.post(endpoint, body=body)

    def add(
        self,
        content: Mapping[str, Union[str, int]],
        priority: str = "Normal",
        references: Optional[List[str]] = None,
        batch_id: str = "",
        separator: str = "-",
    ) -> QueueItem:
        """Adds a new QueueItem resource to the queue with status :code:`New` and returns it to be processed.

        :param content: the SpecificContent of the item
        :type content: Mapping[str, Union[str, int]]
        :param priority: optional Priority attribute (default = :code:`Normal`)
        :type priority: str
        :param references: optional list of references.
        :type references: Optional[List[str]]
        :param batch_id: a unique batch identificatos
        :type batch_id: str
        :param separator: optional character to separate the references if any (default = :code:`-`).
        :type separator: str
        :rtype: QueueItem
        """
        if not batch_id:
            batch_id = str(uuid4())
        body = self._format_new_queue_item_body(
            content=content,
            priority=priority,
            refs=references,
            batch_id=batch_id,
            separator=separator,
        )
        endpoint = "/odata/Queues/UiPathODataSvc.AddQueueItem"
        data = self.client.post(endpoint, body=body)
        queue_item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            status=data["Status"],
            item_data=data["SpecificContent"],
            reference=data["Reference"],
        )
        return queue_item

    def _format_new_queue_item_body(
        self,
        content,
        priority: Optional[str] = None,
        refs: Optional[List[str]] = None,
        batch_id: str = "",
        separator: str = "-",
    ):
        ref_id = str(uuid4())
        body_add = {
            "itemData": {
                "Priority": priority,
                "Name": self.name,
                "SpecificContent": content,
            }
        }
        if refs:
            reference = ""
            for ref in refs:
                try:
                    ref_value = body_add["itemData"]["SpecificContent"][ref]
                except KeyError as exc:
                    raise ValueError(
                        f"Invalid reference: {ref} not found as attribute in SpecificContent"
                    ) from exc
                reference += str(ref_value) + separator
                body_add["itemData"]["Reference"] = f"{reference[:-1]}#{batch_id}"
                body_add["itemData"]["SpecificContent"]["ItemID"] = reference[:-1]
                body_add["itemData"]["SpecificContent"]["ReferenceID"] = ref_id
                body_add["itemData"]["SpecificContent"]["BatchID"] = batch_id
        return body_add

    def _format_transaction_body(
        self,
        machine_identifier,
        content,
        batch_id,
        refs: Optional[List[str]] = None,
        separator: Optional[str] = "-",
    ) -> dict[str, Any]:
        ref_id = str(uuid4())
        body_start = {
            "transactionData": {
                "Name": self.name,
                "RobotIdentifier": machine_identifier,
                "SpecificContent": content,
            }
        }
        if refs:
            reference = ""
            for ref in refs:
                try:
                    ref_value = body_start["transactionData"]["SpecificContent"][ref]
                except KeyError as exc:
                    raise ValueError(
                        f"Invalid reference: {ref} not found as attribute in SpecificContent"
                    ) from exc
                reference += f"{str(ref_value)}{separator}"
            body_start["transactionData"]["Reference"] = f"{reference[:-1]}#{batch_id}"
            body_start["transactionData"]["SpecificContent"]["ItemID"] = reference[:-1]
            body_start["transactionData"]["SpecificContent"]["ReferenceID"] = ref_id
            body_start["transactionData"]["SpecificContent"]["BatchID"] = batch_id
        return body_start

    def start(
        self,
        machine_identifier: str,
        content: Mapping[str, Union[str, int]],
        batch_id: str = "",
        references: Optional[List[str]] = None,
        separator="-",
    ) -> QueueItem:
        """Starts a new transaction and sends back the item to be processed.

        :param machine_identifier: the unique identifier of your machine.
        :param content: the SpecificContent attrubitue of you transaction.
        :param batch_id: an optional unique id for batch transactions.
        :param references: an optional list of references to be hashed.
        :param separator: an optional character to hash the references.
        :type machine_identifier: str.
        :type content: Mapping[str, Union[str, int]].
        :type batch_id: str.
        :type references: Optional[List[str]].
        :type separator: str.
        :rtype: QueueItem
        """
        if not batch_id:
            batch_id = str(uuid4())
        endpoint = "/odata/Queues/UiPathODataSvc.StartTransaction"
        body = self._format_transaction_body(  # type: ignore
            machine_identifier=machine_identifier,
            content=content,
            batch_id=batch_id,
            refs=references,
            separator=separator,
        )
        data = self.client.post(endpoint, body=body)
        queue_item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            status=data["Status"],
            item_data=data["SpecificContent"],
            reference=data["Reference"],
        )
        return queue_item

    def _process_queue_item_params(self, options: Optional[dict[str, str]] = None):
        filter_params = {"$filter": f"QueueDefinitionId eq {self.id}"}
        mod_filter_params = filter_params.copy()
        if options and ("$filter" in options):
            # if a filter flag is passed we need to modify it to only get
            # the elements of the Queue and delete it afterwards to prevent
            # getting all queue items for all queues (default by API).
            filter_params["$filter"] += f" and {options['$filter']}"
            del options["$filter"]  # type: ignore
            try:
                mod_filter_params = filter_params | options
            except TypeError:
                mod_filter_params = {**filter_params, **options}
        if options and ("$select" in options):
            assert "Id" in options["$select"]
            assert "Reference" in options["$select"]
            try:
                mod_filter_params = filter_params | options
            except TypeError:
                mod_filter_params = {**filter_params, **options}
        return mod_filter_params

    async def _get_items_dataframe(self, options: Optional[dict[str, Any]] = None):
        """Returns an initial dataframe and a list of results with the extra pages"""
        params = self._process_queue_item_params(options=options)
        endpoint = "/odata/QueueItems"
        data = self.client.get(endpoint, params=params)
        initial_df = pd.DataFrame(data["value"])
        count = data["@odata.count"]
        pages = count // self._MAX_ITEMS if count > self._MAX_ITEMS else 0
        offset = 0
        async with httpx.AsyncClient() as client:
            urls = []
            for _ in range(pages):
                try:  # keep for legacy Python
                    new_params = params | {"$skip": self._MAX_ITEMS + offset}
                except TypeError:
                    new_params = {**params, "$skip": self._MAX_ITEMS + offset}
                urls.append(
                    self.client.prepare_url(endpoint, new_params)
                )  # add new url with skip
                offset += self._MAX_ITEMS
            headers = self.client.prepare_headers()
            tasks = (client.get(url, headers=headers) for url in urls)
            resps = await asyncio.gather(*tasks)
        return [json.loads(resp.text) for resp in resps], initial_df

    async def get_async_dataframe(self, days_from: int = 90) -> pd.DataFrame:
        """Retrieves a dataframe of results from the queue with status either New, Abandoned, Retried,
        InProgress, and Successful in the previous days

        :param days_from: the number of days to retrieve the queue items
        :type days_from: int
        :rtype: pd.DataFrame
        """
        then = datetime.datetime.now() - timedelta(days=days_from)
        then_date = then.strftime("%Y-%m-%dT00:00:00Z")
        options = {
            "$filter": f"Status in ('New', 'Abandoned', 'Retried', 'InProgress', 'Successful') and CreationTime gt {then_date}",
            "$select": "Status, Reference, Id, QueueDefinitionId, SpecificContent, CreationTime",
            "$orderby": "CreationTime",
        }
        data, initial_df = await self._get_items_dataframe(options=options)
        for page in data:
            new_pd = pd.DataFrame(page["value"])
            initial_df = pd.concat([initial_df, new_pd], ignore_index=True)
        return initial_df

    async def get_async_new_items(self, days_from: int = 90) -> pd.DataFrame:
        """Retrieves a dataframe of results from the queue with only the QueueItems with status New"""
        then = datetime.datetime.now() - timedelta(days=days_from)
        then_date = then.strftime("%Y-%m-%dT00:00:00Z")
        options = {
            "$filter": f"Status eq 'New' and CreationTime gt {then_date}",
            "$select": "Status, Reference, Id, QueueDefinitionId, SpecificContent, CreationTime",
            "$orderby": "CreationTime",
        }
        data, initial_df = await self._get_items_dataframe(options=options)
        for page in data:
            new_pd = pd.DataFrame(page["value"])
            initial_df = pd.concat([initial_df, new_pd], ignore_index=True)
        return [
            QueueItem(
                qi["Id"],
                self.name,
                self.client,
                qi["Status"],
                qi["SpecificContent"],
                qi["Reference"],
            )
            for qi in initial_df.to_dict("records")
        ]

    def get_item(
        self, id: int, options: Optional[Mapping[str, str]] = None
    ) -> QueueItem:
        """Retrieves a single QueueItem resource given its id.

        :param id: the item id.
        :type id: int
        :param options: and optional dictionary of odata query options.
        :type options: Optional[Mapping[str, str]]
        :rtype: QueueItem
        """
        endpoint = f"/odata/QueueItems({id})"
        data = self.client.get(endpoint, params=options)
        item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            status=data["Status"],
            item_data=data["SpecificContent"],
            reference=data["Reference"],
        )
        return item

    def edit(self, content):
        """Edits a Queue"""
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class Asset(Resource):
    """Class to handle an Asset type Resource"""

    _type = "asset"
    _def_endpoint = "/odata/Assets({id})"

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, name: str, client: Client, asset_data: dict[str, str]):
        super().__init__(id, name, self._type)
        self.client = client
        self.asset_data = asset_data
        self.value = asset_data["Value"]
        self.value_type = asset_data["ValueType"]

    def info(self):
        return self.asset_data

    def key(self):
        return self.asset_data["Key"]

    def refresh(self):
        data = self.client.get(self._def_endpoint.format(id=self.id))
        self.asset_data = data
        self.value = data["Value"]

    def _prepare_edit_body(self, value, name, description):
        formatted_body = self.asset_data.copy()
        formatted_body["Description"] = (
            description if description else formatted_body["Description"]
        )
        if self.value_type == "Credential":
            raise ValueError(
                "Attempted to edit Asset resource with ValueType='Credential'."
            )
        if self.value_type == "Integer":
            assert isinstance(value, int)
            formatted_body["IntValue"] = str(value)
            formatted_body["Value"] = str(value) if value else formatted_body["Value"]
            formatted_body["Name"] = name if name else formatted_body["Name"]
        elif self.value_type == "Bool":
            assert isinstance(value, bool)
            formatted_body["BoolValue"] = str(value)
            formatted_body["Value"] = str(value) if value else formatted_body["Value"]
            formatted_body["Name"] = name if name else formatted_body["Name"]
        elif self.value_type == "Text":
            formatted_body["StringValue"] = value
            formatted_body["Value"] = value if value else formatted_body["Value"]
            formatted_body["Name"] = name if name else formatted_body["Name"]
        else:
            raise Exception("Unrecognized value_type.")
        return formatted_body

    def edit(self, value: Optional[Union[str, int, bool]] = "", name: Optional[str] = None, description: Optional[str] = None):  # type: ignore
        """Edits a Resource of type Asset.

        :param value: optional value (str, int, bool) to edit the Asset.
        :param name: optional name to edit the Asset.
        :param description: optional description to edit the Asset.
        """
        body = self._prepare_edit_body(value=value, name=name, description=description)
        self.client.put(self._def_endpoint.format(id=self.id), body=body)
        self.refresh()

    def delete(self):
        self.client.delete(self._def_endpoint.format(id=self.id))


class Machine(Resource):
    _type = "machine"
    def_endpoint = "/odata/Machines({id})"

    def __init__(
        self, id: int, name: str, client: Client, machine_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.machine_data = machine_data
        self.machine_key = machine_data["Key"]

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.machine_data

    def key(self):
        return self.machine_data["Key"]

    def refresh(self):
        data = self.client.get(self.def_endpoint.format(id=self.id))
        self.machine_data = data
        self.name = data["Name"]
        self.machine_key = data["Key"]

    def edit(self, content):
        """Edits an Machine"""
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class Calendar(Resource):
    """Class to handle a Calendar type resource"""

    _type = "calendar"
    def_endpoint = "/odata/Calendars({id})"

    def __init__(
        self, id: int, name: str, client: Client, calendar_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.calendar_data = calendar_data

    def key(self):
        pass

    def edit(self):
        pass

    def refresh(self):
        new_cal = self.client.get(endpoint=self.def_endpoint.format(id=self.id))
        self.calendar_data = new_cal
        self.name = new_cal["Name"]

    def info(self):
        return self.calendar_data

    def delete(self):
        return self.client.delete(endpoint=self.def_endpoint.format(id=self.id))


class Environment(Resource):
    """Class to handle an Environment type Resource"""

    _type = "environment"
    def_endpoint = "/odata/Environments({id})"

    def __init__(self, id: int, name: str, client: Client, env_data: dict[str, str]):
        super().__init__(id, name, self._type)
        self.client = client
        self.env_data = env_data

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.env_data

    def refresh(self):
        data = self.client.get(endpoint=self.def_endpoint.format(id=self.id))
        self.env_data = data
        self.name = data["Name"]

    def delete(self):
        return self.client.delete(endpoint=self.def_endpoint.format(id=self.id))

    def edit(self):
        pass

    def key(self):
        pass


class CredentialStore(Resource):
    """Class to handle a CredentialStore type Resource"""

    _type = "credential_store"
    def_endpoint = "/odata/CredentialStores({id})"

    def __init__(
        self, id: int, name: str, client: Client, creds_data=Mapping[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.creds_data = creds_data

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.creds_data

    def refresh(self):
        data = self.client.get(endpoint=self.def_endpoint.formar(id=self.id))
        self.creds_data = data
        self.name = data["Name"]

    def key(self):
        pass

    def edit(self):
        pass

    def delete(self):
        return self.client.delete(endpoint=self.def_endpoint.format(id=self.id))


class Bucket(Resource):
    """Class to handle a Bucket type Resource"""

    _type = "bucket"
    def_endpoint = "/odata/Buckets({id})"

    def __init__(
        self, id: int, name: str, client: Client, bucket_data=Mapping[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.bucket_data = bucket_data

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.bucket_data

    def refresh(self):
        data = self.client.get(endpoint=self.def_endpoint.format(id=self.id))
        self.bucket_data = data
        self.name = data["Name"]

    def edit(self):
        pass

    def key(self):
        pass

    def get_directories(self, directory_path: Optional[str] = None):
        endpoint = f"/odata/Buckets({self.id})/UiPath.Server.Configuration.OData.GetDirectories"
        return self.client.get(endpoint, params={"directory": directory_path})

    def get_file(self, path: str):
        endpoint = (
            f"/odata/Buckets({self.id})/UiPath.Server.Configuration.OData.GetFile"
        )
        return self.client.get(endpoint, params={"path": path})

    def get_files(self, directory_path: Optional[str] = None):
        endpoint = (
            f"/odata/Buckets({self.id})/UiPath.Server.Configuration.OData.GetFiles"
        )
        return self.client.get(endpoint, params={"directory": directory_path})

    def get_read_uri(self, path: str):
        endpoint = (
            f"/odata/Buckets({self.id})/UiPath.Server.Configuration.OData.GetReadUri"
        )
        return self.client.get(endpoint, params={"path": path})

    def get_write_uri(self, path: str):
        endpoint = (
            f"/odata/Buckets({self.id})/UiPath.Server.Configuration.OData.GetWriteUri"
        )
        return self.client.get(endpoint, params={"path": path})

    def delete(self):
        return self.client.delete(endpoint=self.def_endpoint.format(id=self.id))

    def delete_file(self, path: str):
        endpoint = (
            f"/odata/Buckets({self.id})/UiPath.Server.Configuration.OData.DeleteFile"
        )
        return self.client.delete(endpoint, params={"path": path})


class Job(Resource):
    """Class to handle a Job type Resource"""

    _type = "job"
    def_endpoint = "/odata/Jobs({id})"

    def __init__(self, id: int, name: str, client: Client, job_data: Mapping[str, Any]):
        super().__init__(id, name, self._type)
        self.client = client
        self.job_data = job_data

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.job_data

    def refresh(self):
        data = self.client.get(endpoint=self.def_endpoint.format(id=self.id))
        self.job_data = data

    def key(self):
        pass

    def stop(self):
        """Stops the current job"""
        endpoint = "/odata/Jobs({self.id})/UiPath.Server.Configuration.OData.StopJob"
        return self.client.post(endpoint)

    def validate(self):
        """Validates the current job"""
        endpoint = "/odata/Jobs({self.id})/UiPath.Server.Configuration.OData.ValidateExistingJob"
        return self.client.post(endpoint)

    def restart(self):
        """Restarts the current Job"""
        endpoint = "/odata/Jobs/UiPath.Server.Configuration.OData.RestartJob"
        return self.client.post(endpoint, body={"jobId": self.id})

    def resume(self):
        endpoint = "/odata/Jobs/UiPath.Server.Configuration.OData.ResumeJob"
        return self.client.post(endpoint, body={"jobId": self.id})

    def edit(self):
        pass

    def delete(self):
        pass


class Folder(Resource):
    """Class to handle a Folder type Resource"""

    _type = "folder"
    def_endpoint = "/odata/Folders({id})"

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, name: str, client: Client, folder_data: dict[str, str]):
        super().__init__(id, name, self._type)
        self.client = client
        self.folder_data = folder_data

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.folder_data

    def key(self):
        return self.folder_data["Key"]

    def refresh(self):
        data = self.client.get(self.def_endpoint.format(id=self.id))
        self.folder_data = data
        self.name = data["DisplayName"]

    def get_queues(
        self, options: Optional[Mapping[str, Any]] = None, item_pool: bool = False
    ):
        endpoint = "/odata/QueueDefinitions"
        data = self.client.get(endpoint, params=options)
        return [
            Queue(q["Id"], q["Name"], q, self.client, item_pool) for q in data["value"]
        ]

    def get_queue(
        self,
        id: int,
        options: Optional[Mapping[str, Any]] = None,
        item_pool: bool = True,
    ) -> Queue:
        """Retreives a Queue resource based on its id.

        :param id: the queue id
        :param options: an optional dicitonary of odata query options.
        :type id: int
        :type options: Optional[Mapping[str, Any]
        :rtype: Queue
        """
        data = self.client.get(f"/odata/QueueDefinitions({id})", params=options)
        return Queue(
            id=data["Id"],
            name=data["Name"],
            queue_data=data,
            client=self.client,
            item_pool=item_pool,
        )

    def get_assets(self, options: Optional[Mapping[str, Any]] = None):
        endpoint = "/odata/Assets"
        data = self.client.get(endpoint, params=options)
        return [Asset(a["Id"], a["Name"], self.client, a) for a in data["value"]]

    def get_asset(self, id: int, options: Optional[Mapping[str, Any]] = None) -> Asset:
        """Retrives an Asset resource based on its id.

        :param id: the asset id
        :param options: an optional dictionary of odata query options.
        :rtype: Asset
        :type id: int
        :type options: Optional[Mapping[str, Any]
        """
        data = self.client.get(f"/odata/Assets({id})", params=options)
        return Asset(
            id=data["Id"], name=data["Name"], client=self.client, asset_data=data
        )

    def get_environment(self, environment_id: int) -> Environment:
        """Retrieves an Environment based on its id

        :param environment_id: the id of the environment to select
        :type environment_id: int
        :rtype: Environment
        """
        endpoint = f"/odata/Environments({environment_id})"
        data = self.client.get(endpoint)
        return Environment(data["Id"], data["Name"], self.client, data)

    def get_environments(
        self, options: Optional[Mapping[str, Any]] = None
    ) -> List[Environment]:
        """Retrieves a list of Environments associated to the current folder

        :param options: an optional dictionary of odata query options
        :type options: Optional[Mapping[str, Any]]
        :rtype: List[Environment]
        """
        endpoint = "/odata/Environments"
        data = self.client.get(endpoint, params=options)
        return [Environment(e["Id"], e["Name"], self.client, e) for e in data["value"]]

    def get_buckets(self, options: Optional[Mapping[str, Any]] = None) -> List[Bucket]:
        """Retrieves a list of all Buckets associated to the current folder

        :param options: an optional dictionary of odata query options
        :type options: Optional[Mapping[str, Any]]
        :rtype: List[Bucket]
        """
        endpoint = "/odata/Buckets"
        data = self.client.get(endpoint, params=options)
        return [Bucket(b["Id"], b["Name"], self.client, b) for b in data["value"]]

    def get_bucket(self, bucket_id: int) -> Bucket:
        """Retrieves a single bucket based on its id

        :param bucket_id: the id of the bucket to select
        :rtype: Bucket
        """
        endpoint = f"/odata/Buckets({bucket_id})"
        data = self.client.get(endpoint)
        return Bucket(data["Id"], data["Name"], self.client, data)

    def get_logs(self, options: Optional[Mapping[str, Any]] = None):
        """Retrieves the logs"""
        endpoint = "/odata/RobotLogs"
        data = self.client.get(endpoint, options)
        return data

    def get_jobs(self, options: Optional[Mapping[str, Any]] = None) -> List[Job]:
        """Retrieves a list of Jobs associated to that folder

        :param options: dictionary of odata query options
        :type options: Optional[Mapping, str, Any]
        :rtype: List[Job]
        """
        endpoint = "/odata/Jobs"
        data = self.client.get(endpoint, options)
        return [Job(j["Id"], j["Name"], self.client, j) for j in data["value"]]

    def get_job(self, job_id: int) -> Job:
        """Retrieves a single Job

        :param job_id: the id of the job
        :type job_id: int
        :rtype: Job
        """
        endpoint = f"/odata/Jobs({job_id})"
        data = self.client.get(endpoint)
        return Job(data["Id"], data["Name"], self.client, data)

    def get_processes(
        self, options: Optional[Mapping[str, str]] = None
    ) -> List[Process]:
        """Returns a list of Process resources.

        :param options: an optional dictionary of odata query options
        :type options: dict[str, str]
        :rtype: List[Process]
        """
        endpoint = "/odata/Processes"
        data = self.client.get(endpoint, options)
        if not data["value"]:
            raise ValueError("No processes were found")
        try:
            return [
                Process(
                    id=val["Key"],
                    name=val["Title"],
                    client=self.client,
                    process_data=val,
                )
                for val in data["value"]
            ]
        except KeyError as err:
            msg = "Cannot get process without 'Key' and 'Title'. Please do not include either fields in the '$select' parameter."
            raise ValueError(msg) from err

    def get_schedules(
        self, options: Optional[Mapping[str, Any]] = None
    ) -> List[Schedule]:
        """Retrieves a list of Process Schedules

        :param options: dictionary of odata query options
        :type options: Optional[Mapping[str, Any]]
        :rtype: List[Schedule]
        """
        endpoint = "/odata/ProcessSchedules"
        data = self.client.get(endpoint, options)
        if not data["value"]:
            raise ValueError("No processes were found")
        schedules = [
            Schedule(
                id=sch["Id"], name=sch["Name"], client=self.client, schedule_data=sch
            )
            for sch in data["value"]
        ]
        return schedules

    def get_schedule(
        self, id: Optional[int] = None, name: Optional[str] = None
    ) -> Schedule:
        """Retrieves a single ProcessSchedule

        :param id: the schedule id
        :param name: the schedule name
        :type id: Optional[int]
        :type name: Optional[str]
        :rtype: Schedule
        """
        if id:
            return self._get_schedule_by_id(id)
        if name:
            return self._get_schedule_by_name(name)
        raise ValueError("At least one of 'id' or 'name' must not be 'None")

    def _get_schedule_by_name(self, name: str) -> Schedule:
        schedules = self.get_schedules(options={"$filter": f"Name eq '{name}'"})
        return schedules[0]  # return the first match

    def _get_schedule_by_id(self, id: int) -> Schedule:
        endpoint = f"/odata/ProcessSchedules({id})"
        data = self.client.get(endpoint)
        return Schedule(
            id=data["Id"], name=data["Name"], client=self.client, schedule_data=data
        )

    def get_release_ids(self) -> Dict[str, int]:
        r"""Retrieves a dictionary where the keys correspond to the release names (i.e) without the version,
        and the values are the ids of those releases, so they can be used to access a single Release

        :rtype: Dict[str, int]
        """
        endpoint = "/odata/Releases"
        data = self.client.get(endpoint)
        ids = {}
        for release in data["value"]:
            ids.update({release["Name"]: release["Id"]})
        return ids

    def get_release(self, release_id: int) -> Release:
        """Gets a single release based on its release id

        :param release_id: the id of the release to be queried
        :type release_id: int
        :rtype: Release
        """
        endpoint = f"/odata/Releases({release_id})"
        data = self.client.get(endpoint)
        return Release(
            id=data["Id"], name=data["Name"], client=self.client, release_data=data
        )

    def get_releases(
        self, options: Optional[Mapping[str, str]] = None
    ) -> List[Release]:
        """Retries a list of releases

        :param options: an optional fictionary of odata query options
        :type options: Optional[Mapping[str, str]]
        :rtype: List[Release]
        """
        endpoint = "/odata/Releases"
        data = self.client.get(endpoint, options)
        return [
            Release(
                id=release["Id"],
                name=release["Name"],
                client=self.client,
                release_data=release,
            )
            for release in data["value"]
        ]

    def upload_package(self, nuget_file: str):
        """Uploads a .nuget file to the Orchestrator tenant

        :param nuget_file: the location of the .nupkg file containing the process to be uploaded to your Orchestrator tenant

        """
        endpoint = "/odata/Processes/UiPath.Server.Configuration.OData.UploadPackage"
        files = {
            "file": (nuget_file, open(nuget_file, "rb")),
        }
        data = self.client.post(endpoint=endpoint, files=files)
        return data

    def _create_body(self, name, value, value_type, description):
        attr_value = value_type
        if value_type == "Text":
            attr_value = "String"
        elif value_type == "Integer":
            attr_value = "Int"
        body = {
            "Name": name,
            "ValueScope": "Global",
            "ValueType": value_type,
            f"{attr_value}Value": value,
            "Description": description,
        }
        return body

    def create_asset(
        self,
        name: str,
        value: Union[str, bool, int],
        value_type: Literal["Text", "Integer", "Bool"],
        description: str = "",
    ) -> Asset:
        """Creates a Resource of type Asset

        :param name: the name of the Asset.
        :param value: the value of the Asset.
        :param value_type: the value type of the Asset ('Test', 'Integer', 'Bool').
        :param description: an optional description of the Asset.
        :rtype: Asset
        :type name: str
        :type value: Union[str, bool, int]
        :type value_type: str
        :type description: str
        """
        assert value_type in ("Text", "Integer", "Bool")
        body = self._create_body(name, value, value_type, description)
        data = self.client.post(endpoint="/odata/Assets", body=body)
        asset = Asset(
            id=data["Id"], name=data["Name"], client=self.client, asset_data=data
        )
        return asset

    def edit(self, content):
        """Edits an Folder"""
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


def raise_no_client(f):
    """Raises a ValueError if the credentials flow has not been
    initialized first to prevent user from calling other methods first."""

    def wrapper(self, *args, **kwargs):
        if self.client is None:
            raise ValueError("You need to authenticate yourself first!")
        return f(self, *args, **kwargs)

    return wrapper


class Schedule(Resource):
    """Class to interact with a Schedule type Resource"""

    _def_endpoint = f"/odata/ProcessSchedules('{id}')"
    _type = "process_schedule"

    def __init__(
        self, id: int, name: str, client: Client, schedule_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.schedule_data = schedule_data

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.schedule_data

    def key(self) -> str:
        return self.schedule_data["Key"]

    def refresh(self) -> None:
        endpoint = self._def_endpoint.format(id=self.id)
        self.schedule_data = self.client.get(endpoint)

    def get_cron(self) -> str:
        cron_summary = (
            self.schedule_data["StartProcessCronSummary"]
            if self.schedule_data["StartProcessCronSummary"]
            # else get_description(self.schedule_data["StartProcessCron"])
            else self.schedule_data["StartProcessCron"]
        )
        return cron_summary

    def edit(self):
        pass

    def delete(self):
        pass


class Process(Resource):
    """Class to handle a Process type Resource"""

    _type = "process"
    def_endpoint = "/odata/Processes({id})"

    # pylint: disable=redefined-builtin
    def __init__(
        self, id: str, name: str, client: Client, process_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.process_data = process_data
        self.process_id = id.split(":")[0]

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.process_data

    def key(self):
        return self.process_data["Key"]

    def refresh(self):
        raise NotImplementedError

    def download_package(self, dir_name: str):
        """Downloads a .nupkg containing the process in the specified route

        :param dir_name: string representing the directory name to download the package into
        :rtype dir_name: str
        """
        endpoint = f"/odata/Processes/UiPath.Server.Configuration.OData.DownloadPackage(key='{self.id}')"
        data = self.client.get(endpoint)
        with open(os.path.join(dir_name, f"{self.id}.nupkg"), "wb") as f:
            f.write(data)
        # return data

    def get_available_versions(self):
        """Retries all the available versions of the process"""
        endpoint = f"/odata/Processes/UiPath.Server.Configuration.OData.GetProcessVersions(processId='{self.process_id}')"
        data = self.client.get(endpoint)
        return data

    def get_arguments(self) -> Mapping[str, Any]:
        """Retrieves the input and ouput arguments of a process and returns their names and types"""
        endpoint = f"/odata/Processes/UiPath.Server.Configuration.ODATA.GetArguments(key = '{self.id}')"
        data = self.client.get(endpoint)
        parsed_arguments = self._parse_arguments(args=data)
        return parsed_arguments

    def _parse_arguments(self, args: Mapping[str, Any]) -> Mapping[str, Any]:
        input_args = json.loads(args["Input"]) if args["Input"] else None
        output_args = json.loads(args["Output"]) if args["Output"] else None
        fmt_input_args = []
        fmt_output_args = []
        if input_args:
            for arg in input_args:
                fmt_input_args.append(
                    {"name": arg["name"], "type": arg["type"].split(",")[0]}
                )
        if output_args:
            for arg in output_args:
                fmt_output_args.append(
                    {"name": arg["name"], "type": arg["type"].split(",")[0]}
                )
        return {"input_args": fmt_input_args, "output_args": fmt_output_args}

    def edit(self):
        pass

    def delete(self):
        pass


class Release(Resource):
    """Class to handle a Release type Resource"""

    _def_endpoint = f"/odata/Releases/({id})"
    _type = "process"

    # pylint: disable=redefined-builtin
    def __init__(
        self, id: int, name: str, client: Client, release_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.release_data = release_data

    def __hash__(self):
        return hash(self.id)

    def update_to_latest_version(self):
        endpoint = f"​/odata​/Releases({self.id})​/UiPath.Server.Configuration.OData.UpdateToLatestPackageVersion"
        data = self.client.post(endpoint=endpoint, body={"mergePackageTags": True})
        return data

    def rollback(self):
        endpoint = f"/odata/Releases({self.id})/UiPath.Server.Configuration.OData.RollbackToPreviousReleaseVersion"
        data = self.client.post(endpoint=endpoint)
        return data

    def update(self, version: str):
        """Updates the process to the given version

        :param version: string with a version for the process (e.g. 1.8.9)
        :type version: str
        """
        endpoint = f"/odata/Releases({self.id})/UiPath.Server.Configuration.OData.UpdateToSpecificPackageVersion"
        data = self.client.post(endpoint=endpoint, body={"packageVersion": version})
        return data

    def info(self):
        return self.release_data

    def key(self):
        return self.release_data["Key"]

    def refresh(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass


class Orchestrator:
    """Creates an Orchestrator object.
    If no parameters are passed, it forces authentication via one of the credential methods.
    Otherwise, you need to provide together with the `auth` parameter, the necessary keyword
    arguments to authentication depending on the value of `auth` you provided.
    Check the documentation for the different types of authentication flows (`CloudFlow`
    and `CustomFlow`)
    Optional parameters:

    :param auth: authentication type ('cloud', 'on-premise')
    :type auth: Literal['cloud', 'on-premise']
    :param client_id: client id for oauth authentication type.
    :type client_id: str
    :param refresh_token: refresh token for cloud authentication type.
    :type refresh_token: str
    :param tenant_name: orchestrator tenant name
    :type tenant_name: str
    :param organization: your organization name
    :type organization: str
    :param username: username for on-premise authentication type
    :type username: str
    :param password: password for on-premise authentication type
    :type password: str
    :param orchestrator_url: orchestrator url for custom or premise authentication type
    :type orchestrator_url: str
    """

    client: Client = None  # type: ignore

    def __init__(self, auth=None, **kwargs):
        if not kwargs:
            return
        self.client = Client(auth, **kwargs)

    def from_oauth_credentials(
        self, tenant_name: str, client_id: str, refresh_token: str, organization: str
    ) -> Orchestrator:
        """Authenticates a client using default cloud base_url

        :param tenant_name: orchestrator tenant name.
        :param client_id: client id for oauth authentication type.
        :param refresh_token: refresh token for cloud authentication type.
        :param organization: your organization name.
        """
        if self.client:
            return self
        self.client = Client(
            auth="cloud",
            tenant_name=tenant_name,
            client_id=client_id,
            refresh_token=refresh_token,
            organization=organization,
        )
        return self

    def from_on_premise_credentials(
        self, tenant_name: str, username: str, password: str, orchestrator_url: str
    ) -> Orchestrator:
        """Authenticates a client using on-premise credentials

        :param tenant_name: the tenant name used in your organization
        :type tenant_name: str
        :param username: the username of the account
        :type username: str
        :param password: the password to authenticate
        :type password: str
        :param orchestrator_url: the custom url to host your on premise orchestrator
        :type orchestrator_url: str
        """
        if self.client:
            return self
        self.client = Client(
            auth="on-premise",
            tenant_name=tenant_name,
            username=username,
            password=password,
            orchestrator_url=orchestrator_url,
        )
        return self

    @raise_no_client
    def get_folders(self, options: Optional[Mapping[str, str]] = None) -> List[Folder]:
        """Returns a set of Folders resources

        :param options: an optional dictionary of odata query options:
        :type options: Optional[Mapping[str, Any]]
        :rtpye: List[Folder]
        """
        if self.client is None:
            raise ValueError("You need to authenticate yourself first!")
        endpoint = "/odata/Folders"
        data = self.client.get(endpoint, options)
        try:
            return [
                Folder(
                    id=folder["Id"],
                    name=folder["DisplayName"],
                    folder_data=folder,
                    client=self.client,
                )
                for folder in data["value"]
            ]
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either field in the '$select' parameter."
            raise ValueError(msg) from err

    @raise_no_client
    def get_folder(
        self, id: int, options: Optional[Mapping[str, Any]] = None
    ) -> Folder:
        """Returns a Folder resource based on its id

        :param id: the folder id.
        :param options: optional dictionary of odata query options.
        :type options: Optional[Mapping[str, Any]]
        :rtype: Folder
        """
        # pylint: disable=redefined-builtin
        endpoint = f"/odata/Folders({id})"
        data = self.client.get(endpoint, options)
        self.client.folder_id = id
        pprint(data)
        try:
            return Folder(
                id=data["Id"],
                name=data["DisplayName"],
                folder_data=data,
                client=self.client,
            )
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either field in the '$select' parameter."
            raise ValueError(msg) from err
        except TypeError as err:
            msg = "Cannot get folder. Please review your credentials"
            raise ValueError(msg) from err

    def get_machine(
        self, machine_key: str, options: Optional[Mapping[str, str]] = None
    ) -> Machine:
        """Returns a Machine resource based on its key

        :param machine_key: the key of the machine
        :param options: optional dictionary of odata query options
        :rtype: Machine
        """
        endpoint = f"/odata/Machines({machine_key})"
        data = self.client.get(endpoint, options)
        try:
            return Machine(
                id=data["Id"], name=data["Name"], client=self.client, machine_data=data
            )
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either fields in the '$select' parameter."
            raise ValueError(msg) from err

    def get_machines(
        self, options: Optional[Mapping[str, Any]] = None
    ) -> List[Machine]:
        """Returns a list of Machine resources

        :param options: optional dictionary of odata query options
        :type options: Optional[Mapping[str, Any]]
        :rtype: List[Machines]
        """

        endpoint = "/odata/Machines"
        data = self.client.get(endpoint, options)
        try:
            return [
                Machine(
                    id=val["Id"], name=val["Name"], client=self.client, machine_data=val
                )
                for val in data["value"]
            ]
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either fields in the '$select' parameter."
            raise ValueError(msg) from err

    def get_alerts(
        self, days: Optional[int] = 1, options: Optional[Mapping[str, Any]] = None
    ):
        """Retrieves a list of Alerts

        :param options: optional dictionary of odata query options
        :param days: number of prior days to retrieve the alerts from
        :type days: int
        :type options: Optional[Mapping[str, Any]]
        """
        endpoint = "/odata/Alerts"
        if days:
            dt_days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
            str_dt = dt_days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
            options = {"$filter": f"CreationTime gt {str_dt}"}
        return self.client.get(endpoint, params=options)

    def get_alert_unread_count(self) -> int:
        """Retrieves the total count of unread alerts

        :rtype: int
        """
        endpoint = "/odata/Alerts/UiPath.Server.Configuration.OData.GetUnreadCount"
        return self.client.get(endpoint)["value"]

    def get_calendar(self, calendar_id: int) -> Calendar:
        """Retrieves a single Calendar based on its id

        :param calendar_id: the id of the calendar
        :type calendar_id: int
        :rtype: Calendar
        """
        endpoint = f"/odata/Calendars({calendar_id})"
        data = self.client.get(endpoint)
        return Calendar(data["Id"], data["Name"], self.client, data)

    def get_calendars(
        self, options: Optional[Mapping[str, Any]] = None
    ) -> List[Calendar]:
        """Retrieves a list of Calendars

        :param options: optional dictionary of odata query options
        :type options: Optional[Mapping[str, Any]]
        :rtype: List[Calendar]
        """
        endpoint = "/odata/Calendars"
        data = self.client.get(endpoint, params=options)
        return [Calendar(c["Id"], c["Name"], self.client, c) for c in data["value"]]
