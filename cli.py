import json


def add_student(students):
    while True:
        name = input("Enter name: ")
        if name =="":
            break

        id = input("Enter ID: ")
        marks = input("Enter marks: ")
        student = {"name": name, "ID": id, "marks": marks}

        students.append(student)
    for student in students:
        print(student)
def view_students(students):
    pass
def search_student(students, id):
    pass
def class_average(students):
    pass
import json


def save_students(students):
    with open("students.json", "w") as file:
        json.dump(students, file)



def load_students():
    try:
        with open("students.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError,json.JSONDecodeError):
        return []
students = load_students()
while True:
    print("1. Add student records")
    print("2. View all students")
    print("3. Search student by ID")
    print("4. Calculate class average")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_student(students)
        save_students(students)
    elif choice == "2":
        view_students(students)
    elif choice == "3":
        id = input("Enter ID to search: ")
        search_student(students, id)
    elif choice == "4":
        class_average(students)
    elif choice == "5":
        save_students(students)
        print(students)
        break
    else:
        print("Invalid choice")
