#include <cpprest/http_client.h>
#include <cpprest/filestream.h>
#include <cpprest/json.h>
#include "htmlcxx/html/ParserDom.h"
#include <cppcoro/sync_wait.hpp>
#include <cppcoro/task.hpp>
#include <fstream>
#include <iostream>
#include <sstream>

using namespace utility;
using namespace web;
using namespace web::http;
using namespace web::http::client;
using namespace concurrency::streams;
using namespace std;
using namespace htmlcxx;

cppcoro::task<utility::string_t> get_content(const utility::string_t& url) {
    http_client client(url);
    http_response response = co_await client.request(methods::GET);
    if (response.status_code() != status_codes::OK) {
        throw std::runtime_error("Failed to connect to server.");
    }
    string_t html_content = co_await response.extract_string();
    HTML::ParserDom parser;
    tree<HTML::Node> dom = parser.parseTree(utility::conversions::to_utf8string(html_content));
    tree<HTML::Node>::iterator it = dom.begin();
    tree<HTML::Node>::iterator end = dom.end();
    co_return parser.render(it, end);
}

void traverse_json(const json::value& input_json, json::value& output_json) {
    for (const auto& pair : input_json.as_object()) {
        auto key = pair.first;
        auto value = pair.second;
        if (value.is_object()) {
            json::value inner_output;
            traverse_json(value, inner_output);
            output_json[key] = inner_output;
        } else if (key == "Link") {
            output_json[key] = value;
            try {
                auto content = cppcoro::sync_wait(get_content(value.as_string()));
                output_json["Content"] = json::value(utility::conversions::to_string_t(content));
            } catch (const std::exception& e) {
                std::cerr << "Error: " << e.what() << '\n';
            }
        }
    }
}

int main() {
    ifstream input_file("../capi.json");
    stringstream buffer;
    buffer << input_file.rdbuf();
    input_file.close();

    json::value input_json = json::value::parse(buffer.str());
    json::value output_json;

    traverse_json(input_json, output_json);

    ofstream output_file("output.json");
    output_file << output_json.serialize();
    output_file.close();

    return 0;
}
