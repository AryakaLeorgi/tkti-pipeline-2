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
        if (!/[A-Z]/.test(password)) {
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
