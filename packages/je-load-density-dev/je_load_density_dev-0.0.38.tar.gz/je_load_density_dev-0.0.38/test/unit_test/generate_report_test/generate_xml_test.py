from je_load_density import create_loading_test_user
from je_load_density import generate_xml_report
from je_load_density import start_test

# test and generate html

test_dict = {
    "request_method": "get",
    "request_url": "http://httpbin.org/get",
    "assert_result_dict": {"status_code": 200}
}
start_test(
    create_loading_test_user(test_dict),
    user_count=50, test_time=10, spawn_rate=10,
    web_ui_dict={"host": "127.0.0.1", "port": 8089},
)
# after test, you can generate html report
# if no data will raise exception
generate_xml_report()
