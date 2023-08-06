"""Client for Quantuloop Quantum Simulator Suite on AWS"""

from __future__ import annotations
# Copyright 2023 Quantuloop
from ctypes import *
from io import BytesIO
from hashlib import sha256
from typing import Literal
import json
import zipfile
from ket import quantum_exec_timeout
from ket.base import set_quantum_execution_target
from ket.clib.libket import JSON
import requests

SECRET = ""
URL = ""
VERIFY = True
TIMEOUT = None

AVAILABLE_SIMULATORS = []
SIMULATOR = ''
SEED = '0'
DUMP_TYPE = 'shots'
SHOTS = '1024'
GPU_COUNT = '1'
PRECISION = '1'

__all__ = ['available_simulators', 'set_server', 'set_simulator']


def available_simulators() -> list[str]:
    """Get and update the list of the available simulators"""

    global AVAILABLE_SIMULATORS
    AVAILABLE_SIMULATORS = requests.get(
        URL+'/simulators', timeout=30, verify=VERIFY).json()

    return AVAILABLE_SIMULATORS


def set_server(*,
               url: str,
               secret: str | None = None,
               timeout: int | None = None,
               verify=True):
    """Set the Server and Secret for quantum execution"""
    global SECRET

    if secret:
        SECRET = sha256(secret.encode('utf-8')).hexdigest().encode('utf-8')
    global URL
    URL = url
    global VERIFY
    VERIFY = verify
    global TIMEOUT

    if timeout:
        TIMEOUT = timeout
        quantum_exec_timeout(timeout)

    available_simulators()


def set_simulator(simulator: str | None = None, *,
                  seed: int | None = None,
                  dump_type: str | None = None,
                  shots: int | None = None,
                  gpu_count: int | None = None,
                  precision: Literal[1, 2] | None = None):
    """Set a Quantuloop simulator as the quantum execution target

    You must run :func:`quantuloop_aws_client.set_server` before calling this function.

    Quantuloop QueST is not affected by the "precision" and "gpu_count" parameters 
    as it is only available for single GPU and single precision execution.        

    .. warning::

        Your internet connection can strongly influence the total execution time when
        setting the "dump_type" parameter to "vector" or "probability".

    Args:
        simulator: see :func:`quantuloop_aws_client.available_simulators` for the available simulators
        token: Quantuloop Access Token
        toke_file: Path to load the Quantuloop Access Token from a file
        seed: Initialize the simulator RNG
        dump_type: must be "vector", "probability", or "shots", default "vector"
        shots: select the number of shots if ``dump_type`` is "shots"
        gpu_count: maximum number of GPUs; if set to 0, simulation will use all available GPUs
        precision: floating point precision used in the simulation; positive values are: 1 for single precision (float) and 2 for double precision
    """

    if simulator is not None:
        simulator = simulator.lower()
        if simulator not in AVAILABLE_SIMULATORS:
            raise ValueError(
                f"parameter 'simulator' must be in {AVAILABLE_SIMULATORS}"
            )
        global SIMULATOR
        SIMULATOR = simulator

    if seed is not None:
        if seed < 0:
            raise ValueError('parameter "seed" must be greater than zero')
        global SEED
        SEED = str(seed)

    if dump_type:
        if dump_type not in ["vector", "probability", "shots"]:
            raise ValueError(
                'parameter "dump_type" must be "vector", "probability", or "shots"')
        global DUMP_TYPE
        DUMP_TYPE = dump_type

    if shots:
        if shots < 1:
            raise ValueError('parameter "shots" must be greater than one')
        global SHOTS
        SHOTS = str(shots)

    if gpu_count is not None:
        global GPU_COUNT
        GPU_COUNT = str(int(gpu_count))

    if precision is not None:
        if precision not in [1, 2]:
            raise ValueError('parameter "dump_type" must be int(1) or int(2)')
        global PRECISION
        PRECISION = str(int(precision))

    set_quantum_execution_target(_send_quantum_code)


def _send_quantum_code(process):
    process.serialize_quantum_code(JSON)
    process.serialize_metrics(JSON)

    code_data, code_size, _ = process.get_serialized_quantum_code()
    metrics_data, metrics_size, _ = process.get_serialized_metrics()

    request_files = BytesIO()
    with zipfile.ZipFile(request_files, 'w',
                         compression=zipfile.ZIP_BZIP2,
                         compresslevel=9) as zip_file:
        zip_file.writestr('secret.txt', SECRET)
        zip_file.writestr('quantum_code.json',
                          bytearray(code_data[:code_size.value]))
        zip_file.writestr('quantum_metrics.json',
                          bytearray(metrics_data[:metrics_size.value]))

    zipped_result = requests.get(
        URL+'/run',
        params={
            'simulator': SIMULATOR,
            'seed': SEED,
            'dump_type': DUMP_TYPE,
            'shots': SHOTS,
            'gpu_count': GPU_COUNT,
            'precision': PRECISION,
            'timeout': TIMEOUT,
        },
        files={
            'request.zip': ('request.zip', request_files.getvalue(), 'application/zip')
        },
        timeout=None if TIMEOUT == 0 else TIMEOUT,
        verify=VERIFY
    ).content

    try:
        with zipfile.ZipFile(BytesIO(zipped_result), 'r') as zip_file:
            result = zip_file.read('result.json')

        result_size = len(result)

        process.set_serialized_result(
            (c_uint8*result_size)(*result),
            result_size,
            JSON
        )
    except zipfile.BadZipFile:
        raise RuntimeError(json.loads(zipped_result))
