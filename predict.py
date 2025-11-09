import tensorflow as tf
import numpy as np
import argparse

# Load model
model = tf.keras.models.load_model("model.h5")

# Command-line args for test input
parser = argparse.ArgumentParser()
parser.add_argument("--duration", type=float, default=100.0)
parser.add_argument("--jobs", type=float, default=5.0)
parser.add_argument("--team_size", type=float, default=10.0)
args = parser.parse_args()

# Prepare input vector (adapt if your model expects different shape)
x = np.array([[args.duration, args.jobs, args.team_size]])
pred = model.predict(x)
print("Predicted Reward:", float(pred))
