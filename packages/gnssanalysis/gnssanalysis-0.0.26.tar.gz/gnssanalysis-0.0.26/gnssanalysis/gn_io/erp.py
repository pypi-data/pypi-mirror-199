import os
from collections.abc import Callable, Iterable
from io import BytesIO as _BytesIO
from numbers import Real
from typing import List, TextIO, Union

import pandas as _pd

from gnssanalysis import gn_io as _gn_io


def normalise_headers(headers: Iterable[str]) -> List[str]:
    """Apply :func: `gn_io.erp.normalise_headers` to all headers in an iterable

    :param Iterable[str] headers: Iterable of header strings obtained from an ERP file
    :return List[str]: List of normalised headers as per :func: `gn_io.erp.normalise_headers`
    """
    return [normalise_header(h) for h in headers]


def normalise_header(header: str) -> str:
    """Normalise an ERP header to a canonical version where possible

    To attempt to rationalise the various forms that ERP headers can take this function starts
    by removing all hyphens, upper-casing all characters, and then attempting to match a
    collection of known patterns (eg. XPOLE, X, XP) to map to a canonical version.

    :param str header: ERP header
    :return str: Normalised ERP header
    """
    # Send everything to uppercase and remove all hyphens
    header = header.replace("-", "").upper()
    # Find things that start with an S or end in "SIG" and normalise to our chosen std dev convention
    header = normalise_stddevcorr_headers(header)
    # Match all things in a group (X, XPOLE, etc.) and return our preferred version
    return get_canonical_header(header)


def merge_hyphen_headers(raw_split_header: Iterable[str]) -> List[str]:
    """Take a list of raw headers from an ERP file and merge hyphenated headers that got split

    In some ERP files hyphenated headers, such as UTC-TAI, occasionally have spaces before or after
    the hyphen/minus sign. This breaks tokenisation as the header gets split into multiple parts.
    This function re-merges those header components.

    :param Iterable[str] raw_split_header: ERP header line that has been split/tokenized
    :return List[str]: List of ERP headers with hyphen-seperated headers merged
    """
    # Copy to avoid mutating input list
    headers = list(raw_split_header)
    # Do things starting with hyphens first (this is all we've seen in practice)
    # Detect items that start with a "-" and merge them with previous item
    # Find position of header item that starts with "-"
    hyphen_idx = next((i for i, v in enumerate(headers) if v.startswith("-")), None)
    # Don't process if we didn't find anything or it's at the start of the headers (nothing to merge forward with)
    while hyphen_idx is not None and hyphen_idx > 0:
        # Merge the hyphen-starting label with the label before it
        merged_header_label = headers[hyphen_idx - 1] + headers[hyphen_idx]
        # Replace those two header items with their merged equivalent
        headers[hyphen_idx - 1 : hyphen_idx + 1] = [merged_header_label]
        # See if we need to do it again for a new header item
        hyphen_idx = next((i for i, v in enumerate(headers) if v.startswith("-")), None)
    # Do things ending with hyphens now
    # Detect items that end with a "-" and merge them with the next item
    # Find position of header item that ends with "-"
    hyphen_idx = next((i for i, v in enumerate(headers) if v.endswith("-")), None)
    # Don't process if we didn't find anything or it's at the end of the headers (nothing to merge next with)
    while hyphen_idx is not None and hyphen_idx < (len(headers) - 1):
        # Merge the hyphen-starting label with the label before it
        merged_header_label = headers[hyphen_idx] + headers[hyphen_idx + 1]
        # Replace those two header items with their merged equivalent
        headers[hyphen_idx : hyphen_idx + 2] = [merged_header_label]
        # See if we need to do it again for a new header item
        hyphen_idx = next((i for i, v in enumerate(headers) if v.endswith("-")), None)
    return headers


