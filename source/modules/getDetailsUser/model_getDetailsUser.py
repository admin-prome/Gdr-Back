class UserDetails:
    def __init__(self, id, employee_number, full_name, email, branch, position, category, branch_zone, management):
        self.id = id
        self.employee_number = employee_number
        self.full_name = full_name.title()  
        self.email = email
        self.branch = branch.title()  
        self.position = position.title()  
        self.category = category.title()  
        self.branch_zone = branch_zone.title()  
        self.management = management.title()  

    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=json_data.get("id"),
            employee_number=json_data.get("employeeNumber"),
            full_name=json_data.get("fullName").title(),  
            email=json_data.get("email"),
            branch=json_data.get("branch").title(),  
            position=json_data.get("position").title(),  
            category=json_data.get("category").title(),  
            branch_zone=json_data.get("branchZone").title(),  
            management=json_data.get("management").title()  
        )

    def __str__(self):
        return f"UserDetails(id={self.id}, email={self.email}, full_name={self.full_name})"
