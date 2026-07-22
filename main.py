import json
from abc import ABC,abstractmethod
from pathlib import Path

database="school_data.json"
data={"students":[] , "teachers":[]}


if Path(database).exists():
    with open(database,"r") as f:
        content=f.read()
        if content:
            data=json.loads(content)


def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)

class Persons(ABC):
    
    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    

    @staticmethod
    def email_validation(email):
        if "@" in email and "." in email:
            return True
        
        else:
            return False

class student(Persons):

    def get_roles(self):
        return "student"
    
    def register(self):
        name=input("tell your name-->")
        age=int(input("tell age name-->"))
        email=input("tell your mail-->")
        roll_num=input("tell your roll number-->")

        if not Persons.email_validation(email):
            print("Invalid email")
            return
        
        for i in data['students']:
            if i['roll_num']==roll_num:
                print("student already exists ")
                return
            
        data ['students'].append({
            "name":name,
            "age":age,
            "email":email,
            "roll_num":roll_num,
            "grade":{}
        })
        save()
        print(f"student {name} registered")

    def show_details(self):
        roll_num=input("roll number-->")
        for i in data['students']:
            if i['roll_num']==roll_num:
                grades=i['grade']
                avg=sum(grades.values())/len(grades) if grades else 0

                print(f"\n name : {i['name']}")
                print(f"Roll_num : {i['roll_num']}")
                print(f"Grades : {grades}")
                print(f"Average : {avg}")
                return
        print("student not found")



    def add_grade(self):
        roll_num=input("tell your roll number-->")
        subject=input("Subject :")
        marks=float(input("Marks :"))

        for i in data['students']:
            if i["roll_num"]==roll_num:
                i['grade'][subject] = marks
                save()
                print("grade added successfully")
                return
            print("student not found")

class teacher(Persons):

    def get_roles(self):
        return "teacher"

    def register(self):
        name=input("tell your name-->")
        age=int(input("tell age name-->"))
        email=input("tell your mail-->")
        subject=input("tell your subject-->")
        empl_id=input("tell your id-->")

        if not Persons.email_validation(email):
            print("Invalid email")
            return

        for i in data['teachers']:
            if i['empl_id']==empl_id:
                print("teacher already exists ")
                return

        data ['teachers'].append({
            "name":name,
            "age":age,
            "email":email,
            "empl_id":empl_id,
            "subject":subject
        })
        save()
        print(f"teacher {name} registered")

    def show_details(self):
        empl_id=input("Employee ID-->")
        for i in data['teachers']:
            if i['empl_id']==empl_id:

                print(f"\n name : {i['name']}")
                print(f"Subject : {i['subject']}")
                print(f"Emp ID : {'empl_id'}")
                return
        print("teacher not found")


@abstractmethod
def show_details(self):
        pass
stud=student()
tech=teacher()

print("Press 1 to register a student")
print("Press 2 to register a teacher")
print("Press 3 to add grades to a student")
print("Press 4 to show a student details")
print("Press 5 to show a teacher details")

choice=int(input("choose from the desired options-->"))

if choice==1:
    stud.register()

elif choice==2:
    tech.register()

elif choice==3:
    stud.add_grade()

elif choice==4:
    stud.show_details()

elif choice==5:
    tech.show_details()