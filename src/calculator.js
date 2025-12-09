// Simple calculator module with intentional bug
// This file has a syntax error that the AI should detect and fix

function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b
}

// Export functions - intentional syntax error: missing semicolon and typo
module.exports = {
    add,
    subtrac,  // typo: should be "subtract"
    multiply,
    divide
};
