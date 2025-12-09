"""
Training data for error classification model.
Contains sample error logs for different categories.
"""

TRAINING_DATA = [
    # ===== SYNTAX ERRORS (auto-fixable) =====
    {
        "text": "SyntaxError: Unexpected token '}' at line 45",
        "category": "syntax_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "error: expected ';' before '}' token",
        "category": "syntax_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "ParseError: Missing closing bracket",
        "category": "syntax_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "SyntaxError: invalid syntax at line 23",
        "category": "syntax_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "Unexpected end of JSON input",
        "category": "syntax_error",
        "fixable": True,
        "priority": "high"
    },
    
    # ===== RUNTIME ERRORS (auto-fixable) =====
    {
        "text": "TypeError: Cannot read property 'length' of undefined",
        "category": "runtime_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "ReferenceError: myVariable is not defined",
        "category": "runtime_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "TypeError: .tset is not a function",
        "category": "runtime_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "TypeError: null is not an object",
        "category": "runtime_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "NameError: name 'undefined_var' is not defined",
        "category": "runtime_error",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "AttributeError: 'NoneType' object has no attribute",
        "category": "runtime_error",
        "fixable": True,
        "priority": "high"
    },
    
    # ===== TEST FAILURES (auto-fixable) =====
    {
        "text": "AssertionError: Expected true but got false",
        "category": "test_failure",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "FAIL: test_user_login - assertion failed",
        "category": "test_failure",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "Test failed: expected 5 but received 4",
        "category": "test_failure",
        "fixable": True,
        "priority": "medium"
    },
    {
        "text": "1 failing test in auth.test.js",
        "category": "test_failure",
        "fixable": True,
        "priority": "high"
    },
    {
        "text": "jest test suite failed with 2 errors",
        "category": "test_failure",
        "fixable": True,
        "priority": "high"
    },
    
    # ===== DEPENDENCY ERRORS (not auto-fixable) =====
    {
        "text": "npm ERR! 404 Not Found - package-name@1.0.0",
        "category": "dependency_error",
        "fixable": False,
        "priority": "high"
    },
    {
        "text": "ERESOLVE unable to resolve dependency tree",
        "category": "dependency_error",
        "fixable": False,
        "priority": "high"
    },
    {
        "text": "pip install failed: No matching distribution found",
        "category": "dependency_error",
        "fixable": False,
        "priority": "medium"
    },
    {
        "text": "npm WARN deprecated package has known vulnerabilities",
        "category": "dependency_error",
        "fixable": False,
        "priority": "low"
    },
    {
        "text": "ModuleNotFoundError: No module named 'missing_package'",
        "category": "dependency_error",
        "fixable": False,
        "priority": "high"
    },
    
    # ===== CONFIG ERRORS (not auto-fixable) =====
    {
        "text": "Error: Missing required environment variable DATABASE_URL",
        "category": "config_error",
        "fixable": False,
        "priority": "high"
    },
    {
        "text": "ConfigurationError: Invalid config file format",
        "category": "config_error",
        "fixable": False,
        "priority": "high"
    },
    {
        "text": "Error: PORT is not defined in .env file",
        "category": "config_error",
        "fixable": False,
        "priority": "medium"
    },
    {
        "text": "ENOENT: no such file or directory, open 'config.json'",
        "category": "config_error",
        "fixable": False,
        "priority": "medium"
    },
    
    # ===== NETWORK ERRORS (not auto-fixable) =====
    {
        "text": "ETIMEDOUT: connection timed out to api.example.com",
        "category": "network_error",
        "fixable": False,
        "priority": "medium"
    },
    {
        "text": "ECONNREFUSED: Connection refused at localhost:5432",
        "category": "network_error",
        "fixable": False,
        "priority": "high"
    },
    {
        "text": "fetch failed: NetworkError when attempting to fetch resource",
        "category": "network_error",
        "fixable": False,
        "priority": "medium"
    },
    {
        "text": "Error: getaddrinfo ENOTFOUND unknown-host.com",
        "category": "network_error",
        "fixable": False,
        "priority": "medium"
    },
    {
        "text": "SSLError: certificate verify failed",
        "category": "network_error",
        "fixable": False,
        "priority": "high"
    },
]

# Additional augmented data (variations)
AUGMENTED_DATA = [
    # More syntax errors
    {"text": "error TS2304: Cannot find name 'foo'", "category": "syntax_error", "fixable": True, "priority": "high"},
    {"text": "ESLint: Parsing error unexpected token", "category": "syntax_error", "fixable": True, "priority": "high"},
    
    # More runtime errors  
    {"text": "Uncaught TypeError: x.map is not a function", "category": "runtime_error", "fixable": True, "priority": "high"},
    {"text": "Error: Cannot call method on undefined", "category": "runtime_error", "fixable": True, "priority": "high"},
    
    # More test failures
    {"text": "Expected: 200, Received: 404", "category": "test_failure", "fixable": True, "priority": "medium"},
    {"text": "Error: Timeout - Async callback not invoked within 5000ms", "category": "test_failure", "fixable": True, "priority": "medium"},
    
    # More dependency errors
    {"text": "gyp ERR! build error during npm install", "category": "dependency_error", "fixable": False, "priority": "high"},
    {"text": "Could not resolve dependency: peer react@18 from package", "category": "dependency_error", "fixable": False, "priority": "medium"},
    
    # More config errors
    {"text": "Error reading config: YAML parse error", "category": "config_error", "fixable": False, "priority": "medium"},
    {"text": "Invalid credentials in settings.json", "category": "config_error", "fixable": False, "priority": "high"},
    
    # More network errors
    {"text": "EHOSTUNREACH: No route to host", "category": "network_error", "fixable": False, "priority": "medium"},
    {"text": "socket hang up during HTTP request", "category": "network_error", "fixable": False, "priority": "medium"},
]

def get_all_training_data():
    """Return combined training data."""
    return TRAINING_DATA + AUGMENTED_DATA
