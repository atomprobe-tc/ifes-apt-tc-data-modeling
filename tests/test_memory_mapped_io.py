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

import mmap
import os
from pathlib import Path

import numpy as np


# @typing.no_type_check
def get_memory_mapped_data(
    file_path: str,
    data_type: str,
    offset_bytes: int,
    skip_that_many_bytes_stride: tuple[int, ...],
    data_shape: tuple[int, ...],
):
    """Read typed data from memory-mapped file from offset with stride."""
    # https://stackoverflow.com/questions/60493766/ \
    #       read-binary-flatfile-and-skip-bytes for I/O access details

    with (
        open(file_path, "rb") as fp,
        mmap.mmap(fp.fileno(), length=0, access=mmap.ACCESS_READ) as memory_mapped,
    ):
        # examples
        # shape = (n, m)
        # strides = (row_stride, col_stride)
        # every 3rd row use shape=(n // 3, m), strides=(row_stride * 3, col_stride)
        # every 3rd col use shape=(n, m // 3), strides=(row_stride, col_stride * 3)
        return np.ndarray(
            shape=data_shape,
            dtype=data_type,
            buffer=memory_mapped,
            offset=offset_bytes,
            strides=skip_that_many_bytes_stride,
        ).copy()
        """
        return np.ndarray(
            buffer=memory_mapped,
            dtype=data_type,
            offset=data_offset,
            strides=data_stride,
            shape=data_shape,
        ).copy()
        """
    return None


def test_memory_mapped_io():
    file_path = Path(f"{os.getcwd()}/tests/data/utils/memory_mapped_io.raw")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    data_type_literal = "<f4"
    item_size = np.dtype(data_type_literal).itemsize
    assert item_size == 4
    twod_write = np.linspace(1, 24, 24, dtype=data_type_literal).reshape(6, 4)

    assert np.shape(twod_write) == (6, 4)
    assert twod_write.dtype == np.dtype("<f4")
    twod_write.tofile(file_path)

    twod_read = get_memory_mapped_data(
        file_path, "<f4", 0, (4 * item_size, item_size), (6, 4)
    )

    assert np.shape(twod_read) == (6, 4)
    assert twod_read.dtype == np.dtype("<f4")
    np.testing.assert_array_equal(twod_read, twod_write)

    oned_read = get_memory_mapped_data(file_path, "<f4", 0, (1 * item_size,), (6 * 4,))
    assert np.shape(oned_read) == (6 * 4,)
    assert twod_read.dtype == np.dtype("<f4")
    np.testing.assert_array_equal(oned_read, twod_write.reshape(6 * 4))

    return

    for row_idx in [0, 1, 2, 3]:
        each_second_row = get_memory_mapped_data(
            file_path,
            "<f4",
            row_idx * 4 * item_size,
            (2 * 4 * item_size, item_size),
            (6 // 2, 4),
        )

    # each dim-th column
    for column_idx in [0, 1, 2, 3]:
        # explicitly 2d
        read_data = get_memory_mapped_data(
            file_path,
            "<f4",
            column_idx * item_size,
            (3 * item_size, item_size * 3),
            (4, 3 // 3),
        )  # skip each 3rd column
        # 1d only
        read_data = get_memory_mapped_data(
            file_path, "<f4", column_idx * item_size, (4 * item_size,), (6,)
        )  # skip each 3rd column

        # print(f"{np.shape(read_data)}, {read_data.dtype}, {read_data}")
        # del read_data
        assert True
