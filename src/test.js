const calc = require('./calculator');

// Test the calculator
console.log("Testing Calculator...");

try {
    console.log("2 + 3 =", calc.add(2, 3));
    console.log("5 - 2 =", calc.subtract(5, 2));  // This will fail because of typo
    console.log("4 * 3 =", calc.multiply(4, 3));
    console.log("10 / 2 =", calc.divide(10, 2));
    console.log("All tests passed!");
} catch (error) {
    console.error("Test failed:", error.message);
    process.exit(1);
}
