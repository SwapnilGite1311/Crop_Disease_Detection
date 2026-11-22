
import requests
import time
import os

def update_motor(value):
    """Update Blynk virtual pin V1 using BLYNK_AUTH_TOKEN from the environment."""
    token = os.getenv("BLYNK_AUTH_TOKEN")
    if not token:
        print("Set the BLYNK_AUTH_TOKEN environment variable before using the hardware controls.")
        return
    response = requests.get(
        "https://blynk.cloud/external/api/update",
        params={"token": token, "V1": value},
        timeout=15,
    )
    if response.status_code == 200:
        print("Motor updated.")
    else:
        print("Failed to update motor:", response.text)

def motor_on():
    """Locks the solenoid door by sending '1' to V1."""
    update_motor("1")

def motor_off():
    """Unlocks the solenoid door by sending '0' to V1."""
    update_motor("0")

def main():
    while True:
        print("\n1️⃣ Motor On\n2️⃣ Motor Off\n3️⃣ Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            motor_on()
        elif choice == "2":
            motor_off()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice! Try again.")

        time.sleep(1)  # Small delay to avoid API spamming

if __name__ == "__main__":
    main()
