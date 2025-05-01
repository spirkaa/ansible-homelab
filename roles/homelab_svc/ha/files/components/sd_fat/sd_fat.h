#pragma once

#include "esphome/core/component.h"
#include <esphome/core/hal.h>

namespace esphome {
namespace sd_fat {

class SdFatComponent : public Component {
  public:
    void setup() override;
    void dump_config() override;

    void set_cs_pin(InternalGPIOPin *pin) { cs_pin_ = pin; }
    void append_file(char *path, char *data);

    bool card_available;
  protected:
    InternalGPIOPin *cs_pin_;
    bool is_card_available_();
    float card_size_;
};

}  // namespace sd_fat
}  // namespace esphome
