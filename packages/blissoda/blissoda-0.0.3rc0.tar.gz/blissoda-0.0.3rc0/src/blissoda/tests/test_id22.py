import os
import pytest
from unittest import mock
from ..id22.stscan_processor import StScanProcessor

_FILENAME = os.path.abspath(
    "/data/visitor/id000000/id00/20230227/raw/Blank/Blank_0001/Blank_0001.h5"
)
_PROCESSED_DIR = os.path.abspath("/data/visitor/id000000/id00/20230227/processed")


@pytest.fixture
def current_session_mock(mock_persistent, mocker):
    m = mocker.patch("blissoda.persistent.current_session")
    m = mocker.patch("blissoda.id22.stscan_processor.current_session")
    m.scan_saving.proposal_name = "id000000"
    m.scan_saving.proposal_type = "inhouse"
    m.scan_saving.filename = _FILENAME


@pytest.fixture
def submit_mock(mocker, current_session_mock):
    return mocker.patch("blissoda.id22.stscan_processor.submit")


@pytest.fixture
def stscan_processor(tmpdir, submit_mock):
    return StScanProcessor(
        convert_workflow=str(tmpdir / "convert.json"),
        rebinsum_workflow=str(tmpdir / "rebinsum.json"),
        extract_workflow=str(tmpdir / "extract.json"),
    )


def test_create_workflows(stscan_processor, tmpdir):
    stscan_processor.__info__()
    assert (tmpdir / "convert.json").exists()
    assert (tmpdir / "rebinsum.json").exists()
    assert (tmpdir / "extract.json").exists()


def test_persist_changes(stscan_processor, tmpdir):
    stscan_processor.rebindirs = dict()
    stscan_processor.binsize = [0.002, 0.003]
    stscan_processor.delta2theta = 0.004
    stscan_processor.range = 0, 10
    stscan_processor.resfile = "/tmp/temp.res"
    stscan_processor.do_rebin = True

    def assert_values():
        assert stscan_processor.rebindirs == dict()
        assert stscan_processor.binsize == [0.002, 0.003]
        assert stscan_processor.delta2theta == [0.004]
        assert stscan_processor.range == [0, 10]
        assert stscan_processor.resfile == "/tmp/temp.res"
        assert stscan_processor.do_rebin

    assert_values()

    stscan_processor.convert_workflow = str(tmpdir / "convert2.json")
    stscan_processor.rebinsum_workflow = str(tmpdir / "rebinsum2.json")
    stscan_processor.extract_workflow = str(tmpdir / "extract2.json")

    assert_values()

    stscan_processor = StScanProcessor(
        convert_workflow=str(tmpdir / "convert2.json"),
        rebinsum_workflow=str(tmpdir / "rebinsum2.json"),
        extract_workflow=str(tmpdir / "extract2.json"),
    )

    assert_values()


def test_info(stscan_processor):
    assert stscan_processor.__info__()


def test_submit_convert(stscan_processor, submit_mock, tmpdir):
    stscan_processor.submit_workflows()

    calls = [
        mock.call(
            args=(str(tmpdir / "convert.json"),),
            kwargs={
                "inputs": [
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "convert", "name": "outprefix", "value": "id000000"},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                ]
            },
            queue="solo1",
        )
    ]

    submit_mock.assert_has_calls(calls)


def test_submit_rebin(stscan_processor, submit_mock, tmpdir):
    stscan_processor.do_rebin = True
    stscan_processor.submit_workflows()

    calls = [
        mock.call(
            args=(str(tmpdir / "convert.json"),),
            kwargs={
                "inputs": [
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "convert", "name": "outprefix", "value": "id000000"},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                ]
            },
            queue="solo1",
        ),
        mock.call(
            args=(str(tmpdir / "rebinsum.json"),),
            kwargs={
                "inputs": [
                    {"id": "rebin", "name": "delta2theta", "value": 0.003},
                    {"id": "sum", "name": "binsize", "value": 0.002},
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "rebin", "name": "outprefix", "value": "id000000"},
                    {"id": "rebin", "name": "primary_outdir", "value": _PROCESSED_DIR},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                    {"id": "sum", "name": "primary_outdir", "value": _PROCESSED_DIR},
                ]
            },
            queue="solo2",
        ),
    ]

    submit_mock.assert_has_calls(calls)


