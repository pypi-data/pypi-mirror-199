from polyglotiq import DetectionModel, RuleFilter


detector = DetectionModel("cuda")

print(detector.detect("Hello, world!"))