from sporestack import api_client


def test__is_onion_url() -> None:
    onion_url = "http://spore64i5sofqlfz5gq2ju4msgzojjwifls7"
    onion_url += "rok2cti624zyq3fcelad.onion/v2/"
    assert api_client._is_onion_url(onion_url) is True
    # This is a good, unusual test.
    onion_url = "https://www.facebookcorewwwi.onion/"
    assert api_client._is_onion_url(onion_url) is True
    assert api_client._is_onion_url("http://domain.com") is False
    assert api_client._is_onion_url("domain.com") is False
    assert api_client._is_onion_url("http://onion.domain.com/.onion/") is False
    assert api_client._is_onion_url("http://me.me/file.onion/") is False
    assert api_client._is_onion_url("http://me.me/file.onion") is False
