# m-formatter-logging là thư viện python để write log cho các module BackEnd-Mobio

#### Version:
Phiên bản hiện tại `1.0.4`

#### Cài đặt:
`pip3 install m-formatter-logging`

#### Sử dụng:
1. Gọi func log tương ứng với level mong muốn.
- Sử dụng tham số `sensitive=True` (default=False) trong trường hợp dữ liệu log có data nhạy cảm (Ví dụ: thông tin PII của profile, mật khẩu của user, mã voucher,...).
- Sử dụng key extra để log thêm thông tin (chỉ show trên hệ thống ELK).
```
if __name__ == '__main__':
    def test():
        MobioLogging().info('app_test_lib_logging::test():info', sensitive=True, extra={"key1": "value1"})
        try:
            a = 1 / 0
            MobioLogging().info('__init__::test():a: %s' % a)
        except Exception as ex1:
            MobioLogging().error('app_test_lib_logging::test():error: %s' % ex1, sensitive=True)

        MobioLogging().debug('app_test_lib_logging::test():debug')
        MobioLogging().warning('app_test_lib_logging::test():warning', sensitive=False)

    test()
```


2. Sử dụng file custom config:
```
config_file_path = 'path/to/config/file'
MobioLogging().file_config(self, config_file_path)
```


3. Sử dụng custom filter để xử lý cụ thể 1 trường hợp log:
```
class CustomizeFilterRecords():
    def filter(self, record):
        if record.key1 == 'value1':
            return False # no log
        return True

MobioLogging().logger.addFilter(CustomizeFilterRecords())
```

#### Changelog:

##### v1.0.4:
* Cập nhật lại mô tả trong README.

##### v1.0.3:
* Phiên bản đầu tiên.
