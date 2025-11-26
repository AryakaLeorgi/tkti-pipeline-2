import xml.etree.ElementTree as ET
import networkx as nx

class AntParser:
    def __init__(self, path="build.xml"):
        self.path = path

    def parse(self):
        tree = ET.parse(self.path)
        root = tree.getroot()

        g = nx.DiGraph()
        features = {
            "target_count": 0,
            "task_count": 0,
            "uses_parallel": False,
            "uses_junit": False,
            "property_count": 0,
            "javac_flags": []
        }

        for target in root.findall("target"):
            tname = target.get("name", "")
            g.add_node(tname)
            features["target_count"] += 1

            for task in target:
                ttype = task.tag.lower()
                features["task_count"] += 1

                if ttype == "parallel":
                    features["uses_parallel"] = True
                if ttype == "junit":
                    features["uses_junit"] = True
                if ttype == "javac":
                    if task.get("debug"):
                        features["javac_flags"].append("debug")
                if ttype == "property":
                    features["property_count"] += 1

                # link dependencies
                depends = target.get("depends")
                if depends:
                    for d in depends.split(","):
                        g.add_edge(d.strip(), tname)

        return g, features
