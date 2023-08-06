from polly import workspaces
import pytest
import os
from polly.errors import (
    InvalidParameterException,
    UnauthorizedException,
    InvalidPathException,
)

key = "POLLY_REFRESH_TOKEN"
token = os.getenv(key)


def test_obj_initialised():
    assert workspaces.Workspaces(token) is not None


def test_fetch_my_workspaces():
    obj = workspaces.Workspaces(token)
    assert dict(obj.fetch_my_workspaces()) is not None


def test_create_copy_incorrect_token():
    incorrect_token = "incorrect_token"
    with pytest.raises(UnauthorizedException, match=r"Expired or Invalid Token"):
        workspaces.Workspaces(incorrect_token)


def test_create_copy():
    obj = workspaces.Workspaces(token)
    invalid_source_id = "12"
    valid_source_id = 12
    invalid_source_path = ["source_path"]
    valid_source_path = "source_path"
    valid_destination_id = 13
    invalid_destination_id = "13"
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.create_copy(invalid_source_id, valid_source_path, valid_destination_id)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.create_copy(valid_source_id, invalid_source_path, valid_destination_id)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.create_copy(valid_source_id, valid_source_path, invalid_destination_id)


def test_upload_to_workspaces_incorrect_path():
    workspace_id = 12
    workspace_path = "workspace_path"
    local_path = "local_path"
    obj = workspaces.Workspaces(token)
    with pytest.raises(
        InvalidPathException, match=r"does not represent a file or a directory"
    ):
        obj.upload_to_workspaces(workspace_id, workspace_path, local_path)


def test_upload_to_workspaces():
    obj = workspaces.Workspaces(token)
    invalid_workspace_id = "12"
    valid_workspace_id = 12
    invalid_workspace_path = ["workspace_path"]
    valid_workspace_path = "workspace_path"
    invalid_local_path = ["local_path"]
    valid_local_path = "local_path"
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.upload_to_workspaces(
            invalid_workspace_id, valid_workspace_path, valid_local_path
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.upload_to_workspaces(
            valid_workspace_id, invalid_workspace_path, valid_local_path
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.upload_to_workspaces(
            valid_workspace_id, valid_workspace_path, invalid_local_path
        )


def test_download_from_workspaces_incorrect_token():
    incorrect_token = "incorrect_token"
    with pytest.raises(UnauthorizedException, match=r"Expired or Invalid Token"):
        workspaces.Workspaces(incorrect_token)


def test_download_from_workspaces():
    obj = workspaces.Workspaces(token)
    invalid_workspace_id = "12"
    valid_workspace_id = 12
    invalid_workspace_path = ["workspace_path"]
    valid_workspace_path = "workspace_path"
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.download_from_workspaces(invalid_workspace_id, valid_workspace_path)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.download_from_workspaces(valid_workspace_id, invalid_workspace_path)
