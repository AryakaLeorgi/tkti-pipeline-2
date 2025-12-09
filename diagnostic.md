# Build Error

========================================
Running UserAuth Unit Tests
========================================

✅ PASS: Valid email should pass validation
✅ PASS: Invalid email should fail validation
/var/lib/jenkins/workspace/tkti/src/auth.js:35
        if (!/[A-Z]/.tset(password)) {
                     ^

TypeError: /[A-Z]/.tset is not a function
    at UserAuth.validatePassword (/var/lib/jenkins/workspace/tkti/src/auth.js:35:22)
    at runTests (/var/lib/jenkins/workspace/tkti/src/test.js:41:32)
    at Object.<anonymous> (/var/lib/jenkins/workspace/tkti/src/test.js:97:1)
    at Module._compile (node:internal/modules/cjs/loader:1356:14)
    at Module._extensions..js (node:internal/modules/cjs/loader:1414:10)
    at Module.load (node:internal/modules/cjs/loader:1197:32)
    at Module._load (node:internal/modules/cjs/loader:1013:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:128:12)
    at node:internal/main/run_main_module:28:49

Node.js v18.19.1

## Source Files


=== SOURCE FILE: src/auth.js ===
/**
 * User Authentication Module
 * Handles user login, registration, and validation
 */

class UserAuth {
    constructor() {
        this.users = [];
    }

    /**
     * Validate email format
     * @param {string} email 
     * @returns {boolean}
     */
    validateEmail(email) {
        // Bug: regex is incorrect, missing escape for dot
        const emailRegex = /^[^\s@]+@[^\s@]+.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Validate password strength
     * @param {string} password 
     * @returns {object} validation result
     */
    validatePassword(password) {
        const errors = [];

        if (password.length < 8) {
            errors.push("Password must be at least 8 characters");
        }

        // Bug: typo in method name - should be "test" not "tset"
        if (!/[A-Z]/.tset(password)) {
            errors.push("Password must contain uppercase letter");
        }

        if (!/[0-9]/.test(password)) {
            errors.push("Password must contain a number");
        }

        return {
            valid: errors.length === 0,
            errors: errors
        };
    }

    /**
     * Register a new user
     * @param {string} email 
     * @param {string} password 
     * @returns {object} registration result
     */
    register(email, password) {
        if (!this.validateEmail(email)) {
            return { success: false, error: "Invalid email format" };
        }

        const passwordValidation = this.validatePassword(password);
        if (!passwordValidation.valid) {
            return { success: false, error: passwordValidation.errors[0] };
        }

        // Check if user already exists
        if (this.users.find(u => u.email === email)) {
            return { success: false, error: "User already exists" };
        }

        this.users.push({ email, password });
        return { success: true, message: "User registered successfully" };
    }

    /**
     * Login user
     * @param {string} email 
     * @param {string} password 
     * @returns {object} login result
     */
    login(email, password) {
        const user = this.users.find(u => u.email === email && u.password === password);

        if (user) {
            return { success: true, message: "Login successful" };
        }

        return { success: false, error: "Invalid credentials" };
    }
}

module.exports = UserAuth;


=== SOURCE FILE: src/test.js ===
/**
 * Unit Tests for UserAuth Module
 */

const UserAuth = require('./auth');

let auth;
let passed = 0;
let failed = 0;

function assert(condition, testName) {
    if (condition) {
        console.log(`✅ PASS: ${testName}`);
        passed++;
    } else {
        console.log(`❌ FAIL: ${testName}`);
        failed++;
    }
}

function runTests() {
    console.log("========================================");
    console.log("Running UserAuth Unit Tests");
    console.log("========================================\n");

    auth = new UserAuth();

    // Test 1: Valid email validation
    assert(
        auth.validateEmail("test@example.com") === true,
        "Valid email should pass validation"
    );

    // Test 2: Invalid email validation
    assert(
        auth.validateEmail("invalid-email") === false,
        "Invalid email should fail validation"
    );

    // Test 3: Password validation - too short
    const shortPassword = auth.validatePassword("Ab1");
    assert(
        shortPassword.valid === false,
        "Short password should fail validation"
    );

    // Test 4: Password validation - valid password
    const validPassword = auth.validatePassword("SecurePass123");
    assert(
        validPassword.valid === true,
        "Valid password should pass validation"
    );

    // Test 5: Register new user
    const registerResult = auth.register("newuser@test.com", "SecurePass123");
    assert(
        registerResult.success === true,
        "New user registration should succeed"
    );

    // Test 6: Duplicate registration should fail
    const duplicateResult = auth.register("newuser@test.com", "AnotherPass456");
    assert(
        duplicateResult.success === false,
        "Duplicate registration should fail"
    );

    // Test 7: Login with valid credentials
    const loginResult = auth.login("newuser@test.com", "SecurePass123");
    assert(
        loginResult.success === true,
        "Login with valid credentials should succeed"
    );

    // Test 8: Login with invalid credentials
    const invalidLogin = auth.login("newuser@test.com", "wrongpassword");
    assert(
        invalidLogin.success === false,
        "Login with invalid credentials should fail"
    );

    // Summary
    console.log("\n========================================");
    console.log(`Test Results: ${passed} passed, ${failed} failed`);
    console.log("========================================");

    if (failed > 0) {
        console.error("\n⚠️  Some tests failed!");
        process.exit(1);
    } else {
        console.log("\n🎉 All tests passed!");
        process.exit(0);
    }
}

// Run tests
runTests();
