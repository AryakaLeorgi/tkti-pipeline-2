// append_metrics.groovy
// This script appends the latest pipeline metrics into a CSV file for analysis.

def metricsFile = new File("pipeline_metrics.csv")

if (!metricsFile.exists()) {
    metricsFile.write("build_number,stage,stage_duration,tests_passed,tests_failed,build_duration,total_duration\n")
}

// For demo, generate fake metrics or read from existing stage output
def buildNumber = System.getenv("BUILD_NUMBER") ?: "local"
def totalDuration = (Math.random() * 10 + 5).round(3)
def buildDuration = (Math.random() * 3 + 1).round(3)
def testPassed = (Math.random() * 10).toInteger()
def testFailed = (Math.random() * 2).toInteger()

metricsFile.append("${buildNumber},Build,${buildDuration},${testPassed},${testFailed},${buildDuration},${totalDuration}\n")

println "✅ Metrics appended successfully!"
