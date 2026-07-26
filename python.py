import random
import string

def check_password_strength(password):
    score = 0
    feedback = []
    
    # 1. Length Check
    if len(password) >= 12:
        score += 3
        feedback.append("✓ სიგრძე შესანიშნავია (12+ სიმბოლო)")
    elif len(password) >= 8:
        score += 1
        feedback.append("⚠ სიგრძე ნორმალურია, მაგრამ სასურველია 12+ სიმბოლო")
    else:
        feedback.append("✗ პაროლი ძალიან მოკლეა (მინიმუმ 8 სიმბოლო)")
        
    # 2. Check for Lowercase & Uppercase
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    if has_lower and has_upper:
        score += 2
        feedback.append("✓ შეიცავს დიდ და პატარა ასოებს")
    else:
        feedback.append("✗ გამოიყენეთ როგორც დიდი, ისე პატარა ასოები")
        
    # 3. Check for Numbers
    has_digit = any(c.isdigit() for c in password)
    if has_digit:
        score += 2
        feedback.append("✓ შეიცავს ციფრებს")
    else:
        feedback.append("✗ დაამატეთ ციფრები")
        
    # 4. Check for Special Symbols
    special_chars = string.punctuation
    has_special = any(c in special_chars for c in password)
    if has_special:
        score += 3
        feedback.append("✓ შეიცავს სპეციალურ სიმბოლოებს (!, @, #, და ა.შ.)")
    else:
        feedback.append("✗ დაამატეთ სპეციალური სიმბოლოები უსაფრთხოებისთვის")
        
    # Final Rating Calculation
    print("\n--- ანალიზის შედეგი ---")
    print(f"ჯამური ქულა: {score} / 10")
    
    if score >= 9:
        print("დონე: ძლიერი 🔒 (უსაფრთხოა)")
    elif score >= 6:
        print("დონე: საშუალო ⚠️ (შესაძლებელია გაუმჯობესება)")
    else:
        print("დონე: სუსტი ❌ (იოლია გასატეხად)")
        
    print("\nდეტალური რჩევები:")
    for item in feedback:
        print(f" - {item}")

def generate_secure_password():
    length = int(input("\nშეიყვანეთ სასურველი სიგრძე (მინიმუმ 10): "))
    if length < 8:
        length = 8
        
    # Combine letters, digits, and punctuation
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate random password
    secure_password = "".join(random.choice(characters) for _ in range(length))
    print(f"\nგენერირებული პაროლი: {secure_password}")

# Main Program Loop
while True:
    print("\n=== უსაფრთხოების მთავარი მენიუ ===")
    print("1. პაროლის სიძლიერის შემოწმება")
    print("2. ძლიერი პაროლის გენერაცია")
    print("3. გასვლა")
    
    choice = input("აირჩიეთ მოქმედება (1-3): ")
    
    if choice == '1':
        user_pass = input("\nშეიყვანეთ შესამოწმებელი პაროლი: ")
        check_password_strength(user_pass)
    elif choice == '2':
        generate_secure_password()
    elif choice == '3':
        print("პროგრამა დასრულდა.")
        break
    else:
        print("არასწორი არჩევანი, სცადეთ თავიდან.")
        