def normalise_stddevcorr_headers(header: str) -> str:
    """Create a canonical representation of (partially normalised) std.dev or corr ERP headers

    This canonicisation process involves stripping a leading "S" from a header, replacing it with
    a trailing "SIG", stripping a leading "C" and replacing it with a trainling "CORR" and changing
    a "COR" suffix to be "CORR".

    :param str header: paritially normalised ERP header
    :return str: ERP header with canonical std.dev and corr. representation
    """
    if header[0] == "S":
        return header[1:] + "SIG"
    elif header[0] == "C":
        return header[1:] + "CORR"
    elif header.endswith("COR"):
        return header + "R"
    else:
        return header


def get_canonical_header(header: str) -> str:
    """Map ERP column header to a canonical representation of that column header

    :param str header: ERP column header
    :return str: Canonical column header
    """
    if header.endswith("SIG"):
        base_header_label = get_canonical_header(header[:-3])
        if base_header_label.endswith("pole"):
            return base_header_label[:-4] + "sig"
        return base_header_label + "sig"
    elif header.endswith("CORR"):
        base_header_label = get_canonical_header(header[:-4])
        if base_header_label.endswith("pole"):
            return base_header_label[:-4] + "corr"
        return base_header_label + "corr"
    else:
        if header in ["X", "XP", "XPOLE"]:
            return "Xpole"
        elif header in ["XRT", "XDOT"]:
            return "Xrt"
        elif header in ["Y", "YP", "YPOLE"]:
            return "Ypole"
        elif header in ["YRT", "YDOT"]:
            return "Yrt"
        elif header in ["UT1UTC"]:
            return "UT1-UTC"
        elif header in ["UT1RUTC"]:
            return "UT1R-UTC"
        elif header in ["UT1TAI"]:
            return "UT1-TAI"
        elif header in ["UT1RTAI"]:
            return "UT1R-TAI"
        elif header in ["UT1", "UT"]:
            return "UT"
        elif header in ["UT1R", "UTR"]:
            return "UTR"
        elif header in ["LOD", "LD"]:
            return "LOD"
        elif header in ["LODR", "LDR"]:
            return "LODR"
        elif header in ["NF"]:
            return "Nf"
        elif header in ["NR"]:
            return "Nr"
        elif header in ["NT"]:
            return "Nt"
        elif header in ["DEPS", "DE"]:
            return "Deps"
        elif header in ["DPSI", "DP"]:
            return "Dpsi"
        elif header in ["XUT", "XT"]:
            return "XUT"
        elif header in ["YUT", "YT"]:
            return "YUT"
        else:
            return header


def get_erp_scaling(normalised_header: str, original_header: str) -> Union[int, float]:
    """Get scaling factor to go from ERP stored data to "SI units"

    Scare quotes around "SI units" because rates are still per day, but in general converts to
    seconds and arcseconds rather than eg. microseconds.

    :param str normalised_header: Normalised ERP column header
    :param str original_header: Original ERP column header (needed for correlation data)
    :return Union[int, float]: Scaling factor to (multiplicatively) go from ERP-file data to "SI units"
    """
    if normalised_header in ["Xpole", "Xsig", "Ypole", "Ysig", "Xrt", "Xrtsig", "Yrt", "Yrtsig"]:
        return 1e-6
    elif normalised_header in ["UT1-UTC", "UT1R-UTC", "UT1-TAI", "UT1R-TAI", "UTsig", "UTRsig"]:
        return 1e-7
    elif normalised_header in ["LOD", "LODR", "LODsig"]:
        return 1e-7
    elif normalised_header in ["Deps", "Depssig", "Dpsi", "Dpsisig"]:
        return 1e-6
    elif normalised_header in ["XYcorr", "XUTcorr", "YUTcorr"]:
        if original_header.startswith("C"):
            return 1e-2
        else:
            return 1
    else:
        return 1


