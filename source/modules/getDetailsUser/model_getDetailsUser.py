class UserDetails:
    def __init__(self, id, employee_number, full_name, email, branch, position, category, branch_zone, management):
        self.id = id
        self.employee_number = employee_number
        self.full_name = full_name
        self.email = email
        self.branch = branch
        self.position = position
        self.category = category
        self.branch_zone = branch_zone 
        self.management = management

    @classmethod
    def from_json(cls, json_data):
        print(json_data)
        json_data = json_data['userDetails']
        print(type(json_data))
        rtaJson= cls(
            id=json_data.get("id"),
            employee_number=json_data.get("employeeNumber"),
            full_name=json_data.get("fullName"),  
            email=json_data.get("email"),
            branch=json_data.get("branch"),  
            position=json_data.get("position"),  
            category=json_data.get("category"),  
            branch_zone=json_data.get("branchZone"),  
            management=json_data.get("management")  
        )
        print(rtaJson)
        return rtaJson

    def __str__(self):
        return f"UserDetails(id={self.id}, email={self.email}, full_name={self.full_name})"
