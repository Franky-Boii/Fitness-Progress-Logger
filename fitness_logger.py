from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "data/workouts.csv"


# -----------------------------
#  Ensure CSV exists
# -----------------------------
def ensure_data_file():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["date", "exercise", "sets", "reps", "weight"])
        df.to_csv(DATA_FILE, index=False)


#  Log a workout
def log_workout():
    date = datetime.now().strftime("%Y-%m-%d")
    exercise = input("Exercise name: ")
    sets = int(input("Number of sets: "))
    reps = int(input("Reps per set: "))
    weight = float(input("Weight used (kg): "))

    new_entry = {
        "date": date,
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight,
    }

    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    print("✅ Workout logged successfully!")


#  Weekly summary
def weekly_summary():
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])

    last_7_days = df[df["date"] >= datetime.now() - pd.Timedelta(days=7)]

    if last_7_days.empty:
        print("⚠️ No workouts in the last 7 days.")
        return

    print("\n📊 Weekly Workout Summary")
    print("-" * 30)
    print(f"Total workouts: {len(last_7_days)}")

    avg_weight = last_7_days.groupby("exercise")["weight"].mean().round(1)

    print("\nAverage Weight per Exercise:")
    for exercise, weight in avg_weight.items():
        print(f"- {exercise}: {weight} kg")


def generate_weekly_pdf():
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])

    last_7_days = df[df["date"] >= datetime.now() - pd.Timedelta(days=7)]

    if last_7_days.empty:
        print("⚠️ No data available for PDF report.")
        return

    if not os.path.exists("reports"):
        os.makedirs("reports")

    report_date = datetime.now().strftime("%Y-%m-%d")
    file_path = f"reports/weekly_report_{report_date}.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, 800, "Weekly Fitness Progress Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Report Date: {report_date}")
    c.drawString(50, 740, f"Workouts Logged: {len(last_7_days)}")

    # Average weight per exercise
    c.drawString(50, 700, "Average Weight per Exercise:")

    avg_weights = last_7_days.groupby("exercise")["weight"].mean().round(1)

    y_position = 670
    for exercise, weight in avg_weights.items():
        c.drawString(70, y_position, f"- {exercise}: {weight} kg")
        y_position -= 20

    c.save()

    print(f"📄 Weekly PDF report generated: {file_path}")


# Main menu
def main_menu():
    ensure_data_file()

    while True:
        print("\n🏋️ Fitness Progress Logger")
        print("1. Log new workout")
        print("2. View weekly summary")
        print("3. Generate weekly PDF report")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            log_workout()
        elif choice == "2":
            weekly_summary()
        elif choice == "3":
            generate_weekly_pdf()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main_menu()
