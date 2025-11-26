// append_metrics.groovy
import java.nio.file.*

// Define the metrics file path
def metricsFile = new File("metrics.csv")

// Example data (you can modify or generate these dynamically)
def newMetrics = "544,2.334,0,3.517,2.142,12.898"

// If the file doesn't exist, create it and add headers
if (!metricsFile.exists()) {
    metricsFile.write("build_id,test_time,failures,build_time,deploy_time,total_time\n")
}

// Append new metrics to the CSV
metricsFile.append(newMetrics + "\n")

println "✅ Metrics appended successfully!"
