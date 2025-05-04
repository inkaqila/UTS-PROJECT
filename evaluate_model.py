# import numpy as np
# from tensorflow.keras.models import load_model
# from sklearn.metrics import classification_report, confusion_matrix
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os

# def run(model_path="lstm_model.h5",
#         x_test_path="X_test.npy",
#         y_test_path="y_test.npy",
#         output_img="static/confusion_matrix.png"):

#     # 1. Load model
#     model = load_model(model_path)
#     print(f"✅ Loaded model dari `{model_path}`")

#     # 2. Load test data
#     X_test = np.load(x_test_path)
#     y_test = np.load(y_test_path)
#     print(f"✅ Loaded X_test ({X_test.shape}) dan y_test ({y_test.shape})")

#     # 3. Predict
#     y_pred_probs = model.predict(X_test)
#     y_pred = np.argmax(y_pred_probs, axis=1)

#     # 4. Report
#     target_names = ['Negatif', 'Netral', 'Positif']
#     print("\n=== Classification Report ===")
#     print(classification_report(y_test, y_pred, target_names=target_names))
#     print("=== Confusion Matrix ===")
#     cm = confusion_matrix(y_test, y_pred)
#     print(cm)

#     # 5. Simpan hasil evaluasi ke CSV
#     df = pd.DataFrame({
#         'actual': y_test,
#         'predicted': y_pred
#     })
#     df.to_csv("evaluation_results.csv", index=False)
#     print("✅ Hasil evaluasi disimpan di `evaluation_results.csv`")

#     # 6. Simpan Confusion Matrix sebagai gambar
#     os.makedirs(os.path.dirname(output_img), exist_ok=True)  # Pastikan folder static/ ada
#     plt.figure(figsize=(6, 5))
#     sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
#                 xticklabels=target_names, yticklabels=target_names)
#     plt.xlabel('Predicted Label')
#     plt.ylabel('True Label')
#     plt.title('Confusion Matrix')
#     plt.tight_layout()
#     plt.savefig(output_img)
#     plt.close()
#     print(f"✅ Confusion matrix disimpan di `{output_img}`")

# if __name__ == "__main__":
#     run()

import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run(model_path="lstm_model.h5",
        x_test_path="X_test.npy",
        y_test_path="y_test.npy",
        cm_img="static/confusion_matrix.png",
        report_csv="static/classification_report.csv"):

    # 1. Load model
    model = load_model(model_path)

    # 2. Load test data
    X_test = np.load(x_test_path)
    y_test = np.load(y_test_path)

    # 3. Predict
    y_pred = np.argmax(model.predict(X_test), axis=1)

    # 4. Classification Report sebagai dict
    target_names = ['Negatif','Netral','Positif']
    report_dict = classification_report(
        y_test, y_pred, target_names=target_names, output_dict=True
    )
    # 5. Simpan report ke CSV
    df_report = pd.DataFrame(report_dict).T.round(4)
    os.makedirs(os.path.dirname(report_csv), exist_ok=True)
    df_report.to_csv(report_csv)
    print(f"✅ Classification report disimpan di `{report_csv}`")

    # 6. Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    os.makedirs(os.path.dirname(cm_img), exist_ok=True)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=target_names, yticklabels=target_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig(cm_img)
    plt.close()
    print(f"✅ Confusion matrix disimpan di `{cm_img}`")

if __name__ == "__main__":
    run()