def test_submit_sum(stscan_processor, submit_mock, tmpdir):
    stscan_processor.do_sum = True
    stscan_processor.submit_workflows()

    calls = [
        mock.call(
            args=(str(tmpdir / "convert.json"),),
            kwargs={
                "inputs": [
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "convert", "name": "outprefix", "value": "id000000"},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                ]
            },
            queue="solo1",
        ),
        mock.call(
            args=(str(tmpdir / "rebinsum.json"),),
            kwargs={
                "inputs": [
                    {"id": "rebin", "name": "delta2theta", "value": 0.003},
                    {"id": "sum", "name": "binsize", "value": 0.002},
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "rebin", "name": "outprefix", "value": "id000000"},
                    {"id": "rebin", "name": "primary_outdir", "value": _PROCESSED_DIR},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                    {"id": "sum", "name": "primary_outdir", "value": _PROCESSED_DIR},
                ]
            },
            queue="solo2",
        ),
    ]

    submit_mock.assert_has_calls(calls)


def test_submit_sum_multiparams(stscan_processor, submit_mock, tmpdir):
    stscan_processor.do_sum = True
    stscan_processor.binsize = [0.002, 0.003]
    stscan_processor.delta2theta = [0.004, 0.005]

    stscan_processor.submit_workflows()

    calls = [
        mock.call(
            args=(str(tmpdir / "convert.json"),),
            kwargs={
                "inputs": [
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "convert", "name": "outprefix", "value": "id000000"},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                ]
            },
            queue="solo1",
        ),
        mock.call(
            args=(str(tmpdir / "rebinsum.json"),),
            kwargs={
                "inputs": [
                    {"id": "rebin", "name": "delta2theta", "value": 0.004},
                    {"id": "sum", "name": "binsize", "value": 0.002},
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "rebin", "name": "outprefix", "value": "id000000"},
                    {"id": "rebin", "name": "primary_outdir", "value": _PROCESSED_DIR},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                    {"id": "sum", "name": "primary_outdir", "value": _PROCESSED_DIR},
                ]
            },
            queue="solo2",
        ),
        mock.call(
            args=(str(tmpdir / "rebinsum.json"),),
            kwargs={
                "inputs": [
                    {"id": "rebin", "name": "delta2theta", "value": 0.005},
                    {"id": "sum", "name": "binsize", "value": 0.002},
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "rebin", "name": "outprefix", "value": "id000000"},
                    {"id": "rebin", "name": "primary_outdir", "value": _PROCESSED_DIR},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                    {"id": "sum", "name": "primary_outdir", "value": _PROCESSED_DIR},
                ]
            },
            queue="solo2",
        ),
        mock.call(
            args=(str(tmpdir / "rebinsum.json"),),
            kwargs={
                "inputs": [
                    {"id": "rebin", "name": "delta2theta", "value": 0.004},
                    {"id": "sum", "name": "binsize", "value": 0.003},
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "rebin", "name": "outprefix", "value": "id000000"},
                    {"id": "rebin", "name": "primary_outdir", "value": _PROCESSED_DIR},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                    {"id": "sum", "name": "primary_outdir", "value": _PROCESSED_DIR},
                ]
            },
            queue="solo2",
        ),
        mock.call(
            args=(str(tmpdir / "rebinsum.json"),),
            kwargs={
                "inputs": [
                    {"id": "rebin", "name": "delta2theta", "value": 0.005},
                    {"id": "sum", "name": "binsize", "value": 0.003},
                    {"id": "wait", "name": "filename", "value": _FILENAME},
                    {"id": "wait", "name": "entries", "value": []},
                    {"id": "rebin", "name": "outprefix", "value": "id000000"},
                    {"id": "rebin", "name": "primary_outdir", "value": _PROCESSED_DIR},
                    {
                        "id": "convert",
                        "name": "primary_outdir",
                        "value": _PROCESSED_DIR,
                    },
                    {"id": "sum", "name": "primary_outdir", "value": _PROCESSED_DIR},
                ]
            },
            queue="solo2",
        ),
    ]

    submit_mock.assert_has_calls(calls)
