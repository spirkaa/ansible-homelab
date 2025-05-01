# ESPHome SdFat Component

Компонент для esphome на основе библиотеки [SdFat](https://github.com/greiman/SdFat) для добавления строк в конец указанного файла на карте памяти SD.

## Ограничения

Не поддерживаются каталоги, перезапись, чтение или удаление файлов. Файлы создаются с таймштампом по умолчанию, а не с актуальным временем.

## Подключение

```yaml
esphome:
  libraries:
    - SPI
    - SdFat

external_components:
  - source: components

sd_fat:
  id: sd_fat1
  cs_pin: GPIO15
```

## Использование

```yaml
lambda: |-
  id(sd_fat1).append_file("test.csv", "a;b;c");
```
