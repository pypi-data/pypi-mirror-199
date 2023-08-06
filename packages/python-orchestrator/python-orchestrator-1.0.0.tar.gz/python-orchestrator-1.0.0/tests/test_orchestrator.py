from orchestrator import Orchestrator
import pytest
from pprint import pprint
import os

if not os.getenv("CI"):
    from dotenv import load_dotenv

    load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
MACHINE_IDENTIFIER = os.getenv("MACHINE_IDENTIFIER")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
TENANT_NAME = os.getenv("TENANT_NAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def test_get_folder_cloud(init_orch, init_premise):
    folder = init_orch.get_folder(1263510)
    assert folder.id == 1263510
    assert folder.name == "Pre-produccion"
    assert folder._type == "folder"
    assert folder.client
    assert folder.client.folder_id == 1263510
    assert folder.folder_data
    key = folder.key()
    folder.refresh()
    new_key = folder.key()
    folder_data = folder.info()
    assert folder_data == folder.folder_data
    assert key == new_key
    options = {
        "$filter": "DisplayName eq 'Pre-produccion'",
    }
    folders = init_orch.get_folders(options)
    assert len(folders) == 1
    assert folders[0].name == "Pre-produccion"
    assert folders[0] == folder
    assert folders[0].folder_data != folder.folder_data

    # test on_premise

    folder = init_premise.get_folder(13)
    assert folder.id == 13
    assert folder.name == "Pre-produccion"
    assert folder._type == "folder"
    assert folder.client
    assert folder.client.folder_id == 13
    assert folder.folder_data
    key = folder.key()
    folder.refresh()
    new_key = folder.key()
    folder_data = folder.info()
    assert folder_data == folder.folder_data
    assert key == new_key
    options = {
        "$filter": "DisplayName eq 'Pre-produccion'",
    }
    folders = init_premise.get_folders(options)
    assert len(folders) == 1
    assert folders[0].name == "Pre-produccion"
    assert folders[0] == folder
    assert folders[0].folder_data != folder.folder_data


@pytest.mark.xfail(raises=ValueError)
def test_get_folder_options(init_orch):
    """Test raises Value error when selecting only DisplayName and not Id"""
    options = {"$select": "DisplayName"}
    init_orch.get_folder(1263510, options)


@pytest.mark.xfail(raises=ValueError)
def test_init_no_client_raises():
    """tests the @raise_no_client decorator"""
    orch = Orchestrator()
    orch.get_folder(id=1232123)


@pytest.mark.xfail(raises=ValueError)
def test_auto_init_missing_param():
    """Tests the Orchestrator __init__ method when a parameter is missing"""
    orch = Orchestrator(
        auth="cloud",
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        tenant_name=TENANT_NAME,
    )
    orch.get_folder(1263510)


@pytest.mark.xfail(raises=ValueError)
def test_auto_init_missing_param_prem():
    """Tests the Orchestrator __init__ method when a parameter is missing"""
    orch = Orchestrator(
        auth="on-premise",
        tenant_name="",
        username=USERNAME,
    )
    orch.get_folder(1263510)


@pytest.mark.xfail(raises=ValueError)
def test_wrong_auth_xfail():
    """Tests wrong 'auth' argument."""
    Orchestrator(
        auth="asdfgs",
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        tenant_name=TENANT_NAME,
        organization="JTBOT",
    )


@pytest.mark.xfail(raises=ValueError)
def test_wrong_params():
    """Tests ValueError thrown if wrong 'tenant_name' and/or 'organization'"""
    orch = Orchestrator(
        auth="cloud",
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        tenant_name="TENANT_NAME",
        organization="JTBOT",
    )
    orch.get_folders()


def test_machines():
    """Tests Machines and various methods"""
    init_premise = Orchestrator().from_on_premise_credentials(
        tenant_name="",
        username=USERNAME,
        password=PASSWORD,
        orchestrator_url="https://orchestrator.jt-rpa.com",
    )
    machines = init_premise.get_machines()
    machine = machines[0]
    single_machine = init_premise.get_machine(machine_key=machine.id)
    assert machine == single_machine
    machine.refresh()
    machine.info()
    machine.key()
    machines = init_premise.get_machines(options={"$filter": "Id eq 117353"})


def test_alerts(init_premise):
    """Tests Alerts and various methods"""
    alerts = init_premise.get_alerts(days=1)
    assert alerts
    init_premise.get_alert_unread_count()


def test_calendars(init_premise):
    """Tests Calendars and various methods"""
    init_premise.get_calendars()
