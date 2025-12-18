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


# Main menu
def main_menu():
    ensure_data_file()

    while True:
        print("\n🏋️ Fitness Progress Logger")
        print("1. Log new workout")
        print("2. View weekly summary")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            log_workout()
        elif choice == "2":
            weekly_summary()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main_menu()
