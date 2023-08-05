import logging
import json

def test_getmempoolinfo(caplog, client):
    caplog.set_level(logging.INFO)
    caplog.set_level(logging.DEBUG, logger="cryptoadvance.spectrum")
    result = client.post("/", json={"method": "getaddressinfo"})
    assert result.status_code == 200
    print(json.loads(result.data))
    assert json.loads(result.data)["result"]["loaded"]