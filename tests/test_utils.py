#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webdriver_manager import utils
from unittest import mock
import pytest
import json


def test_validate_response_json_decode_error():
    resp = mock.Mock()
    resp.headers = {}
    resp.request.url = "http://example.com"
    resp.content = "content"
    resp.json = mock.Mock(side_effect=json.decoder.JSONDecodeError("", "", 0))
    with pytest.raises(ValueError) as excinfo:
        utils.validate_response(resp)
    assert str(excinfo.value) == "\n".join(
        [
            "response body:",
            "content",
            "request url:",
            "http://example.com",
            "response headers:",
            "{}",
            ""
        ]
    )
