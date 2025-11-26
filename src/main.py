from ant_parser.parser import AntParser
from ml.utils import tokenize, graph_to_vector
from ml.infer import infer

def run():
    parser = AntParser("build.xml")
    g, feats = parser.parse()

    text = input("Describe the issue: ")
    text_vec = tokenize(text)
    graph_vec = graph_to_vector(feats)

    category, confidence = infer(text_vec, graph_vec)

    print("Diagnosis:", category)
    print("Confidence:", confidence)

if __name__ == "__main__":
    run()
