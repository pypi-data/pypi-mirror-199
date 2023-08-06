from ctranslate2 import Translator
from transformers import MT5TokenizerFast
import os
from .rule_filter import RuleFilter
from .constants import SUPPORTED_LANGS, DetectionResults


# search for model folder called "models"that is at the level above this file (this is a module)
relative_file_location = os.path.join(os.path.dirname(__file__), "..", "ct2_model")

model_hf_name = "AnonymousArt/mt5_language_detection"
quantization = "int8"

if not os.path.exists(relative_file_location) or not os.path.isdir(relative_file_location):
    print("--- Could not find models folder at {} ---".format(relative_file_location))
    print("--- Attempting to convert model from huggingface ---")

    os.system(f"ct2-transformers-converter --model {model_hf_name} --quantization {quantization} --output {relative_file_location} --force")

    if os.path.exists(relative_file_location) and os.path.isdir(relative_file_location):
        print("--- Model successfully converted ---")
    else:
        raise FileNotFoundError("|| Could not find models folder at {} and could not convert model from huggingface ||\n|| Please ensure that ct2-transformers-converter from CTranslate2 is in your path ||".format(relative_file_location))

class DetectionModel:
    def __init__ (self, device="cpu", inter_threads = 3, intra_threads = 1, compute_type="auto") -> None:
        self.model = Translator(relative_file_location, device=device, inter_threads=inter_threads, intra_threads=intra_threads, compute_type=compute_type)
        self.tokenizer = MT5TokenizerFast.from_pretrained(relative_file_location + "/tokenizer")
        self.rule_filter: RuleFilter = RuleFilter(restrict_to_langs=SUPPORTED_LANGS)
        self.supported_langs: list = SUPPORTED_LANGS

    @property
    def rule_filter (self):
        return self._rule_filter

    def tokenize (self, items):
        input_ids =  self.tokenizer(items, return_tensors="pt", padding=False, truncation=True, max_length=2048)["input_ids"]
        input_ids = [self.tokenizer.convert_ids_to_tokens(x) for x in input_ids]
        return input_ids

    def _suppress_langs_ (self, eligible_langs):
        """Method which takes a list of eligible languages and returns a list of suppressed languages 
        This assumes the tokenizer has a token for each lang code, which is the case for the model used here"""
        return [lang for lang in self.supported_langs if lang not in eligible_langs]

    def decode_results (self, results):
        return [self.tokenizer.decode(self.tokenizer.convert_tokens_to_ids(result.hypotheses[0]), skip_special_tokens=True) for result in results]

    def detect (self, texts: list[str], batch_size: int=4096) -> list[DetectionResults]:
        if type(texts) == str:
            texts: list[str] = [texts]

        if type(texts) != list:
            texts: list[str] = list(texts)

        eligible_langs = [self.rule_filter.filter(text) for text in texts]
        

        binary_detection_decision = [len(eligible_langs[i]) > 1 and len(eligible_langs[i]) != 0 for i in range(len(eligible_langs))]
        suppressed_langs = [self._suppress_langs_(eligible_langs[i]) if binary_detection_decision[i] else [] for i in range(len(eligible_langs))]

        # if binary_detection_decision is True, then pass in text to this new array, else pass in empty string
        tokenized_text = self.tokenize([texts[i] if binary_detection_decision[i] else "" for i in range(len(texts))])

        results = self.model.translate_batch(tokenized_text, batch_size=batch_size, beam_size=1, num_hypotheses=1, suppress_sequences=suppressed_langs, batch_type='tokens')

        decoded_results = self.decode_results(results)


        ordered_return_detections = []
        for i in range(len(results)):
            detected_lang = None
            current_text = texts[i]
            if not binary_detection_decision[i]:
                detected_lang = eligible_langs[i][0]
                ordered_return_detections.append(DetectionResults(current_text, detected_lang))
                continue

            detected_lang = decoded_results[i]
            ordered_return_detections.append(DetectionResults(current_text, detected_lang))