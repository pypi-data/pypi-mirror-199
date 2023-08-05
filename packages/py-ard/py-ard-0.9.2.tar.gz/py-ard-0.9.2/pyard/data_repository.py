# -*- coding: utf-8 -*-
#
#    py-ard
#    Copyright (c) 2020 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#
import sys
import copy
from collections import namedtuple
import functools
import sqlite3
from urllib.error import HTTPError

import pandas as pd

from . import db
from .broad_splits import broad_splits_dna_mapping
from .broad_splits import broad_splits_ser_mapping
from .misc import (
    get_2field_allele,
    get_3field_allele,
    number_of_fields,
    get_1field_allele,
)
from .misc import expression_chars, get_G_name, get_P_name

# GitHub URL where IMGT HLA files are downloaded.
from pyard.smart_sort import smart_sort_comparator

IMGT_HLA_URL = "https://raw.githubusercontent.com/ANHIG/IMGTHLA/"

ars_mapping_tables = [
    "dup_g",
    "dup_lgx",
    "g_group",
    "lgx_group",
    "exon_group",
    "p_not_g",
]
ARSMapping = namedtuple("ARSMapping", ars_mapping_tables)

code_mapping_tables = [
    "alleles",
    "xx_codes",
    "who_alleles",
    "who_group",
]


def expression_reduce(df):
    """
    For each group of expression alleles, check if __all__ of
    them have the same expression character. If so, the second field
    with the expression character is a valid allele.
    Rule:
        The general rule is that expression characters can propagate up to two
        field level if all three-field and/or four-field alleles have the same
        expression character.

    :param df: dataframe with Allele column that is all expression characters
    :return: 2 field allele or None
    """
    for e in expression_chars:
        if df["Allele"].str.endswith(e).all():
            return df["2d"].iloc[0] + e
    return None


