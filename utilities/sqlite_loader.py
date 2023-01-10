"""
 SPDX-License-Identifier: MIT
   Copyright (c) 2023, SCANOSS
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:
   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
"""
import argparse
import itertools
import os
import sys

import yaml
import sqlite3
from tqdm import tqdm

SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS purl2cpe(
    purl TEXT,
    cpe TEXT,
    UNIQUE(purl,cpe)
);
"""

SQL_INSERT_PURL2CPE = """
INSERT INTO purl2cpe (purl, cpe)
VALUES (?, ?)
ON CONFLICT DO NOTHING;
"""


def setup_sqlite(data_dir: str, db_file: str, debug: bool = False, quiet: bool = False) -> bool:
    """
    Walk the given data directory, load the PURL2CPE relationships and write to an SQLite file
    :param data_dir: data directory to walk
    :param db_file: SQLite file to write results into
    :param debug: print debug statements
    :param quiet: run in quiet mode
    :return: Success (True) or Failure (False)
    """
    if not db_file:
        print_stderr('No DB file specified to write results into.')
        return False
    if not data_dir:
        print_stderr('No data directory specified to retrieve data.')
        return False
    if os.path.exists(db_file) and not os.access(db_file, os.W_OK):
        print_stderr(f'DB file already exists and is not writable: {db_file}')
        return False

    cpes_file_name = 'cpes.yml'
    cpes_file_paths = []
    # First, build the list of paths for all cpes.yml file
    for root, directories, files in os.walk(data_dir):
        if cpes_file_name in files:
            cpes_file_paths.append(os.path.join(root, cpes_file_name))

    if not cpes_file_paths or len(cpes_file_paths) == 0:
        print_stderr(f'No relationship files found in: {data_dir}')
        return False
    if debug:
        print_stderr(f'Found {len(cpes_file_paths)} relationships to process')
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # Create the table to hold the pairs data
    cursor.execute(SQL_CREATE_TABLE)
    # For each cpe file, we have to generate the purls.yml file path
    progress_bar = cpes_file_paths
    if not quiet:
        progress_bar = tqdm(cpes_file_paths)
    for cpes_file_path in progress_bar:
        purls_file_path = f'{os.path.dirname(cpes_file_path)}/purls.yml'
        if not os.path.exists(cpes_file_path):
            print_stderr(f'CPE file does not exist, skipping: {cpes_file_path}')
            continue
        if not os.path.exists(purls_file_path):
            print_stderr(f'PURL file does not exist, skipping: {purls_file_path}')
            continue
        # Read the 2 yaml files in 2 separate lists and build all possible pairs.
        # Then insert each pair into the cpe2purl sqlite table
        if debug:
            print_stderr(f'Processing {cpes_file_path}...')
        with open(cpes_file_path, 'r') as cpes_file, open(purls_file_path, 'r') as purls_file:
            cpe_list = yaml.safe_load(cpes_file)['cpes']
            purls_list = yaml.safe_load(purls_file)['purls']
            purl_cpe_pairs = list(itertools.product(purls_list, cpe_list))
            for purl_cpe_pair in purl_cpe_pairs:
                cursor.execute(SQL_INSERT_PURL2CPE, purl_cpe_pair)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    if not quiet:
        print_stderr(f'PURL2CPE relationship data written to: {db_file}')
    return True


def print_stderr(*args, **kwargs):
    """
    Print the given message to STDERR
    """
    print(*args, file=sys.stderr, **kwargs)


def setup_args():
    """
    Setup command line arguments
    :return: arguments object
    """
    parser = argparse.ArgumentParser(description=f'SCANOSS PURL2CPE Loader. License: MIT')
    parser.add_argument('data_dir', metavar='DATA-DIR', type=str, help='Data folder location')
    parser.add_argument('--output', '-o', type=str, default='purl2cpe.db',
                        help='SQLite DB file (optional - default purl2cpe.db).')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrites')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug messages')
    parser.add_argument('--quiet', '-q', action='store_true', help='Enable quiet mode')
    args = parser.parse_args()
    return args


def main():
    """
    Run the SQLite loader utility
    """
    args = setup_args()

    if not os.path.exists(args.data_dir) or not os.path.isdir(args.data_dir):
        print_stderr(f'Specified data directory does not exist or is not a folder: {args.data_dir}')
        exit(1)
    if os.path.exists(args.output) and not args.force:
        print_stderr(f'Specified output DB ({args.output}) already exists. Use --force to overwrite.')
        exit(1)
    if not setup_sqlite(args.data_dir, args.output, args.debug, args.quiet):
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()

