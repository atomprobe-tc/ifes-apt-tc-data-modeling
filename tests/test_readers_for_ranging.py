#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

import h5py
import pytest

from ifes_apt_tc_data_modeling.analysisset.analysisset_reader import (
    ReadAnalysissetFileFormat,
)
from ifes_apt_tc_data_modeling.env.env_reader import ReadEnvFileFormat
from ifes_apt_tc_data_modeling.fig.fig_reader import ReadFigTxtFileFormat
from ifes_apt_tc_data_modeling.imago.imago_reader import ReadImagoAnalysisFileFormat
from ifes_apt_tc_data_modeling.rng.rng_reader import ReadRngFileFormat
from ifes_apt_tc_data_modeling.rrng.rrng_reader import ReadRrngFileFormat
from ifes_apt_tc_data_modeling.utils.hfive import simple_hfive_file

READERS = [
    (
        ReadRrngFileFormat,
        "rrng",
        ".rrng",
        ["examples_without_provenance/ger_duesseldorf_kuehbach/Mo_range.rrng"],
    ),
    (
        ReadRngFileFormat,
        "rng",
        ".rng",
        [
            "examples_without_provenance/ger_duesseldorf_kuehbach/SeHoKim_R5076_44076_v02.rng"
        ],
    ),
    (
        ReadAnalysissetFileFormat,
        "analysisset",
        ".analysisset",
        ["examples_with_provenance/ZX21-T4.analysisset"],
    ),
    # note that Matlab FIG need processing first to a text file using matlab_fig_to_txt.m for the reader to function!
    (
        ReadFigTxtFileFormat,
        "fig",
        ".fig.txt",
        ["examples_without_provenance/ger_erlangen_felfer/R56_01769.rng.fig.txt"],
    ),
    # note that env files need a reformatting to utf-8 character encoding for the reader to function!
    (ReadEnvFileFormat, "env", ".env", ["examples_without_provenance/ErMnO.env"]),
    (
        ReadImagoAnalysisFileFormat,
        "imago",
        ".analysis",
        ["examples_without_provenance/default.analysis"],
    ),
]


@pytest.mark.parametrize(
    "reader_cls,reader_type,mime_type,file_names", READERS, ids=[r[1] for r in READERS]
)
def test_readers_for_ranging(reader_cls, reader_type, mime_type, file_names):
    prefix = f"{os.getcwd()}/tests/data/{reader_type}/"

    for fpath in file_names:
        print(f">>>> {fpath}")
        full_path = f"{prefix}/{fpath}"

        assert os.path.exists(full_path)
        assert full_path.lower().endswith(mime_type)

        reader = reader_cls(full_path)
        ranges = getattr(reader, reader_type)

        with h5py.File(f"{full_path}.nxs", "w") as h5w:
            idx = 1
            for ion in ranges["molecular_ions"]:
                simple_hfive_file(h5w, idx, ion)
                idx += 1

        assert os.path.exists(f"{full_path}.nxs")
