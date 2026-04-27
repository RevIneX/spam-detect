import requests
import json
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, roc_auc_score
from tabulate import tabulate

MESSAGES = [
    # Спам [1]
    "URGENT: Your account access is limited!", "CONGRATULATIONS! You won a gift card!",
    "Lose 20lbs in 2 weeks! Click here", "Cheap Medications! Buy Viagra online",
    "Double your BTC in 24h! Send now", "You have been selected for a free iPhone",
    "Your PayPal account has been suspended", "Earn 5000$ daily working from home",
    "Lowest mortgage rates ever", "Your Netflix subscription expired",
    "Verify your identity now", "You are our 1,000,000th visitor",
    "Get rich fast with Bitcoin", "Weight loss miracle pill – order now",
    "Your Apple ID has been locked", "Free vacation package waiting for you",
    "Last chance to claim your prize", "Work from home, earn 10k per month",
    "Your credit card is blocked", "Click this link to claim your reward",
    "Your account will be closed today", "Meet singles in your area",
    "Low interest loan approved", "Your invoice is attached (scam)",
    "African prince needs your help", "You won a brand new car",
    "Urgent! Your bank account hacked", "Tax refund waiting for you",
    "Increase your Instagram followers fast", "One weird trick to lose weight",
    "You have a secret admirer", "Your package delivery failed",
    "Timeshare opportunity – act now", "Investment guaranteed return",

    # Хам [0]
    "Meeting at 5pm today in the office", "I love you so much, honey",
    "Can you send the project file?", "Happy birthday, have a great one!",
    "I am running 5 minutes late", "Dinner tonight at the new Italian place?",
    "Thanks for the help yesterday", "Did you see the latest show? It was crazy",
    "Your password was changed successfully", "Pick up some milk on your way home",
    "The server maintenance is done", "Please review the PR and merge it",
    "Can we hop on a quick call?", "I miss you, let's meet soon",
    "Docker cache is a lifesaver for SRE", "Let's catch up over coffee",
    "What's the weather like today?", "I attached the report for your review",
    "Great job on the presentation", "Don't forget to submit your timesheet",
    "How was your weekend?", "I'm thinking of ordering pizza for lunch",
    "The deposit has been made", "Congratulations on your promotion",
    "You look nice today", "Reminder: team meeting at 3pm",
    "Here is the link to the design doc", "Thanks for your patience",
    "The build passed successfully", "Let me know if you need anything",
    "I appreciate your feedback", "Have a nice day",
    "Can you review the documentation?", "See you at the conference",
]

while len(MESSAGES) < 100:
    MESSAGES.append("Additional test message")
Y_TRUE = [1]*50 + [0]*50
MESSAGES = MESSAGES[:100]
Y_TRUE = Y_TRUE[:len(MESSAGES)]
while len(Y_TRUE) < len(MESSAGES):
    Y_TRUE.append(0 if len(Y_TRUE) >= 50 else 1)

Y_PRED = []
Y_SCORES = []
TABLE_DATA = []

print("ТЕСТИРОВАНИЕ НЕЙРОНКИ (без цветов, для CI)")
print("="*80)

for MSG, GT in zip(MESSAGES, Y_TRUE):
    try:
        R = requests.post("http://localhost:1001/analyze", json={"text": MSG}, timeout=30)
        RES = R.json()
        PRED = 1 if RES["result"] == "SPAM" else 0
        SCORE = RES["score"]
    except Exception as e:
        PRED = 0
        SCORE = 0.0
        RES = {"error": str(e)}

    Y_PRED.append(PRED)
    Y_SCORES.append(SCORE if PRED == 1 else 1 - SCORE)

    STATUS = "СОВПАДЕНИЕ" if PRED == GT else "НЕСООТВЕТСТВИЕ"
    PRED_STR = "СПАМ" if PRED == 1 else "ХАМ"
    GT_STR = "СПАМ" if GT == 1 else "ХАМ"
    MSG_STR = MSG[:30].upper()
    TABLE_DATA.append([MSG_STR, GT_STR, PRED_STR, f"{SCORE:.4f}", STATUS])

HEADERS = ["СООБЩЕНИЕ", "ЭТАЛОН", "ПРЕДСКАЗАНИЕ", "СКОР", "СТАТУС"]
print(tabulate(TABLE_DATA, headers=HEADERS, tablefmt="grid"))

P = precision_score(Y_TRUE, Y_PRED, zero_division=0)
R = recall_score(Y_TRUE, Y_PRED, zero_division=0)
F = f1_score(Y_TRUE, Y_PRED, zero_division=0)
ACC = accuracy_score(Y_TRUE, Y_PRED)
ROC = roc_auc_score(Y_TRUE, Y_SCORES)

print(f"\n{'#'*50}")
print(f"# ОБЩАЯ ТОЧНОСТЬ : {ACC:.4f}")
print(f"# ПРЕЦИЗИОННОСТЬ : {P:.4f}")
print(f"# ПОЛНОТА        : {R:.4f}")
print(f"# F1-МЕРА        : {F:.4f}")
print(f"# ROC AUC        : {ROC:.4f}")
print(f"{'#'*50}")