from models.schemas import RecommendationResult

class FixGenerator:

    def generate_fix(self, log: str) -> RecommendationResult:

        if "NullPointerException" in log:
            return RecommendationResult(
                fix_description="Periksa variable yang null dan tambahkan null-check.",
                updated_code_snippet="""
if (user == null) {
    throw new IllegalArgumentException("User cannot be null");
}
""",
                severity="high"
            )

        if "ImagePullBackOff" in log:
            return RecommendationResult(
                fix_description="Pastikan Docker image tersedia dan kredensial registry benar.",
                updated_code_snippet="""
imagePullSecrets:
  - name: regcred
""",
                severity="medium"
            )

        if "CVE-" in log:
            return RecommendationResult(
                fix_description="Update library ke versi patch yang aman.",
                updated_code_snippet="implementation 'org.apache.logging.log4j:log4j-core:2.17.1'",
                severity="critical"
            )

        return RecommendationResult(
            fix_description="Tidak ditemukan fix otomatis.",
            updated_code_snippet=None,
            severity="low"
        )
