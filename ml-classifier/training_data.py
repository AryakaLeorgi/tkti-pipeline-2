"""
Training data for error classification model.
Contains sample error logs for different categories.
EXPANDED version with more samples for better accuracy.
"""

TRAINING_DATA = [
    # ===== SYNTAX ERRORS (auto-fixable) =====
    {"text": "SyntaxError: Unexpected token '}' at line 45", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "error: expected ';' before '}' token", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "ParseError: Missing closing bracket", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "SyntaxError: invalid syntax at line 23", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "Unexpected end of JSON input", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "error TS2304: Cannot find name 'foo'", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "ESLint: Parsing error unexpected token", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "SyntaxError: Unexpected identifier", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "SyntaxError: Unexpected string", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "SyntaxError: missing ) after argument list", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "SyntaxError: missing : after property id", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "SyntaxError: Unexpected token ILLEGAL", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "error: expected expression before ','", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "IndentationError: expected an indented block", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "IndentationError: unexpected indent", "category": "syntax_error", "fixable": True, "priority": "high"},
    
    # ===== RUNTIME ERRORS (auto-fixable) =====
    {"text": "TypeError: Cannot read property 'length' of undefined", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "ReferenceError: myVariable is not defined", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "TypeError: .tset is not a function", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "TypeError: .test is not a function", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "TypeError: null is not an object", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "NameError: name 'undefined_var' is not defined", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "AttributeError: 'NoneType' object has no attribute", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "Uncaught TypeError: x.map is not a function", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "Error: Cannot call method on undefined", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "TypeError: undefined is not a function", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "TypeError: Cannot read properties of null", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "ReferenceError: x is not defined at line 15", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "TypeError: Cannot convert undefined to object", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "TypeError: object is not iterable", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "ZeroDivisionError: division by zero", "category": "runtime_error", "fixable": True, "priority": "high"},
    
    # ===== TEST FAILURES (auto-fixable) =====
    {"text": "AssertionError: Expected true but got false", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "FAIL: test_user_login - assertion failed", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "Test failed: expected 5 but received 4", "category": "test_failure", "fixable": True, "priority": "medium"},
    {"text": "1 failing test in auth.test.js", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "jest test suite failed with 2 errors", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "Expected: 200, Received: 404", "category": "test_failure", "fixable": True, "priority": "medium"},
    {"text": "Error: Timeout - Async callback not invoked within 5000ms", "category": "test_failure", "fixable": True, "priority": "medium"},
    {"text": "AssertionError: expected 'hello' to equal 'world'", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "FAILED test_calculate_sum - AssertionError", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "expect(received).toBe(expected) // Object.is equality", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "✗ should return user data - Expected object to have property", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "Error: expect(jest.fn()).toHaveBeenCalled()", "category": "test_failure", "fixable": True, "priority": "medium"},
    {"text": "AssertionError [ERR_ASSERTION]: Input A expected to strictly equal input B", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "TypeError: /[A-Z]/.tset is not a function at UserAuth.validatePassword", "category": "test_failure", "fixable": True, "priority": "high"},
    {"text": "Ran 5 tests, 1 failed, 4 passed", "category": "test_failure", "fixable": True, "priority": "high"},
    
    # ===== DEPENDENCY ERRORS (not auto-fixable) =====
    {"text": "npm ERR! 404 Not Found - package-name@1.0.0", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "ERESOLVE unable to resolve dependency tree", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "pip install failed: No matching distribution found", "category": "dependency_error", "fixable": False, "priority": "medium"},
    {"text": "npm WARN deprecated package has known vulnerabilities", "category": "dependency_error", "fixable": False, "priority": "low"},
    {"text": "ModuleNotFoundError: No module named 'missing_package'", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "gyp ERR! build error during npm install", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "Could not resolve dependency: peer react@18 from package", "category": "dependency_error", "fixable": False, "priority": "medium"},
    {"text": "npm ERR! code ENOENT - missing package.json", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "npm WARN peer dep missing: typescript@>=4.0", "category": "dependency_error", "fixable": False, "priority": "medium"},
    {"text": "Cannot find module 'express' from 'server.js'", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "ImportError: cannot import name 'Flask' from 'flask'", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "npm ERR! peer dep missing: webpack", "category": "dependency_error", "fixable": False, "priority": "medium"},
    {"text": "Package 'libssl-dev' has no installation candidate", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "npm ERR! code E401 Unauthorized - authentication required", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "Error: Cannot find module '@babel/core'", "category": "dependency_error", "fixable": False, "priority": "high"},
    
    # ===== CONFIG ERRORS (not auto-fixable) =====
    {"text": "Error: Missing required environment variable DATABASE_URL", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "ConfigurationError: Invalid config file format", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "Error: PORT is not defined in .env file", "category": "config_error", "fixable": False, "priority": "medium"},
    {"text": "ENOENT: no such file or directory, open 'config.json'", "category": "config_error", "fixable": False, "priority": "medium"},
    {"text": "Error reading config: YAML parse error", "category": "config_error", "fixable": False, "priority": "medium"},
    {"text": "Invalid credentials in settings.json", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "Missing API_KEY in environment variables", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "Error: SECRET_KEY must be set", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "Invalid JSON in configuration file", "category": "config_error", "fixable": False, "priority": "medium"},
    {"text": "Config validation failed: 'port' must be a number", "category": "config_error", "fixable": False, "priority": "medium"},
    {"text": "Error: Required config key 'redis.host' not found", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "FATAL: password authentication failed for user", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "Error: JENKINS_HOME not set", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "Cannot read property 'apiKey' of undefined in config", "category": "config_error", "fixable": False, "priority": "high"},
    {"text": "Environment variable AWS_ACCESS_KEY_ID not set", "category": "config_error", "fixable": False, "priority": "high"},
    
    # ===== NETWORK ERRORS (not auto-fixable) =====
    {"text": "ETIMEDOUT: connection timed out to api.example.com", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "ECONNREFUSED: Connection refused at localhost:5432", "category": "network_error", "fixable": False, "priority": "high"},
    {"text": "fetch failed: NetworkError when attempting to fetch resource", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "Error: getaddrinfo ENOTFOUND unknown-host.com", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "SSLError: certificate verify failed", "category": "network_error", "fixable": False, "priority": "high"},
    {"text": "EHOSTUNREACH: No route to host", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "socket hang up during HTTP request", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "Error: connect ECONNRESET 192.168.1.1:443", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "RequestError: Error: read ECONNRESET", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "Error: ENOTFOUND: getaddrinfo failed for hostname", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "504 Gateway Time-out nginx", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "502 Bad Gateway - upstream prematurely closed connection", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "Error: self signed certificate in certificate chain", "category": "network_error", "fixable": False, "priority": "high"},
    {"text": "DNS lookup failed: SERVFAIL", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "net::ERR_CONNECTION_REFUSED", "category": "network_error", "fixable": False, "priority": "medium"},
]

def get_all_training_data():
    """Return all training data."""
    return TRAINING_DATA

def get_category_counts():
    """Return count of samples per category."""
    counts = {}
    for d in TRAINING_DATA:
        cat = d["category"]
        counts[cat] = counts.get(cat, 0) + 1
    return counts
