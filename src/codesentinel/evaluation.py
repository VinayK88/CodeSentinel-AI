from collections import Counter

def evaluate(predicted_rule_ids, expected_rule_ids):
    pred=set(predicted_rule_ids); truth=set(expected_rule_ids)
    tp=len(pred & truth); fp=len(pred-truth); fn=len(truth-pred)
    precision=tp/(tp+fp) if tp+fp else 1.0
    recall=tp/(tp+fn) if tp+fn else 1.0
    return {"tp":tp,"fp":fp,"fn":fn,"precision":round(precision,3),"recall":round(recall,3)}
