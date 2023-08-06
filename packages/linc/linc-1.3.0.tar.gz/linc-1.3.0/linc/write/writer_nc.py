import time
import warnings
import pkg_resources
from pathlib import Path
from typing import Any
from collections.abc import Iterable
from pdb import set_trace

import numpy as np
from cftime import date2num

from ..models import DataFile
from ..reader import read_file
from ..config import Config
from ..config.models import LidarChannel
from ..parse.utils import parse_date_from_filename

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from netCDF4 import Dataset  # type: ignore


def write_nc_legacy(
    files: Iterable[Path | str],
    output_file: Path | str,
    config: Config,
) -> None:
    _f = sorted(list(files), key = lambda p: Path(p).name)

    nc = Dataset(output_file, "w")
    nc.history = "Created " + time.ctime(time.time())
    nc.generated_with = str(pkg_resources.get_distribution("linc").egg_name())
    
    bin_width = config.lidar.bin_width
    bin_count = config.lidar.bin_count
    channel_array = np.array(filter_real_channels(config.lidar.channels))
    first_time = parse_date_from_filename(Path(_f[0]).name)

    time_dim = nc.createDimension("time", None)
    range_dim = nc.createDimension("range", config.lidar.bin_count)
    channel_dim = nc.createDimension("channel", channel_array.shape[0])

    time_var = nc.createVariable("time", "i4", ("time",), compression="zlib")
    time_var.units = f"milliseconds since {first_time.isoformat().replace('T', ' ')}"
    time_var.calendar = "proleptic_gregorian"

    range_var = nc.createVariable(
        "range", "f4", ("range",), compression="zlib"
    )
    range_var[:] = np.arange(
        bin_width, bin_width * (bin_count + 1), bin_width
    )
    
    channel_var = nc.createVariable(
        "channel", "S8", ("channel",)
    )
    channel_var[:] = channel_array
    
    signal_vars = create_signal_variables(nc, config)
    
    for idx_f, iter_file in enumerate(_f):
        current_file = read_file(iter_file, config = config)
        
        write_signal_vars(current_file, time_var, signal_vars, idx_f)

    write_attrs(nc, config)
    

    nc.close()
    
def write_signal_vars(current_file: DataFile, time_var: Any ,signal_vars: list[Any], index: int) -> None:
    time_var[index] = date2num(
            current_file.header.start_date, units=time_var.units, calendar = time_var.calendar
        )
    for (channel_str, channel_var) in signal_vars:
            channel_var[index, :] = current_file.dataset[channel_str].values  # type: ignore
    

def write_attrs(nc: Any, config: Config) -> None:
    for k, v in config.lidar.attrs.items():
        set_or_create_attr(nc, attr_name=k, attr_value=v)


def create_signal_variables(nc: Any, config: Config) -> list[Any]:
    channels_vars: list[tuple[str, Any]] = []
    for channel in list(map(lambda x: x.name, config.lidar.channels)):
        channel_str = channel

        try:
            signal_var = nc.createVariable(
                f"{channel_str}",
                "f4",
                ("time", "range"),
                compression="zlib",
            )
        except:
            raise ValueError(f"problem creating variable: {channel_str}")

        channels_vars.append((channel_str, signal_var))
    return channels_vars

def set_or_create_attr(var, attr_name, attr_value):
    if attr_name in var.ncattrs(): 
        var.setncattr(attr_name, attr_value)
        return
    try:
        var.UnusedNameAttribute = attr_value
        var.renameAttribute("UnusedNameAttribute", attr_name)
    except TypeError:
        raise TypeError(f"Type of attribute {attr_name} is {type(attr_value)} which cannot be written in netCDF")
    return

def filter_real_channels(lidar_channels: list[LidarChannel]) -> list[str]:
    """This function retrieves the lidar channel regardless if stderr or signal.
    For example, if there are two LidarChannel signal_532xpa and stderr_532xpa, it only returns 532xpa to channels list

    Args:
        lidar_channels (list[LidarChannel]): list of config sourced channels

    Returns:
        list[str]: strings with the convention wavelenght|telescope|polarization|aq_type. Ej: 532xpa
    """
    channels: set[str] = set({})
    
    
    for lidar_channel in lidar_channels:
        channels |= {lidar_channel.name.split("_")[1]}
    
    return list(channels)