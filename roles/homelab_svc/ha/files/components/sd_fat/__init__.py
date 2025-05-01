import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.const import CONF_CS_PIN, CONF_ID

sd_fat_ns = cg.esphome_ns.namespace("sd_fat")
SdFatComponent = sd_fat_ns.class_("SdFatComponent", cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(SdFatComponent),
        cv.Required(CONF_CS_PIN): pins.internal_gpio_output_pin_schema,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    cs_pin = await cg.gpio_pin_expression(config[CONF_CS_PIN])
    cg.add(var.set_cs_pin(cs_pin))