def get_erp_unit_string(normalised_header: str, original_header: str) -> str:
    """Get unit description string for a given ERP column

    :param str normalised_header: Normalised ERP column header
    :param str original_header: Original ERP column header (needed for correlation data)
    :return str: Units description string for the ERP column
    """
    if normalised_header in ["Xpole", "Xsig", "Ypole", "Ysig"]:
        return "E-6as"
    elif normalised_header in ["Xrt", "Xrtsig", "Yrt", "Yrtsig"]:
        return "E-6as/d"
    elif normalised_header in ["UT1-UTC", "UT1R-UTC", "UT1-TAI", "UT1R-TAI", "UTsig", "UTRsig"]:
        return "E-7s"
    elif normalised_header in ["LOD", "LODR", "LODsig", ]:
        return "E-7s/d"
    elif normalised_header in ["Deps", "Depssig", "Dpsi", "Dpsisig"]:
        return "E-6"
    elif normalised_header == ["XYcorr", "XUTcorr", "YUTcorr"]:
        if original_header.startswith("C"):
            return "E-2"
        else:
            return ""
    else:
        return ""


def read_erp(
    erp_path: Union[str, bytes, os.PathLike], normalise_header_names: bool = True, convert_units: bool = True
) -> _pd.DataFrame:
    """Read an ERP file from disk into a pandas DataFrame

    :param Union[str, bytes, os.PathLike] erp_path: Path to ERP file on disk
    :param bool normalise_header_names: If True, change header names to canonical versions, defaults to True
    :param bool convert_units: Convert natural ERP file units to "SI units", forces `normalise_header_names`, defaults to True
    :raises RuntimeError: Raised if the start of the column headers can't be found and the file can't be parsed
    :return _pd.DataFrame: A dataframe containing all the columnar data from the ERP file as well as an `attrs` dict
        holding the header comments in a "header_comments" property and whether the data has been scaled in a "scaled"
        property
    """
    if convert_units:
        # SI units implies normalised headers, so that we know which columns
        # to process
        normalise_header_names = True

    content = _gn_io.common.path2bytes(str(erp_path))
    # Do a bit of magic to work out where the header is
    # This is not a standardised location so we try to find the first element
    # of the header (MJD) and work back from there
    start_of_mjd_in_header = content.rfind(b"MJD")
    if start_of_mjd_in_header == -1:
        start_of_mjd_in_header = content.rfind(b"mjd")
    if start_of_mjd_in_header == -1:
        raise RuntimeError(f"ERP file {erp_path} has an invalid format")
    start_of_header = content.rfind(b"\n", 0, start_of_mjd_in_header) + 1
    start_of_units_line = content.find(b"\n", start_of_header) + 1
    start_of_data = content.find(b"\n", start_of_units_line) + 1
    start_of_comments = content.find(b"\n") + 1

    hyphen_merged_headers = merge_hyphen_headers(content[start_of_header:start_of_units_line].decode("utf-8").split())
    if normalise_header_names:
        headers = normalise_headers(hyphen_merged_headers)
    else:
        headers = hyphen_merged_headers

    data_of_interest = content[start_of_data:]  # data block
    erp_df = _pd.read_csv(
        _BytesIO(data_of_interest),
        delim_whitespace=True,
        names=headers,
        index_col=False,
    )

    if convert_units:
        # Convert appropriate columns to proper units, see ERP doc
        for header, orig_header in zip(headers, hyphen_merged_headers):
            erp_df[header] = erp_df[header] * get_erp_scaling(header, orig_header)
    elif normalise_header_names:
        # We need an exception for any correlation columns, there are two conventions
        # about how to store correlation information and if we convert the headers without
        # converting the correlation values then we lose this distinction and wind up
        # with ambiguous data
        for header, orig_header in zip(headers, hyphen_merged_headers):
            if orig_header.startswith("C-"):
                erp_df[header] = erp_df[header] * 1e-2
    erp_df.attrs["scaled"] = convert_units
    erp_df.attrs["header_comments"] = content[start_of_comments:start_of_header].decode(encoding="utf-8")

    return erp_df


