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

import numpy as np
import pytest

from ifes_apt_tc_data_modeling.utils.nx_ion import NxIon
from ifes_apt_tc_data_modeling.utils.utils import create_nuclide_hash


# commented out expected test results are those returned when PRACTICAL_MINIMUM_HALF_LIFE = 0.0
@pytest.mark.parametrize(
    "nuclide_hash, left, right, expected",
    [
        (create_nuclide_hash(["H"]), 0.0, 10.0, "H +"),
        (create_nuclide_hash(["H", "H"]), 0.0, 10.0, "H H"),
        (create_nuclide_hash(["Be"]), 5.0, 17.0, "Be +"),  # Be
        (create_nuclide_hash(["Tc"]), 84.0, 120.0, "Tc"),  # Tc +
        (create_nuclide_hash(["Ra"]), 216.0, 236.0, "Ra"),
        (create_nuclide_hash(["U"]), 228.0, 249.0, "U"),
        (create_nuclide_hash(["Th"]), 222.0, 242.0, "Th"),
        (create_nuclide_hash(["Yb"]), 165.0, 206.0, "Yb +"),
        (create_nuclide_hash(["Fr"]), 222.0, 224.0, "Fr"),  # "Fr +"
        (create_nuclide_hash(["Cr", "Cr", "O"]), 57.819, 61.159, "Cr Cr O ++"),
    ],
    ids=[
        "hydrogen_landscape",
        "hydrogen_pair_landscape",
        "beryllium_landscape",
        "technetium_landscape",
        "radon_landscape",
        "uranium_landscape",
        "thorium_landscape",
        "ytterbium_landscape",
        "francium_landscape",
        "molecular_ion_cr_cr_o",
    ],
)
def test_combinatorial_analysis(
    nuclide_hash: np.uint16, left: np.float64, right: np.float64, expected: str
):
    m_ion = NxIon(nuclide_hash=nuclide_hash, charge_state=1)
    m_ion.add_range(left, right)
    m_ion.comment = ""
    m_ion.apply_combinatorics()
    m_ion.report()
    # print(m_ion.charge_state_model["nuclide_hash"])
    # print(m_ion.charge_state_model["charge_state"])
    assert expected == m_ion.name


import numpy as np

from ifes_apt_tc_data_modeling.utils.definitions import NEUTRON_NUMBER_FOR_ELEMENT
from ifes_apt_tc_data_modeling.utils.molecular_ions import MolecularIonBuilder
from ifes_apt_tc_data_modeling.utils.utils import isotope_to_hash

# find more examples on testing the ion library here
# https://gitlab.com/paraprobe/paraprobe-toolbox/examples/analyses/molecular_ions


def test_combinatorial_walk():
    # Cerium oxide molecular ion, motivated by the following ranging definition line
    # from an rrng file of I think it was Karen Kruska's
    # issue 5 Range33=187.4800 190.2560 Vol:0.12084 Ce:1 O:3 Color:00FF00
    # many duplicates

    mion = MolecularIonBuilder(
        min_abundance=0.0,
        min_abundance_product=0.0,
        min_half_life=np.inf,
        sacrifice_uniqueness=True,
        verbose=True,
    )

    mion.combinatorics(
        [
            isotope_to_hash(58, NEUTRON_NUMBER_FOR_ELEMENT),
            isotope_to_hash(8, NEUTRON_NUMBER_FOR_ELEMENT),
            isotope_to_hash(8, NEUTRON_NUMBER_FOR_ELEMENT),
            isotope_to_hash(8, NEUTRON_NUMBER_FOR_ELEMENT),
        ],
        187.4800,
        190.2560,
    )

    assert len(mion.candidates) == 40


@pytest.mark.parametrize(
    "metastability,expected", [(True, 1), (False, 0)], ids=[">0.4.3", "<=0.4.3"]
)
def test_stable_and_metastable_isotopes(metastability: bool, expected: int):
    mion = MolecularIonBuilder(
        min_abundance=0.0,
        min_abundance_product=0.0,
        min_half_life=np.inf,
        sacrifice_uniqueness=True,
        verbose=True,
        metastability_analysis=metastability,
    )

    mion.combinatorics(
        [isotope_to_hash(73, 107)],
        179.9474648 - 1.0e-3,
        179.9474648 + 1.0e-3,
    )

    assert len(mion.candidates) == expected

    # for cand in mion.candidates:
    #     print(cand.nuclide_hash)
