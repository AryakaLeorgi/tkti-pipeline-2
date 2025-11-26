class StageSegmenter:
    def segment(self, log_text: str):
        stages = {
            "build": [],
            "test": [],
            "deploy": []
        }

        current = None
        for line in log_text.split("\n"):
            if "BUILD STAGE" in line:
                current = "build"
            elif "TEST STAGE" in line:
                current = "test"
            elif "DEPLOY STAGE" in line:
                current = "deploy"

            if current:
                stages[current].append(line)

        return stages
