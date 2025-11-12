def newMetrics = """2025-11-12 23:59:10,4.586,2.172,0,3.516,2.153,13.675
"""

def file = new File('pipeline_metrics.csv')
file.append(newMetrics)
EOF