#define DISABLE_FS_H_WARNING

#include <SPI.h>
#include <SdFat.h>

#include "esphome/core/log.h"
#include "sd_fat.h"

namespace esphome {
namespace sd_fat {

static const char *TAG = "sd_fat";

SdFat sd;
SdFile file;

void SdFatComponent::setup() {
  is_card_available_();
}

bool SdFatComponent::is_card_available_() {
  if (sd.begin(cs_pin_->get_pin())) {
    this->card_size_ = sd.card()->sectorCount() * 0.000512;
    this->card_available = true;
    return true;
  }
  ESP_LOGE(TAG, "SD Card not available!");
  this->card_available = false;
  return false;
}

void SdFatComponent::append_file(char *path, char *data) {
  if (!is_card_available_()) {
    return;
  }
  if (!file.open(path, O_CREAT | O_WRITE | O_AT_END)) {
    ESP_LOGE(TAG, "Failed to open file %s", path);
    return;
  }
  size_t data_size = file.println(data);
  if (!file.close()) {
    ESP_LOGE(TAG, "Failed to close file %s", path);
    return;
  }
  ESP_LOGI(TAG, "File written: %s, data: %s, size: %d", path, data, data_size);
}

void SdFatComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "SD Fat Component:");
  LOG_PIN("  CS Pin: ", this->cs_pin_);
  if (this->card_available) {
    ESP_LOGCONFIG(TAG, "  SD Card size: %.2f MB", this->card_size_);
  } else {
    ESP_LOGE(TAG, "  SD Card not available!");
  }
}

}  // namespace sd_fat
}  // namespace esphome