def get_erp_column_formatter(column_header: str, mjd_precision: int = 2) -> Callable[[Real], str]:
    """Get an appropriate formatter for the data a column of ERP data

    Different ERP columns are formatted slightly differently and so this function provides access to
    appropriate formatters for each column. This includes being able to specify a non-standard number
    of decimal points for the MJD to account for PEA's non-standard high-rate ERP data.

    :param str column_header: Normalised ERP column header
    :param int mjd_precision: Numer of decimal places to use for MJD column, defaults to 2
    :return Callable[[Real], str]: Formatting function that can be applied to values in a column
    """
    if column_header == "MJD":
        return lambda val: format(val, f".{mjd_precision}f")
    elif column_header.endswith("corr") or column_header.endswith("cor"):
        return lambda val: format(val, ".3f")
    else:
        return lambda val: format(int(val), "d")


def format_erp_column(column_series: _pd.Series, mjd_precision: int = 2) -> _pd.Series[str]:
    """Formats an ERP DataFrame column into appropriate strings

    Includes the ability to specify a non-standard number of decimal points for MJD to account
    for PEA's non-standard high-rate ERP data.

    :param _pd.Series column_series: DataFrame column to format into strings
    :param int mjd_precision: Number of decimal places to use for MJD column, defaults to 2
    :return _pd.Series[str]: Series (DataFrame column) full of formatted values
    """
    formatter = get_erp_column_formatter(str(column_series.name), mjd_precision)
    return column_series.apply(formatter)


def write_erp(erp_df: _pd.DataFrame, path: Union[str, bytes, os.PathLike], mjd_precision: int = 2):
    """Write an ERP DataFrame to a file on disk

    :param _pd.DataFrame erp_df: DataFrame of ERP data to write to disk
    :param Union[str, bytes, os.PathLike] path: Path to output file
    :param int mjd_precision: Number of decimal places to user for MJD column, defaults to 2
    """
    with open(path, "w") as file:
        write_erp_to_stream(erp_df, file, mjd_precision)


def write_erp_to_stream(erp_df: _pd.DataFrame, stream: TextIO, mjd_precision: int = 2):
    """Write an ERP DataFrame to a TextIO stream

    _extended_summary_

    :param _pd.DataFrame erp_df: DataFrame of ERP data to write to stream
    :param TextIO stream: IO stream to write ERP data to
    :param int mjd_precision: Number of decimal places to use for MJD column, defaults to 2
    """
    # Front matter
    stream.write("version 2\n")
    stream.write(erp_df.attrs.get("header_comments", "EOP SOLUTION") + "\n")
    # Work out required column widths
    min_width_header = [len(col) for col in erp_df.columns]
    unit_strings = [get_erp_unit_string(normalise_header(header), header) for header in erp_df.columns]
    min_width_units = [len(s) for s in unit_strings]
    if erp_df.attrs.get("scaled", False):
        scaling_series = _pd.Series({col: get_erp_scaling(normalise_header(col), col) for col in erp_df.columns})
    else:
        scaling_series = _pd.Series({col: 1 for col in erp_df.columns})
    value_strings_df = (erp_df / scaling_series).apply(lambda col: format_erp_column(col, mjd_precision))
    min_width_values = value_strings_df.applymap(len).max()
    column_widths = [max(ws) for ws in zip(min_width_header, min_width_units, min_width_values)]
    # Column headers
    stream.write(" ".join(s.rjust(w) for (s, w) in zip(erp_df.columns, column_widths)))
    stream.write("\n")
    # Column units
    stream.write(" ".join(s.rjust(w) for (s, w) in zip(unit_strings, column_widths)))
    stream.write("\n")
    # Values
    for (_, row) in value_strings_df.iterrows():
        stream.write(" ".join(s.rjust(w) for (s, w) in zip(row, column_widths)))
        stream.write("\n")