def generate_ars_mapping(db_connection: sqlite3.Connection, imgt_version):
    if db.tables_exist(db_connection, ars_mapping_tables):
        dup_g = db.load_dict(
            db_connection, table_name="dup_g", columns=("allele", "g_group")
        )
        dup_lgx = db.load_dict(
            db_connection, table_name="dup_lgx", columns=("allele", "lgx_group")
        )
        g_group = db.load_dict(
            db_connection, table_name="g_group", columns=("allele", "g")
        )
        lgx_group = db.load_dict(
            db_connection, table_name="lgx_group", columns=("allele", "lgx")
        )
        exon_group = db.load_dict(
            db_connection, table_name="exon_group", columns=("allele", "exon")
        )
        p_not_g = db.load_dict(
            db_connection, table_name="p_not_g", columns=("allele", "lgx")
        )
        return (
            ARSMapping(
                dup_g=dup_g,
                dup_lgx=dup_lgx,
                g_group=g_group,
                lgx_group=lgx_group,
                exon_group=exon_group,
                p_not_g=p_not_g,
            ),
            None,
        )

    df = load_g_group(imgt_version)

    df_p_group = load_p_group(imgt_version)
    p_group = df_p_group.set_index("A")["P"].to_dict()

    # compare df_p_group["2d"] with df["2d"] to find 2-field alleles in the
    # P-group that aren't in the G-group
    p_not_in_g = set(df_p_group["2d"]) - set(df["2d"])

    # filter to find these 2-field alleles (2d) in the P-group data frame
    df_p_not_g = df_p_group[df_p_group["2d"].isin(p_not_in_g)]

    # dictionary which will define the table
    p_not_g = df_p_not_g.set_index("A")["lgx"].to_dict()

    # multiple Gs
    # goal: identify 2-field alleles that are in multiple G-groups

    # group by 2d and G, and select the 2d column and count the columns
    mg = df.drop_duplicates(["2d", "G"])["2d"].value_counts()
    # filter out the mg with count > 1, leaving only duplicates
    # take the index from the 2d version the data frame, make that a column
    # and turn that into a list
    multiple_g_list = mg[mg > 1].reset_index()["index"].to_list()

    # Keep only the alleles that have more than 1 mapping
    dup_g = (
        df[df["2d"].isin(multiple_g_list)][["G", "2d"]]
        .drop_duplicates()
        .groupby("2d", as_index=True)
        .agg("/".join)
        .to_dict()["G"]
    )

    # multiple lgx
    mlgx = df.drop_duplicates(["2d", "lgx"])["2d"].value_counts()
    multiple_lgx_list = mlgx[mlgx > 1].reset_index()["index"].to_list()

    # Keep only the alleles that have more than 1 mapping
    dup_lgx = (
        df[df["2d"].isin(multiple_lgx_list)][["lgx", "2d"]]
        .drop_duplicates()
        .groupby("2d", as_index=True)
        .agg("/".join)
        .to_dict()["lgx"]
    )

    # Creating dictionaries with mac_code->ARS group mapping
    df_g = pd.concat(
        [
            df[["2d", "G"]].rename(columns={"2d": "A"}),
            df[["3d", "G"]].rename(columns={"3d": "A"}),
            df[["A", "G"]],
        ],
        ignore_index=True,
    )
    g_group = df_g.set_index("A")["G"].to_dict()

    df_lgx = pd.concat(
        [
            df[["2d", "lgx"]].rename(columns={"2d": "A"}),
            df[["3d", "lgx"]].rename(columns={"3d": "A"}),
            df[["A", "lgx"]],
        ]
    )
    lgx_group = df_lgx.set_index("A")["lgx"].to_dict()

    # exon
    df_exon = pd.concat(
        [
            df[["A", "3d"]].rename(columns={"3d": "exon"}),
        ]
    )
    exon_group = df_exon.set_index("A")["exon"].to_dict()

    # save
    db.save_dict(
        db_connection,
        table_name="p_not_g",
        dictionary=p_not_g,
        columns=("allele", "lgx"),
    )
    db.save_dict(
        db_connection,
        table_name="dup_g",
        dictionary=dup_g,
        columns=("allele", "g_group"),
    )
    db.save_dict(
        db_connection,
        table_name="dup_lgx",
        dictionary=dup_lgx,
        columns=("allele", "lgx_group"),
    )
    db.save_dict(
        db_connection, table_name="g_group", dictionary=g_group, columns=("allele", "g")
    )
    db.save_dict(
        db_connection,
        table_name="lgx_group",
        dictionary=lgx_group,
        columns=("allele", "lgx"),
    )
    db.save_dict(
        db_connection,
        table_name="exon_group",
        dictionary=exon_group,
        columns=("allele", "exon"),
    )

    return (
        ARSMapping(
            dup_g=dup_g,
            dup_lgx=dup_lgx,
            g_group=g_group,
            lgx_group=lgx_group,
            exon_group=exon_group,
            p_not_g=p_not_g,
        ),
        p_group,
    )


def load_g_group(imgt_version):
    # load the hla_nom_g.txt
    ars_g_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/hla_nom_g.txt"
    df = pd.read_csv(ars_g_url, skiprows=6, names=["Locus", "A", "G"], sep=";").dropna()
    # the G-group is named for its first allele
    df["G"] = df["A"].apply(get_G_name)
    # convert slash delimited string to a list
    df["A"] = df["A"].apply(lambda a: a.split("/"))
    # convert the list into separate rows for each element
    df = df.explode("A")
    #  A*   + 02:01   = A*02:01
    df["A"] = df["Locus"] + df["A"]
    df["G"] = df["Locus"] + df["G"]
    # Create 2,3 field versions of the alleles
    df["2d"] = df["A"].apply(get_2field_allele)
    df["3d"] = df["A"].apply(get_3field_allele)
    # lgx is 2 field version of the G group allele
    df["lgx"] = df["G"].apply(get_2field_allele)

    return df


def load_p_group(imgt_version):
    # load the hla_nom_p.txt
    ars_p_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/hla_nom_p.txt"
    # example: C*;06:06:01:01/06:06:01:02/06:271;06:06P
    df_p = pd.read_csv(
        ars_p_url, skiprows=6, names=["Locus", "A", "P"], sep=";"
    ).dropna()
    # the P-group is named for its first allele
    df_p["P"] = df_p["A"].apply(get_P_name)
    # convert slash delimited string to a list
    df_p["A"] = df_p["A"].apply(lambda a: a.split("/"))
    df_p = df_p.explode("A")
    # C* 06:06:01:01/06:06:01:02/06:271 06:06P
    df_p["A"] = df_p["Locus"] + df_p["A"]
    df_p["P"] = df_p["Locus"] + df_p["P"]
    # C* 06:06:01:01 06:06P
    # C* 06:06:01:02 06:06P
    # C* 06:271 06:06P
    df_p["2d"] = df_p["A"].apply(get_2field_allele)
    # lgx has the P-group name without the P for comparison
    df_p["lgx"] = df_p["P"].apply(get_2field_allele)
    return df_p


