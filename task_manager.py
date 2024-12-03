import json
from datetime import datetime

class Task:
    def __init__(self, title, description, status="pending"):
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()  # Load existing tasks when starting

    def add_task(self):
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()
        print(f"\nTask '{title}' added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("\nNo tasks found!")
            return

        print("\nYour Tasks:")
        for i, task in enumerate(self.tasks, 1):
            status_symbol = "✓" if task.status == "completed" else "□"
            print(f"\n{i}. [{status_symbol}] {task.title}")
            print(f"   Description: {task.description}")
            print(f"   Status: {task.status}")
            print(f"   Created: {task.created_at}")

    def mark_complete(self):
        self.view_tasks()
        if not self.tasks:
            return
        
        try:
            task_num = int(input("\nEnter task number to mark as complete: ")) - 1
            if 0 <= task_num < len(self.tasks):
                self.tasks[task_num].status = "completed"
                self.save_tasks()
                print(f"\nTask '{self.tasks[task_num].title}' marked as complete!")
            else:
                print("\nInvalid task number!")
        except ValueError:
            print("\nPlease enter a valid number!")
 
    def delete_task(self):
        self.view_tasks()
        if not self.tasks:
            return
        
        try:
            task_num = int(input("\nEnter task number to delete: ")) - 1
            if 0 <= task_num < len(self.tasks):
                deleted_task = self.tasks.pop(task_num)
                self.save_tasks()
                print(f"\nTask '{deleted_task.title}' deleted!")
            else:
                print("\nInvalid task number!")
        except ValueError:
            print("\nPlease enter a valid number!")

    def save_tasks(self):
        """Save tasks to a JSON file"""
        with open('tasks.json', 'w') as f:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, f, indent=2)

    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            with open('tasks.json', 'r') as f:
                tasks_dict = json.load(f)
                self.tasks = [
                    Task(
                        task['title'],
                        task['description'],
                        task['status']
                    ) for task in tasks_dict
                ]
        except FileNotFoundError:
            self.tasks = []

def main():
    manager = TaskManager()
    
    while True:
        print("\n=== Task Manager ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            manager.add_task()
        elif choice == "2":
            manager.view_tasks()
        elif choice == "3":
            manager.mark_complete()
        elif choice == "4":
            manager.delete_task()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()