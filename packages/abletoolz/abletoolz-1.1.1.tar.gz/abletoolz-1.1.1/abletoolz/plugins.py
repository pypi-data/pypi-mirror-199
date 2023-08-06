import logging
import pathlib
import sys
import xml.etree.ElementTree as ET
from typing import Optional, Tuple, Union

from pydantic import BaseModel

sys.path.append(r"C:\Users\elixer\repos\_abletoolz")
# sys.path.append("/Users/fivehtp/repos/_abletoolz")
from abletoolz.ableton_set import AbletonSet
from abletoolz import decode_encode

logger = logging.getLogger(__name__)


def parse_vst_element(vst_element: ET.Element) -> Tuple[Optional[pathlib.Path], Optional[str], Optional[pathlib.Path]]:
    def handle_path_element(path_result):
        full_path = path_result.get("Value")
        if not full_path:
            logger.error("Couldn't get Path for %s", path_result)
            return None, None, None

        if not ("/" in full_path or "\\" in full_path):
            search_result = self.search_plugins(full_path)
            if search_result:
                return None, search_result.name, search_result
            return None, full_path, None

        path_separator = self.path_separator_type(full_path)
        name = full_path.split(path_separator)[-1]
        return pathlib.Path(full_path), name, None

    def handle_dir_element(path_result):
        dir_bin = path_result.find("Data")
        if not dir_bin:
            logger.error("Couldn't get Path for %s", path_result)
            return None, None, None

        text = dir_bin.text
        if not text:
            return None, None, None

        path = self._parse_hex_path(text)
        name_ele = vst_element.find("FileName")
        name = name_ele.get("Value", "") if name_ele is not None else "<>"

        if not path:
            logger.error("%sCouldn't parse absolute path for %s", Y, name)
            return None, name, None

        path_separator = self.path_separator_type(path)
        full_path = f"{path}{path_separator}{name}" if path[-1] != path_separator else f"{path}{name}"

        return pathlib.Path(full_path), name, None

    for plugin_path in ["Dir", "Path"]:
        path_results = vst_element.findall(f".//{plugin_path}")
        if not path_results:
            continue

        if plugin_path == "Path":
            return handle_path_element(path_results[0])
        elif plugin_path == "Dir":
            return handle_dir_element(path_results[0])

    logger.error("%sCouldn't parse plugin!", R)
    return None, None, None


class PluginData(BaseModel):
    data: Optional[str]
    file_name: Optional[str]
    plug_name: Optional[str]
    unique_id: Optional[int]
    buffer: Optional[str]


def parse_plugin_data(root: ET.Element) -> PluginData:
    """."""
    dir_element = root.find("Dir")
    path_element = root.find("Path")

    path = path_element.get("Value") if path_element is not None else None
    data = dir_element.findtext("Data") if dir_element is not None else None
    # decode_encode.

    file_name = root.find("FileName").get("Value") if root.find("FileName") is not None else None
    plug_name = root.find("PlugName").get("Value") if root.find("PlugName") is not None else None

    unique_id_str = root.findtext("UniqueId")
    unique_id = int(unique_id_str) if unique_id_str else None

    vst_preset = root.find(".//VstPreset")
    buffer = vst_preset.findtext("Buffer") if vst_preset is not None else None

    return PluginData(data=data, file_name=file_name, plug_name=plug_name, unique_id=unique_id, buffer=buffer)





als_set = pathlib.Path(
    "../test/sample_missing_fix Project/11.2.10_11 bass_pad fm8_350bars_172.00bpm.als"
)

ableton_set = AbletonSet(als_set)
ableton_set.parse()
plugins = []
for plugin_element in ableton_set.root.iter("PluginDesc"):
    for vst_element in plugin_element.iter("VstPluginInfo"):
        plugins.append(parse_plugin_data(vst_element))

print(plugins)
