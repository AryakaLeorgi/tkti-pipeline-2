import json
import os

ANOMALY_RESULT_PATH = "ml/anomaly_output.json"
CI_ERROR_LOG = "ci/error_log.json"


def load_json_safe(path):
    """Load JSON file, return default if missing."""
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def analyze_root_cause(anomaly_data, ci_error_data):
    explanations = []
    solutions = []

    # -----------------------------
    # Anomaly model results
    # -----------------------------
    anomaly_flag = anomaly_data.get("anomaly", False)
    anomaly_reason = anomaly_data.get("reason", "None")
    anomaly_inputs = anomaly_data.get("inputs", {})

    if anomaly_flag:
        explanations.append(f"⚠ Model mendeteksi ANOMALI: {anomaly_reason}")

        # Check timing anomalies
        build = anomaly_inputs.get("BuildTime", 0)
        test = anomaly_inputs.get("TestTime", 0)
        deploy = anomaly_inputs.get("DeployTime", 0)

        if build > 8:
            explanations.append("• Build time terlalu lama (di atas 8 detik).")
            solutions.append("→ Periksa dependency yang berat atau modul yang lambat.")

        if test > 7:
            explanations.append("• Test time sangat lama (di atas 7 detik).")
            solutions.append("→ Mungkin unit test tidak efisien atau infinite loop kecil.")

        if deploy > 7:
            explanations.append("• Deploy time abnormal (di atas 7 detik).")
            solutions.append("→ Periksa konfigurasi deployment atau penarikan image docker.")

    else:
        explanations.append("Tidak ada anomaly terdeteksi oleh model.")

    # -----------------------------
    # CI Simulation Errors
    # -----------------------------
    simulated_fail = ci_error_data.get("ci_failure", "None")

    if simulated_fail != "None":
        explanations.append(f"⚠ CI mensimulasikan error: {simulated_fail}")

        if simulated_fail == "MissingDependency":
            solutions.append("→ Tambahkan dependency yang hilang di requirements.txt.")
        elif simulated_fail == "PackageVersionConflict":
            solutions.append("→ Periksa versi paket dan lakukan pinning versi.")
        elif simulated_fail == "NetworkTimeout":
            solutions.append("→ Coba ulangi request dan gunakan retry logic.")
        elif simulated_fail == "TestAssertionError":
            solutions.append("→ Perbaiki unit test yang gagal.")
        elif simulated_fail == "ContainerBuildFailure":
            solutions.append("→ Perbaiki Dockerfile atau layer yang conflict.")
        elif simulated_fail == "KubernetesConfigInvalid":
            solutions.append("→ Validasi ulang YAML deploy dan environment variables.")
        elif simulated_fail == "SecurityVulnerabilityFound":
            solutions.append("→ Update dependency yang rentan atau tambahkan patch keamanan.")

    # -----------------------------
    # Final Output
    # -----------------------------
    return {
        "explanations": explanations,
        "solutions": solutions
    }


def save_output(result):
    os.makedirs("ml", exist_ok=True)
    out_path = "ml/root_cause_output.json"

    with open(out_path, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[INFO] Root cause analysis saved to {out_path}")

    # Also print summary to Jenkins console
    print("\n======= ROOT CAUSE ANALYSIS =======")
    for e in result["explanations"]:
        print(e)
    print("\n===== RECOMMENDED FIXES =====")
    for s in result["solutions"]:
        print(s)


def main():
    anomaly_data = load_json_safe(ANOMALY_RESULT_PATH)
    ci_data = load_json_safe(CI_ERROR_LOG)

    result = analyze_root_cause(anomaly_data, ci_data)
    save_output(result)


if __name__ == "__main__":
    main()
