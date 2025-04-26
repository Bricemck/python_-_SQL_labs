import psycopg2
# Imports the PostgreSQL so that we can interact with our Postgre databases
connection = psycopg2.connect(
    database="crm_tool"
) #Establishes connection to the database.
# I made this in Postgre and pre-populated 3 companies with a few employees in each.
cursor = connection.cursor() #cursor objects execute SQL commands through the connection.


print('Welcome to Big Brother CRM... Please select the actions that will assist in your thought policing')
#greeting when app launches... I give up on the Big brother theme around updates.

terminate_program = False
#A flag to control the main loop; I wish I figured this out back in the CYOA lab.

while terminate_program is False: #main loop
    print('\n[C]reate [V]iew [U]pdate [D]elete [Q]uit')
    user_input = input('User Action: ').capitalize()
    #prompts the user to choose between the CRUD options & quit.
    if user_input == 'C':
        print('Adding another cog to the corporate machine...')
        
        create_choice = input('Do you wish to create a [C]ompany or an [E]mployee? ').capitalize()
        #choosing between Company or Employee.
        if create_choice == 'C': #prompts for company info.
            name = input('Enter company name: ')
            industry = input('Enter industry: ')
            founded_year = input('Enter founding year: ')
            headquarters = input('Enter company headquarters location: ')

            #Inserts a Postgre command using the company schema.
            cursor.execute("INSERT INTO COMPANIES (name, industry, founded_year, headquarters)" \
            "VALUES (%s, %s, %s, %s);", (name, industry, founded_year, headquarters))

            connection.commit() #confirms success with a f literal string that updates dynamically.
            print(f'Company "{name}" established with base at {headquarters}.')
            continue
        
        #a lot of the same stuff but for employees.
        elif create_choice == 'E':
            first_name = input('Enter first name: ')
            last_name = input('Enter last name: ')
            email = input('Enter email (optional): ')  # Optional
            position = input('Enter position (optional): ')  # Optional
            salary = input('Enter salary (optional, e.g., 50000.00): ')  # Optional

    # Checks whether variable salary is truthy, (basically not an empty string).
    # This is important because salary expects salary to be numeric(10, 2), which cooresponds to a decimal in Python.
    # Basically we're ensuring compatibility.
            if salary:
                salary = float(salary)
                #And here we're catching empty strings.
            else:
                salary = None

    # If email is provided, ensure it’s unique, else set to None
            if not email:
                email = None
    #companies and employees are connected under company_id
            company_id = input('Enter company ID they serve under: ')
    #Another Postgre insertion to add an employee.
            cursor.execute("""
                INSERT INTO EMPLOYEES (first_name, last_name, email, position, salary, company_id)
                VALUES (%s, %s, %s, %s, %s, %s);
                """, (first_name, last_name, email, position, salary, company_id))

            connection.commit()#
            #success message.
            print(f'Employee {first_name} {last_name} successfully added with position {position}.')
            
    elif user_input == 'V':
        print('Peering into the ministry of company records') 
        view_choice = input('Do you wish to know the dark details of [C]ompanies or [E]mployees?').capitalize()
        if view_choice == 'C':
            cursor.execute("SELECT * FROM COMPANIES;")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print('My dark magic reacheth not that far.')
        elif view_choice == 'E':
            print('\nWhich company’s minions do you wish to inspect?')
            print('[1] Dewie Cheatem & Howe')
            print('[2] Dark Abyss Media')
            print('[3] Globo Corp')
            print('[A] All Employees')
            company_choice = input('Make your selection: ').capitalize()

            query = None

            # for company in companies:
            #     print(f"[{company[0]}] {company[1]} {company[2]}")

            if company_choice == '1':
                query = "SELECT * FROM EMPLOYEES WHERE company_id = 1;"
            elif company_choice == '2':
                query = "SELECT * FROM EMPLOYEES WHERE company_id = 2;"
            elif company_choice == '3':
                query = "SELECT * FROM EMPLOYEES WHERE company_id = 3;"
            elif company_choice == 'A':
                query = "SELECT * FROM EMPLOYEES;"
            else:
                print('Big Brother frowns upon your indecisiveness.')
            
            if query: 
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        print(row)
            continue  
    elif user_input == 'U':
        print("update stuff... I'm too tired to keep up the dystopian stuff")

        update_choice = input('Do you wish to update a [C]ompany or an [E]mployee? ').capitalize()

        if update_choice == 'C':
            cursor.execute("SELECT id, name FROM COMPANIES;")
            companies = cursor.fetchall()
            print('\n All Companies:')
            for company in companies:
                print(f"[{company[0]}] {company[1]}")

            company_id = input('Enter the company ID you wish to update: ')
            new_name = input('Enter the new company name (leave blank to keep current): ')
            new_industry = input('Enter the new industry (leave blank to keep current): ')
            new_founding_year = input('Enter the new founding year (leave blank to keep current): ')
            new_headquarters = input('Enter the new headquarters location (leave blank to keep current): ')

            query = "UPDATE COMPANIES SET "
            values = []

            if new_name:
                query += "name = %s,"
                values.append(new_name)
            if new_industry:
                query += "industry = %s, "
                values.append(new_industry)
            if new_founding_year:
                query += "founding_year = %s, "
                values.append(new_founding_year)
            if new_headquarters:
                query += "headquarters = %s, "
                values.append(new_headquarters)
            
            query = query.rstrip(', ')
            query += " WHERE id = %s;"
            values.append(company_id)

            cursor.execute(query, tuple(values))
            connection.commit()
            print(f"Company ID {company_id} updated successfully.")

        elif update_choice == 'E':
            cursor.execute("SELECT id, first_name, last_name FROM EMPLOYEES;")
            employees = cursor.fetchall()
            print("\nAvailable employees:")
            for employee in employees:
                print(f"[{employee[0]}] {employee[1]} {employee[2]}")

            employee_id = input('Enter the employee ID you wish to update: ')

            new_first_name = input('Enter the new first name (leave blank to keep current): ')
            new_last_name = input('Enter the new last name (leave blank to keep current): ')
            new_email = input('Enter the new email (leave blank to keep current): ')
            new_position = input('Enter the new position (leave blank to keep current): ')
            new_salary = input('Enter the new salary (leave blank to keep current): ')

            query = "UPDATE EMPLOYEES SET "
            values = []

            if new_first_name:
                query += "first_name = %s, "
                values.append(new_first_name)
            if new_last_name:
                query += "last_name = %s, "
                values.append(new_last_name)
            if new_email:
                query += "email = %s, "
                values.append(new_email)
            if new_position:
                query += "position = %s, "
                values.append(new_position)
            if new_salary:
                query += "salary = %s, "
                values.append(new_salary)
            
            query = query.rstrip(', ')

            query += "WHERE id = %s;"
            values.append(employee_id)

            cursor.execute(query, tuple(values))
            connection.commit()
            print(f"Employee ID {employee_id} updated successfully.")

        else:
            print('Invalid choice. Update operation aborted.')

            continue
    elif user_input == 'D':
        print('You have chosen... erasure.')

        delete_choice = input('Delete a [C]ompany or an [E]mployee? ').capitalize()

        if delete_choice == 'C':
            # List companies
            cursor.execute("SELECT id, name FROM COMPANIES;")
            companies = cursor.fetchall()
            print("\nAvailable companies:")
            for company in companies:
                print(f"[{company[0]}] {company[1]}")

            company_id = input('Enter the ID of the company to delete: ')
            confirm = input(f'Are you sure you want to DELETE company ID {company_id}? This will remove all associated employees too. (Y/N): ').capitalize()

            if confirm == 'Y':
                cursor.execute("DELETE FROM EMPLOYEES WHERE company_id = %s;", (company_id,))
                cursor.execute("DELETE FROM COMPANIES WHERE id = %s;", (company_id,))
                connection.commit()
                print(f"Company ID {company_id} and its employees have been purged.")
            else:
                print("Deletion aborted. Big Brother appreciates your restraint.")

        elif delete_choice == 'E':
            # List employees
            cursor.execute("SELECT id, first_name, last_name FROM EMPLOYEES;")
            employees = cursor.fetchall()
            print("\nAvailable employees:")
            for emp in employees:
                print(f"[{emp[0]}] {emp[1]} {emp[2]}")

            employee_id = input('Enter the ID of the employee to delete: ')
            confirm = input(f'Confirm deletion of employee ID {employee_id}? (Y/N): ').capitalize()

            if confirm == 'Y':
                cursor.execute("DELETE FROM EMPLOYEES WHERE id = %s;", (employee_id,))
                connection.commit()
                print(f"Employee ID {employee_id} has been unpersoned.")
            else:
                print("Employee survives another cycle.")

        else:
            print('Invalid option. No deletion performed.')

        continue
    
    elif user_input == 'Q':
        print('peace homie')
        terminate_program = True
    else:
        print('Big Brother is not pleased. Try a valid option.')


    continue
# close connection
cursor.close()
connection.close()