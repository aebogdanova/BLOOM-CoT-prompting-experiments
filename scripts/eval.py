import re
from collections import Counter

KEY_WORDS = "answer is "

def _is_float(string: str):
  try:
    float(string)
    return True
  except:
    return False

def extract_number(answer: str):
  if answer.rfind(KEY_WORDS) >= 0:
    answer = answer[answer.rfind(KEY_WORDS) + len(KEY_WORDS):len(answer)].strip()
    for symbol in ["$", "€", "%", ","]:
      answer = answer.replace(symbol, "")
    if re.match("\d*.?\d+", answer):
      answer = re.match("\d*.?\d+", answer)[0]
      answer = answer.replace(" ", "")
      return answer
    else:
      return ""
  else:
    return ""

def aggregate_answer(ans_list: list):
  float_list = []
  str_list = []
  for answer in ans_list:
    if _is_float(answer):
      float_list.append(float(answer))
    else:
      str_list.append(answer)
  if float_list:
    return Counter(float_list).most_common()[0][0]
  else:
    return Counter(str_list).most_common()[0][0]
      
def evaluate_acc(pred_list: list, target_list: list):
  assert len(pred_list) == len(target_list)
  total = len(pred_list)
  correct = 0
  for pred, target in zip(pred_list, target_list):
    target = target.replace(",", "")
    if _is_float(target) and _is_float(pred):
      if abs(float(target) - float(pred)) <= 1e-5:
        correct += 1
    elif str(pred) == str(target):
      correct += 1
  print(f"Total examples: {total}\tCorrect examples: {correct}\tAccuracy score: {correct / total}")