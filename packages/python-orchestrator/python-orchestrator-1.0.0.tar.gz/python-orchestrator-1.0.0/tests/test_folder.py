from orchestrator import Orchestrator
import pytest
from pprint import pprint
import os
from uuid import uuid1, uuid4
import pandas as pd

if not os.getenv("CI"):
    from dotenv import load_dotenv

    load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
MACHINE_IDENTIFIER = os.getenv("MACHINE_IDENTIFIER")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
TENANT_NAME = os.getenv("TENANT_NAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def test_assets(init_premise):
    folder = init_premise.get_folder(13)
    assets = folder.get_assets()
    assert assets
    assets_options = folder.get_assets(
        options={"$filter": "Name eq 'Global_OrchestratorEndpoint'"}
    )
    assert assets_options[0]
    assets_options[0].refresh()
    assets_options[0].info()
    assert assets_options[0].value
    assert assets_options[0].value_type == "Text"


def test_queues():
    init_premise = Orchestrator().from_on_premise_credentials(
        tenant_name="",
        username=USERNAME,
        password=PASSWORD,
        orchestrator_url="https://orchestrator.jt-rpa.com",
    )
    folder = init_premise.get_folder(13)
    queues = folder.get_queues()
    assert queues
    queue_options = folder.get_queues(options={"$filter": "Id eq 149"})
    assert queue_options
    queue = folder.get_queue(149)
    queue.refresh()
    assert queue == queue_options[0]


def test_bulk_add():
    init_premise = Orchestrator().from_on_premise_credentials(
        tenant_name="",
        username=USERNAME,
        password=PASSWORD,
        orchestrator_url="https://orchestrator.jt-rpa.com",
    )
    folder = init_premise.get_folder(13)
    queue = folder.get_queue(84)
    df = pd.DataFrame(
        {
            "header1": [str(uuid1())] * 200,
            "header2": [str(uuid1())] * 200,
            "header3": [str(uuid4())] * 200,
        }
    )
    queue.bulk_add(df=df, references=["header2"])


def test_queue_duplicate():
    init_premise = Orchestrator().from_on_premise_credentials(
        tenant_name="",
        username=USERNAME,
        password=PASSWORD,
        orchestrator_url="https://orchestrator.jt-rpa.com",
    )
    folder = init_premise.get_folder(13)
    queue = folder.get_queue(84)
    print(queue.dataframe.columns)
    item = queue.check_duplicate(values=["0e7134f8-b76b-11ed-8075-36dbcb61d693"])
    print(item)


def test_filter_dataframe():
    init_premise = Orchestrator().from_on_premise_credentials(
        tenant_name="",
        username=USERNAME,
        password=PASSWORD,
        orchestrator_url="https://orchestrator.jt-rpa.com",
    )
    folder = init_premise.get_folder(13)
    queue = folder.get_queue(84)
    df = pd.DataFrame(
        {
            "header1": ["0e7134f8-b76b-11ed-8075-36dbcb61d693#4d16d0af", str(uuid1())],
            "header2": [str(uuid1()), str(uuid1())],
            "header3": [str(uuid4()), str(uuid4())],
        }
    )
    new_df = queue._filter_dataframe(df, ["header1"])
    queue.bulk_add(new_df, references=["header2"])


def test_get_new_item():
    init_premise = Orchestrator().from_on_premise_credentials(
        tenant_name="",
        username=USERNAME,
        password=PASSWORD,
        orchestrator_url="https://orchestrator.jt-rpa.com",
    )
    folder = init_premise.get_folder(13)
    queue = folder.get_queue(84)
    print(len(queue.new_items))
    new_item = queue.start_item(machine_identifier=MACHINE_IDENTIFIER)
    print(new_item.reference)
    print(new_item)
    print(len(queue.new_items))


test_get_new_item()


@pytest.mark.skip(reason="Not Implemented")
def test_asset_creation(init_premise):
    """Creates Assets of different kinds, edits them and deletes them"""
    folder = init_premise.get_folder(13)
    # creates a string asset
    asset_string = folder.create_asset(
        name="Test_Asset_Create_Delete",
        value_type="Text",
        value="This is a temporary asset",
    )
    # creates a boolean asset
    asset_bool = folder.create_asset(
        name="Test_Asset_Create_Bool_Delete", value_type="Bool", value=True
    )
    # creates an integer asset
    asset_int = folder.create_asset(
        name="Test_Asset_Create_Int_Delete", value_type="Integer", value=25000
    )
    # edit the asset
    assert not asset_string.asset_data["Description"]
    asset_string.edit(description="Some description")
    asset_bool.edit(value=False)
    assert asset_bool.value == "False"
    asset_int.edit(value=25, description="Some other description")
    assert asset_int.value == "25"
    # delet the assets
    asset_int.delete()
    asset_bool.delete()
    asset_string.delete()
