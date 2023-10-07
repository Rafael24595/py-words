from commons.optional import optional
import xml.etree.ElementTree as XML
from domain.soup_panel.soup_config_param import soup_config_param

class soup_config_builder():
    
    @classmethod
    def build(cls, params: soup_config_param):
        xml = XML.parse("assets/app/clean-soup/configuration/soup_config.xml")
        dependencies = xml.getroot().find('input/receivers')
        dimension = dependencies.find('dimensions_receiver/dependencies/dependency')
        
        for parameter in dimension.findall("parameters/parameter"):
            match(parameter.find("name").text):
                case "Height":
                    parameter.find("value").text = str(params.height())
                case "Width":
                    parameter.find("value").text = str(params.width())
                case "Split Geometry":
                    geometry_value: optional[XML.Element] = cls.__get_geometry(parameter, params.geometry())
                    if geometry_value.is_some():
                        geometry_value.unwrap().attrib["status"] = "enabled"
                case "Range":
                    parameter.find("value").text = str(params.geometry_range())
                        
        return XML.tostring(xml.getroot(), encoding='utf8')
    
    @classmethod
    def __get_geometry(cls, parameter: XML.Element, geometry: str) -> optional[XML.Element]:
        for value in parameter.findall("values/value"):
            if value.text == geometry:
                return optional.some(value)
        return optional.none()