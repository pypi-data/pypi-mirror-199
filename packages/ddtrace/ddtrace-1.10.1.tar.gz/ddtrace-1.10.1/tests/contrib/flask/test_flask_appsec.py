import json
import logging

from flask import Response
from flask import request
import pytest

from ddtrace.appsec._constants import SPAN_DATA_NAMES
from ddtrace.appsec.trace_utils import block_request_if_user_blocked
from ddtrace.constants import APPSEC_JSON
from ddtrace.ext import http
from ddtrace.internal import _context
from ddtrace.internal import constants
from ddtrace.internal.compat import six
from ddtrace.internal.compat import urlencode
from tests.appsec.test_processor import RULES_GOOD_PATH
from tests.appsec.test_processor import RULES_SRB
from tests.appsec.test_processor import RULES_SRB_METHOD
from tests.appsec.test_processor import RULES_SRB_RESPONSE
from tests.appsec.test_processor import _ALLOWED_IP
from tests.appsec.test_processor import _BLOCKED_IP
from tests.contrib.flask import BaseFlaskTestCase
from tests.utils import override_env
from tests.utils import override_global_config


_BLOCKED_USER = "123456"
_ALLOWED_USER = "111111"


class FlaskAppSecTestCase(BaseFlaskTestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    def _aux_appsec_prepare_tracer(self, appsec_enabled=True):
        self.tracer._appsec_enabled = appsec_enabled
        # Hack: need to pass an argument to configure so that the processors are recreated
        self.tracer.configure(api_version="v0.4")

    def test_flask_simple_attack(self):
        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/.git?q=1")
            assert resp.status_code == 404
            # Read response data from the test client to close flask.request and flask.response spans
            assert resp.data is not None
            root_span = self.pop_spans()[0]

            appsec_json = root_span.get_tag(APPSEC_JSON)
            assert "triggers" in json.loads(appsec_json if appsec_json else "{}")
            assert _context.get_item("http.request.uri", span=root_span) == "http://localhost/.git?q=1"
            query = dict(_context.get_item("http.request.query", span=root_span))
            assert query == {"q": "1"} or query == {"q": ["1"]}

    def test_flask_path_params(self):
        @self.app.route("/params/<item>")
        def dynamic_url(item):
            return item

        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/params/attack")
            assert resp.status_code == 200
            # Read response data from the test client to close flask.request and flask.response spans
            assert resp.data is not None
            root_span = self.pop_spans()[0]

            flask_args = root_span.get_tag("flask.view_args.item")
            assert flask_args == "attack"

            path_params = _context.get_item("http.request.path_params", span=root_span)
            assert path_params == {"item": "attack"}

    def test_flask_path_params_attack(self):
        @self.app.route("/params/<item>")
        def dynamic_url(item):
            return item

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_GOOD_PATH)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/params/w00tw00t.at.isc.sans.dfind")
            assert resp.status_code == 200

            root_span = self.pop_spans()[0]

            appsec_json = root_span.get_tag(APPSEC_JSON)
            assert "triggers" in json.loads(appsec_json if appsec_json else "{}")

            query = dict(_context.get_item("http.request.path_params", span=root_span))
            assert query == {"item": "w00tw00t.at.isc.sans.dfind"}

    def test_flask_querystrings(self):
        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            self.client.get("/?a=1&b&c=d")
            root_span = self.pop_spans()[0]
            query = dict(_context.get_item("http.request.query", span=root_span))
            assert query == {"a": "1", "b": "", "c": "d"} or query == {"a": ["1"], "b": [""], "c": ["d"]}
            self.client.get("/")
            root_span = self.pop_spans()[0]
            assert len(_context.get_item("http.request.query", span=root_span)) == 0

    def test_flask_cookie_sql_injection(self):
        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_GOOD_PATH)):
            self._aux_appsec_prepare_tracer()
            self.client.set_cookie("localhost", "attack", "1' or '1' = '1'")
            resp = self.client.get("/")
            assert resp.status_code == 404
            root_span = self.pop_spans()[0]

            appsec_json = root_span.get_tag(APPSEC_JSON)
            assert "triggers" in json.loads(appsec_json if appsec_json else "{}")
            assert _context.get_item("http.request.cookies", span=root_span)["attack"] == "1' or '1' = '1'"
            query = dict(_context.get_item("http.request.cookies", span=root_span))
            assert query == {"attack": "1' or '1' = '1'"} or query == {"attack": ["1' or '1' = '1'"]}

    def test_flask_cookie(self):
        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            self.client.set_cookie("localhost", "testingcookie_key", "testingcookie_value")
            resp = self.client.get("/")
            assert resp.status_code == 404
            # Read response data from the test client to close flask.request and flask.response spans
            assert resp.data is not None
            root_span = self.pop_spans()[0]

            assert root_span.get_tag(APPSEC_JSON) is None
            assert (
                _context.get_item("http.request.cookies", span=root_span)["testingcookie_key"] == "testingcookie_value"
            )
            query = dict(_context.get_item("http.request.cookies", span=root_span))
            assert query == {"testingcookie_key": "testingcookie_value"} or query == {
                "testingcookie_key": ["testingcookie_value"]
            }

    def test_flask_useragent(self):
        self.client.get("/", headers={"User-Agent": "test/1.2.3"})
        root_span = self.pop_spans()[0]
        assert root_span.get_tag(http.USER_AGENT) == "test/1.2.3"

    def test_flask_client_ip_header_set_by_env_var_valid(self):
        with override_global_config(dict(_appsec_enabled=True, client_ip_header="X-Use-This")):
            self.client.get("/?a=1&b&c=d", headers={"HTTP_X_CLIENT_IP": "8.8.8.8", "X-Use-This": "4.4.4.4"})
            spans = self.pop_spans()
            root_span = spans[0]
            assert root_span.get_tag(http.CLIENT_IP) == "4.4.4.4"

    def test_flask_body_urlencoded(self):
        @self.app.route("/body", methods=["GET", "POST", "DELETE"])
        def body():
            data = dict(request.form)
            return str(data), 200

        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            data = {"mytestingbody_key": "mytestingbody_value"}
            payload = urlencode(data)

            self.client.post("/body", data=payload, content_type="application/x-www-form-urlencoded")

            root_span = self.pop_spans()[0]
            query = dict(_context.get_item("http.request.body", span=root_span))

            assert root_span.get_tag(APPSEC_JSON) is None
            assert query == {"mytestingbody_key": "mytestingbody_value"}

    def test_flask_body_urlencoded_appsec_disabled_then_no_body(self):
        with override_global_config(dict(_appsec_enabled=False)):
            self._aux_appsec_prepare_tracer()
            payload = urlencode({"mytestingbody_key": "mytestingbody_value"})
            self.client.post("/", data=payload, content_type="application/x-www-form-urlencoded")
            root_span = self.pop_spans()[0]

            assert not _context.get_item("http.request.body", span=root_span)

    def test_flask_request_body_urlencoded_attack(self):
        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            payload = urlencode({"attack": "1' or '1' = '1'"})
            self.client.post("/", data=payload, content_type="application/x-www-form-urlencoded")
            root_span = self.pop_spans()[0]
            query = dict(_context.get_item("http.request.body", span=root_span))
            assert "triggers" in json.loads(root_span.get_tag(APPSEC_JSON))
            assert query == {"attack": "1' or '1' = '1'"}

    def test_flask_body_json(self):
        @self.app.route("/body", methods=["GET", "POST", "DELETE"])
        def body():
            data = request.get_json()
            return str(data), 200

        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            payload = {"mytestingbody_key": "mytestingbody_value"}

            self.client.post("/body", json=payload, content_type="application/json")

            root_span = self.pop_spans()[0]
            query = dict(_context.get_item("http.request.body", span=root_span))

            assert root_span.get_tag(APPSEC_JSON) is None
            assert query == {"mytestingbody_key": "mytestingbody_value"}

    def test_flask_body_json_attack(self):
        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            payload = {"attack": "1' or '1' = '1'"}
            self.client.post("/", json=payload, content_type="application/json")
            root_span = self.pop_spans()[0]
            query = dict(_context.get_item("http.request.body", span=root_span))
            assert "triggers" in json.loads(root_span.get_tag(APPSEC_JSON))
            assert query == {"attack": "1' or '1' = '1'"}

    def test_flask_body_xml(self):
        @self.app.route("/body", methods=["GET", "POST", "DELETE"])
        def body():
            data = request.data
            return data, 200

        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            payload = "<mytestingbody_key>mytestingbody_value</mytestingbody_key>"
            response = self.client.post("/body", data=payload, content_type="application/xml")
            assert response.status_code == 200
            assert response.data == b"<mytestingbody_key>mytestingbody_value</mytestingbody_key>"

            root_span = self.pop_spans()[0]
            query = dict(_context.get_item("http.request.body", span=root_span))

            assert root_span.get_tag(APPSEC_JSON) is None
            assert query == {"mytestingbody_key": "mytestingbody_value"}

    def test_flask_body_xml_attack(self):
        with override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            payload = "<attack>1' or '1' = '1'</attack>"
            self.client.post("/", data=payload, content_type="application/xml")
            root_span = self.pop_spans()[0]
            query = dict(_context.get_item("http.request.body", span=root_span))

            assert "triggers" in json.loads(root_span.get_tag(APPSEC_JSON))
            assert query == {"attack": "1' or '1' = '1'"}

    def test_flask_body_json_empty_body_logs_warning(self):
        with self._caplog.at_level(logging.DEBUG), override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            self.client.post("/", data="", content_type="application/json")
            assert "Failed to parse werkzeug request body" in self._caplog.text

    def test_flask_body_json_bad_logs_warning(self):
        with self._caplog.at_level(logging.DEBUG), override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            self.client.post("/", data="not valid json", content_type="application/json")
            assert "Failed to parse werkzeug request body" in self._caplog.text

    def test_flask_body_xml_bad_logs_warning(self):
        with self._caplog.at_level(logging.DEBUG), override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            self.client.post("/", data="bad xml", content_type="application/xml")
            assert "Failed to parse werkzeug request body" in self._caplog.text

    def test_flask_body_xml_empty_logs_warning(self):
        with self._caplog.at_level(logging.DEBUG), override_global_config(dict(_appsec_enabled=True)):
            self._aux_appsec_prepare_tracer()
            self.client.post("/", data="", content_type="application/xml")
            assert "Failed to parse werkzeug request body" in self._caplog.text

    def test_flask_ipblock_nomatch_200_json(self):
        @self.app.route("/")
        def route():
            return "OK", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_GOOD_PATH)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/", headers={"X-Real-Ip": _ALLOWED_IP})
            root_span = self.pop_spans()[0]
            assert resp.status_code == 200
            assert not _context.get_item("http.request.blocked", span=root_span)

    def test_flask_ipblock_match_403_json(self):
        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_GOOD_PATH)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/foobar", headers={"X-Real-Ip": _BLOCKED_IP})
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            assert root_span.get_tag(http.STATUS_CODE) == "403"
            assert root_span.get_tag(http.URL) == "http://localhost/foobar"
            assert root_span.get_tag(http.METHOD) == "GET"
            assert root_span.get_tag(http.USER_AGENT).startswith("werkzeug/")
            assert root_span.get_tag(SPAN_DATA_NAMES.RESPONSE_HEADERS_NO_COOKIES + ".content-type") == "text/json"

    def test_flask_ipblock_manually_json(self):
        # Most tests of flask blocking are in the test_flask_snapshot, this just
        # test a manual call to the blocking callable stored in _asm_request_context
        @self.app.route("/block")
        def test_route():
            from ddtrace.appsec._asm_request_context import block_request

            return block_request()

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_GOOD_PATH)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/block", headers={"X-REAL-IP": _ALLOWED_IP})
            # Should not block by IP but since the route is calling block_request it will be blocked
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                # not all flask versions have r.text
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON

            root_span = self.pop_spans()[0]
            assert root_span.get_tag(http.STATUS_CODE) == "403"
            assert root_span.get_tag(http.URL) == "http://localhost/block"
            assert root_span.get_tag(http.METHOD) == "GET"
            assert root_span.get_tag(http.USER_AGENT).startswith("werkzeug/")
            assert root_span.get_tag(SPAN_DATA_NAMES.RESPONSE_HEADERS_NO_COOKIES + ".content-type") == "text/json"

    def test_flask_userblock_json(self):
        @self.app.route("/checkuser/<user_id>")
        def test_route(user_id):
            from ddtrace import tracer

            block_request_if_user_blocked(tracer, user_id)
            return "Ok", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_GOOD_PATH)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/checkuser/%s" % _BLOCKED_USER)
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                # not all flask versions have r.text
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON

            root_span = self.pop_spans()[0]
            assert root_span.get_tag(http.STATUS_CODE) == "403"
            assert root_span.get_tag(http.URL) == "http://localhost/checkuser/%s" % _BLOCKED_USER
            assert root_span.get_tag(http.METHOD) == "GET"
            assert root_span.get_tag(http.USER_AGENT).startswith("werkzeug/")
            assert root_span.get_tag(SPAN_DATA_NAMES.RESPONSE_HEADERS_NO_COOKIES + ".content-type") == "text/json"

            resp = self.client.get("/checkuser/%s" % _BLOCKED_USER, headers={"Accept": "text/html"})
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                # not all flask versions have r.text
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_HTML

            resp = self.client.get("/checkuser/%s" % _ALLOWED_USER, headers={"Accept": "text/html"})
            assert resp.status_code == 200

    def test_request_suspicious_request_block_match_query_value(self):
        @self.app.route("/")
        def test_route():
            return "Ok", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB)):
            self._aux_appsec_prepare_tracer()

            resp = self.client.get("/index.html?toto=xtrace")
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-001"]
            assert root_span.get_tag(http.STATUS_CODE) == "403"
            assert root_span.get_tag(http.URL) == "http://localhost/index.html?toto=xtrace"
            assert root_span.get_tag(http.METHOD) == "GET"
            assert root_span.get_tag(http.USER_AGENT).startswith("werkzeug/")
            assert root_span.get_tag(SPAN_DATA_NAMES.RESPONSE_HEADERS_NO_COOKIES + ".content-type") == "text/json"

    def test_request_suspicious_request_block_match_uri(self):
        @self.app.route("/")
        def test_route():
            return "Ok", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB)):
            self._aux_appsec_prepare_tracer()

            resp = self.client.get("/.git")
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-002"]
            assert root_span.get_tag(http.STATUS_CODE) == "403"
            assert root_span.get_tag(http.URL) == "http://localhost/.git"
            assert root_span.get_tag(http.METHOD) == "GET"
            assert root_span.get_tag(http.USER_AGENT).startswith("werkzeug/")
            assert root_span.get_tag(SPAN_DATA_NAMES.RESPONSE_HEADERS_NO_COOKIES + ".content-type") == "text/json"

    def test_request_suspicious_request_block_match_body(self):
        @self.app.route("/")
        def test_route():
            return "Ok", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.post(
                "/index.html",
                data='{"key": "yqrweytqwreasldhkuqwgervflnmlnli"}',
                content_type="application/json",
            )
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-003"]

    def test_request_suspicious_request_block_match_header(self):
        @self.app.route("/")
        def test_route():
            return "Ok", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB)):
            self._aux_appsec_prepare_tracer()

            resp = self.client.get("/", headers={"User-Agent": "01972498723465"})
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-004"]

    def test_request_suspicious_request_block_match_response_code(self):
        @self.app.route("/")
        def test_route():
            return "Ok", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB_RESPONSE)):
            self._aux_appsec_prepare_tracer()

            resp = self.client.get("/do_not_exist.php")
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-005"]

    def test_request_suspicious_request_block_match_method(self):
        @self.app.route("/")
        def test_route():
            return "Ok", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB_METHOD)):
            self._aux_appsec_prepare_tracer()

            resp = self.client.get("/do_not_exist.php")
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-006"]

    def test_request_suspicious_request_block_match_cookies(self):
        @self.app.route("/")
        def test_route():
            return "Ok", 200

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB)):
            self._aux_appsec_prepare_tracer()
            self.client.set_cookie("localhost", "keyname", "jdfoSDGFkivRG_234")
            resp = self.client.get("/")
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-008"]

    def test_request_suspicious_request_block_match_path_params(self):
        @self.app.route("/params/<item>")
        def dynamic_url(item):
            return item

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/params/AiKfOeRcvG45")
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            flask_args = root_span.get_tag("flask.view_args.item")
            assert flask_args == "AiKfOeRcvG45"
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-007"]

    def test_request_suspicious_request_block_match_response_headers(self):
        @self.app.route("/response-header/")
        def specific_reponse():
            resp = Response("Foo bar baz", 200)
            resp.headers["Content-Disposition"] = 'attachment; filename="MagicKey_Al4h7iCFep9s1"'
            return resp

        with override_global_config(dict(_appsec_enabled=True)), override_env(dict(DD_APPSEC_RULES=RULES_SRB)):
            self._aux_appsec_prepare_tracer()
            resp = self.client.get("/response-header/")
            assert resp.status_code == 403
            if hasattr(resp, "text"):
                assert resp.text == constants.APPSEC_BLOCKED_RESPONSE_JSON
            else:
                assert resp.data == six.ensure_binary(constants.APPSEC_BLOCKED_RESPONSE_JSON)
            root_span = self.pop_spans()[0]
            loaded = json.loads(root_span.get_tag(APPSEC_JSON))
            assert [t["rule"]["id"] for t in loaded["triggers"]] == ["tst-037-009"]
