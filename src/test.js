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