def generate_alleles_and_xx_codes_and_who(
    db_connection: sqlite3.Connection, imgt_version, ars_mappings, p_group
):
    """
    Checks to see if there's already an allele list file for the `imgt_version`
    in the `data_dir` directory. If not, will download the file and create
    a valid allele set and corresponding xx codes.

    The format of the AlleleList file has a 6-line header with a header
    on the 7th line
    ```
    # file: Allelelist.3290.txt
    # date: 2017-07-10
    # version: IPD-IMGT/HLA 3.29.0
    # origin: https://github.com/ANHIG/IMGTHLA/Allelelist.3290.txt
    # repository: https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/allelelist/Allelelist.3290.txt
    # author: WHO, Steven G. E. Marsh (steven.marsh@ucl.ac.uk)
    AlleleID,Allele
    HLA00001,A*01:01:01:01
    HLA02169,A*01:01:01:02N
    HLA14798,A*01:01:01:03
    HLA15760,A*01:01:01:04
    HLA16415,A*01:01:01:05
    HLA16417,A*01:01:01:06
    HLA16436,A*01:01:01:07
    ```

    :param db_connection: Database connection to the sqlite database
    :param imgt_version: IMGT database version
    :param ars_mappings: ARSMapping object to ARS mapping tables
    :return: None, updates self
    """
    if db.tables_exist(db_connection, code_mapping_tables):
        valid_alleles = db.load_set(db_connection, "alleles")

        who_alleles = db.load_set(db_connection, "who_alleles")
        who_group = db.load_dict(db_connection, "who_group", ("who", "allele_list"))
        who_group = {k: v.split("/") for k, v in who_group.items()}

        xx_codes = db.load_dict(db_connection, "xx_codes", ("allele_1d", "allele_list"))
        xx_codes = {k: v.split("/") for k, v in xx_codes.items()}

        exp_alleles = db.load_dict(
            db_connection, "exp_alleles", ("exp_allele", "allele_list")
        )
        exp_alleles = {k: v.split("/") for k, v in exp_alleles.items()}

        return valid_alleles, who_alleles, xx_codes, who_group, exp_alleles

    # Create a Pandas DataFrame from the mac_code list file
    # Skip the header (first 6 lines) and use only the Allele column
    if imgt_version == "Latest":
        allele_list_url = f"{IMGT_HLA_URL}Latest/Allelelist.txt"
    else:
        if imgt_version == "3130":
            # 3130 was renamed to 3131 for Allelelist file only 🤷🏾‍
            imgt_version = "3131"
        allele_list_url = (
            f"{IMGT_HLA_URL}Latest/allelelist/Allelelist.{imgt_version}.txt"
        )

    try:
        allele_df = pd.read_csv(allele_list_url, header=6, usecols=["Allele"])
    except HTTPError as e:
        print(
            f"Failed importing alleles for version {imgt_version} from {allele_list_url}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Create a set of valid alleles
    # All 2-field, 3-field and the original Alleles are considered valid alleles
    allele_df["2d"] = allele_df["Allele"].apply(get_2field_allele)
    allele_df["3d"] = allele_df["Allele"].apply(get_3field_allele)
    # For all Alleles with expression characters, find 2-field valid alleles
    exp_alleles = allele_df[
        allele_df["Allele"].apply(
            lambda a: a[-1] in expression_chars and number_of_fields(a) > 2
        )
    ]
    exp_alleles = exp_alleles.groupby("2d").apply(expression_reduce).dropna()

    # flat_exp_alleles = {k: '/'.join(sorted(v, key=functools.cmp_to_key(smart_sort_comparator)))
    #                 for k, v in exp_alleles.items()}
    db.save_dict(
        db_connection, "exp_alleles", exp_alleles, ("exp_allele", "allele_list")
    )

    # Create valid set of alleles:
    # All full length alleles
    # All 3rd and 2nd field versions of longer alleles
    # All 2-field version of alleles with expression that can be reduced
    valid_alleles = (
        set(allele_df["Allele"])
        .union(set(allele_df["2d"]))
        .union(set(allele_df["3d"]))
        .union(set(exp_alleles))
    )

    # Create xx_codes mapping from the unique alleles in 2-field column
    xx_df = pd.DataFrame(allele_df["2d"].unique(), columns=["Allele"])
    # Also create a first-field column
    xx_df["1d"] = xx_df["Allele"].apply(lambda x: x.split(":")[0])
    # xx_codes maps a first field name to its 2 field expansion
    xx_codes = xx_df.groupby(["1d"]).apply(lambda x: list(x["Allele"])).to_dict()

    # Update xx codes with broads and splits
    for broad, splits in broad_splits_dna_mapping.items():
        for split in splits:
            if broad in xx_codes:
                xx_codes[broad].extend(xx_codes[split])
            else:
                xx_codes[broad] = copy.deepcopy(xx_codes[split])

    # Save this version of the valid alleles
    db.save_set(db_connection, "alleles", valid_alleles, "allele")
    # Save this version of xx codes
    flat_xx_codes = {
        k: "/".join(sorted(v, key=functools.cmp_to_key(smart_sort_comparator)))
        for k, v in xx_codes.items()
    }
    db.save_dict(db_connection, "xx_codes", flat_xx_codes, ("allele_1d", "allele_list"))

    # W H O
    who_alleles = allele_df["Allele"].to_list()
    # Save this version of the WHO alleles
    db.save_set(db_connection, "who_alleles", who_alleles, "allele")

    # Create WHO mapping from the unique alleles in the 1-field column
    allele_df["1d"] = allele_df["Allele"].apply(get_1field_allele)

    who_codes = pd.concat(
        [
            allele_df[["Allele", "1d"]].rename(columns={"1d": "nd"}),
            allele_df[["Allele", "2d"]].rename(columns={"2d": "nd"}),
            allele_df[["Allele", "3d"]].rename(columns={"3d": "nd"}),
            pd.DataFrame(ars_mappings.g_group.items(), columns=["Allele", "nd"]),
            pd.DataFrame(p_group.items(), columns=["Allele", "nd"]),
        ],
        ignore_index=True,
    )

    # remove valid alleles from who_codes to avoid recursion
    for k in who_alleles:
        if k in who_codes["nd"]:
            who_codes.drop(labels=k, axis="index")

    # drop duplicates
    who_codes = who_codes.drop_duplicates()

    # who_codes maps a first field name to its 2 field expansion
    who_group = who_codes.groupby(["nd"]).apply(lambda x: list(x["Allele"])).to_dict()

    # dictionary
    flat_who_group = {
        k: "/".join(sorted(v, key=functools.cmp_to_key(smart_sort_comparator)))
        for k, v in who_group.items()
    }
    db.save_dict(
        db_connection, "who_group", flat_who_group, columns=("who", "allele_list")
    )

    return valid_alleles, who_alleles, xx_codes, who_group, exp_alleles


def generate_short_nulls(db_connection, who_group):
    if db.table_exists(db_connection, "shortnulls"):
        shortnulls = db.load_dict(
            db_connection, "shortnulls", ("shortnull", "allele_list")
        )
        shortnulls = {k: v.split("/") for k, v in shortnulls.items()}
        return shortnulls

    # shortnulls
    # scan WHO alleles for those with expression characters and make shortnull mappings
    # DRB4*01:03N | DRB4*01:03:01:02N/DRB4*01:03:01:13N
    # DRB5*01:08N | DRB5*01:08:01N/DRB5*01:08:02N
    shortnulls = dict()
    for who in who_group:
        # e.g. DRB4*01:03
        expression_alleles = dict()
        if who[-1] not in expression_chars and who[-1] not in ["G", "P"] and ":" in who:
            for an_allele in who_group[who]:
                # if an allele in a who_group has an expression character but the group allele doesnt,
                # add it to shortnulls
                last_char = an_allele[-1]
                if last_char in expression_chars:
                    # e.g. DRB4*01:03:01:02N
                    a_shortnull = who + last_char
                    if a_shortnull not in expression_alleles:
                        expression_alleles[a_shortnull] = []
                    expression_alleles[a_shortnull].append(an_allele)
            # only create a shortnull if there is one expression character in this who_group
            # there is nothing to be done for who_groups that have both Q and L for example
            for a_shortnull in expression_alleles:
                # e.g. DRB4*01:03N
                shortnulls[a_shortnull] = "/".join(expression_alleles[a_shortnull])

    db.save_dict(db_connection, "shortnulls", shortnulls, ("shortnull", "allele_list"))
    shortnulls = {k: v.split("/") for k, v in shortnulls.items()}
    return shortnulls


def generate_mac_codes(db_connection: sqlite3.Connection, refresh_mac: bool):
    """
    MAC files come in 2 different versions:

    Martin: when they’re printed, the first is better for encoding and the
    second is better for decoding. The entire list was maintained both as an
    excel spreadsheet and also as a sybase database table. The excel was the
    one that was printed and distributed.

        **==> numer.v3.txt <==**

        Sorted by the length and the the values in the list
        ```
        "LAST UPDATED: 09/30/20"
        CODE	SUBTYPE

        AB	01/02
        AC	01/03
        AD	01/04
        AE	01/05
        AG	01/06
        AH	01/07
        AJ	01/08
        ```

        **==> alpha.v3.txt <==**

        Sorted by the code

        ```
        "LAST UPDATED: 10/01/20"
        *	CODE	SUBTYPE

            AA	01/02/03/05
            AB	01/02
            AC	01/03
            AD	01/04
            AE	01/05
            AF	01/09
            AG	01/06
        ```

    :param db_connection: Database connection to the sqlite database
    :param refresh_mac: Refresh the database with newer MAC data ?
    :return: None
    """
    mac_table_name = "mac_codes"
    if refresh_mac or not db.table_exists(db_connection, mac_table_name):
        # Load the MAC file to a DataFrame
        mac_url = "https://hml.nmdp.org/mac/files/numer.v3.zip"
        df_mac = pd.read_csv(
            mac_url,
            sep="\t",
            compression="zip",
            skiprows=3,
            names=["Code", "Alleles"],
            keep_default_na=False,
        )
        # Create a dict from code to alleles
        mac = df_mac.set_index("Code")["Alleles"].to_dict()
        # Save the mac dict to db
        db.save_dict(
            db_connection,
            table_name=mac_table_name,
            dictionary=mac,
            columns=("code", "alleles"),
        )


def to_serological_name(locus_name: str):
    """
    Map a DNA Allele name to Serological Equivalent.
    http://hla.alleles.org/antigens/recognised_serology.html
    Eg:
      A*1 -> A1
      ...
      DRB5*51 -> DR51
    :param locus_name: DNA Locus Name
    :return: Serological equivalent
    """
    locus, sero_number = locus_name.split("*")
    sero_locus = locus[:2]
    if sero_locus == "C":
        sero_locus = "Cw"
    sero_name = sero_locus + sero_number
    return sero_name


def generate_serology_mapping(db_connection: sqlite3.Connection, imgt_version):
    if not db.table_exists(db_connection, "serology_mapping"):
        """
        Read `rel_dna_ser.txt` file that contains alleles and their serological equivalents.

        The fields of the Alleles->Serological mapping file are:
           Locus - HLA Locus
           Allele - HLA Allele Name
           USA - Unambiguous Serological Antigen associated with allele
           PSA - Possible Serological Antigen associated with allele
           ASA - Assumed Serological Antigen associated with allele
           EAE - Expert Assigned Exceptions in search determinants of some registries

        EAE is ignored when generating the serology map.
        """
        rel_dna_ser_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/rel_dna_ser.txt"
        # Load WMDA serology mapping data from URL
        df_sero = pd.read_csv(
            rel_dna_ser_url,
            sep=";",
            skiprows=6,
            names=["Locus", "Allele", "USA", "PSA", "ASA", "EAE"],
            index_col=False,
        )

        # Remove 0 and ? from USA
        df_sero = df_sero[(df_sero["USA"] != "0") & (df_sero["USA"] != "?")]
        df_sero["Allele"] = df_sero.loc[:, "Locus"] + df_sero.loc[:, "Allele"]

        usa = df_sero[["Locus", "Allele", "USA"]].dropna()
        usa["Sero"] = usa["Locus"] + usa["USA"]

        psa = df_sero[["Locus", "Allele", "PSA"]].dropna()
        psa["PSA"] = psa["PSA"].apply(lambda row: row.split("/"))
        psa = psa.explode("PSA")
        psa = psa[(psa["PSA"] != "0") & (psa["PSA"] != "?")].dropna()
        psa["Sero"] = psa["Locus"] + psa["PSA"]

        asa = df_sero[["Locus", "Allele", "ASA"]].dropna()
        asa["ASA"] = asa["ASA"].apply(lambda x: x.split("/"))
        asa = asa.explode("ASA")
        asa = asa[(asa["ASA"] != "0") & (asa["ASA"] != "?")].dropna()
        asa["Sero"] = asa["Locus"] + asa["ASA"]

        sero_mapping_combined = pd.concat(
            [usa[["Sero", "Allele"]], psa[["Sero", "Allele"]], asa[["Sero", "Allele"]]]
        )

        # Map to only valid serological antigen name
        sero_mapping_combined["Sero"] = sero_mapping_combined["Sero"].apply(
            to_serological_name
        )

        sero_mapping = (
            sero_mapping_combined.groupby("Sero")
            .apply(lambda x: "/".join(sorted(x["Allele"])))
            .to_dict()
        )

        # map alleles for split serology to their corresponding broad
        # Update xx codes with broads and splits
        for broad, splits in broad_splits_ser_mapping.items():
            for split in splits:
                try:
                    sero_mapping[broad] = "/".join(
                        [sero_mapping[broad], sero_mapping[split]]
                    )

                except KeyError:
                    sero_mapping[broad] = sero_mapping[split]

        # re-sort allele lists into smartsort order
        for sero in sero_mapping.keys():
            sero_mapping[sero] = "/".join(
                sorted(
                    sero_mapping[sero].split("/"),
                    key=functools.cmp_to_key(smart_sort_comparator),
                )
            )

        # Save the serology mapping to db
        db.save_dict(
            db_connection,
            table_name="serology_mapping",
            dictionary=sero_mapping,
            columns=("serology", "allele_list"),
        )


def generate_v2_to_v3_mapping(db_connection: sqlite3.Connection, imgt_version):
    if not db.table_exists(db_connection, "v2_mapping"):
        # TODO: Create mapping table using both the allele list history and
        #  deleted alleles as reference.
        # Temporary Example
        v2_to_v3_example = {
            "A*0104": "A*01:04:01:01N",
            "A*0105N": "A*01:04:01:01N",
            "A*0111": "A*01:11N",
            "A*01123": "A*01:123N",
            "A*0115": "A*01:15N",
            "A*0116": "A*01:16N",
            "A*01160": "A*01:160N",
            "A*01162": "A*01:162N",
            "A*01178": "A*01:178N",
            "A*01179": "A*01:179N",
            "DRB5*02ZB": "DRB5*02:UTV",
        }
        db.save_dict(
            db_connection,
            table_name="v2_mapping",
            dictionary=v2_to_v3_example,
            columns=("v2", "v3"),
        )


def set_db_version(db_connection: sqlite3.Connection, imgt_version):
    """
    Set the IMGT database version number as a user_version string in
    the database itself.

    :param db_connection: Active SQLite Connection
    :param imgt_version: current imgt_version
    """
    # If version already exists, don't reset
    version = db.get_user_version(db_connection)
    if version:
        return version

    version = imgt_version

    if imgt_version == "Latest":
        from urllib.request import urlopen

        response = urlopen(
            "https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/release_version.txt"
        )
        for line in response:
            l = line.decode("utf-8")
            if l.find("version:") != -1:
                # Version line looks like
                # # version: IPD-IMGT/HLA 3.51.0
                version = l.split()[-1].replace(".", "")

    db.set_user_version(db_connection, int(version))
    print("Version:", version)
    return db.get_user_version(db_connection)


def get_db_version(db_connection: sqlite3.Connection):
    return db.get_user_version(db_connection)
