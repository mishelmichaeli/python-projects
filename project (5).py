import pickle
import random
from beautifultable import BeautifulTable
import matplotlib.pyplot as plt

# hello, you are the manager of Beinleumi Bank!
# as a bank we save our customer's money
# as a manager, you can conduct all of your employees and customers
# and you can see some statistics of your bank
# have fun!

MAIN_MENU = """You are the manager,
Please choose your action:
    1 - Conduct employees
    2 - Conduct customers
    3 - Watch KPI'S
    0 - finish
    Your answer: """

EMPLOYEES_MENU = """Please choose your action:
    1 - Check in employee
    2 - Get employee details
    3 - Change employee password
    4 - Delete employee
    5 - print employee list
    0 - finish
    Your answer: """

CUSTOMERS_MENU = """Please choose your action:
    1 - Check in customer
    2 - Get customer details
    3 - Change customer balance
    4 - Delete customer
    5 - print customer list
    0 - finish
    Your answer: """

KPI_MENU = """Please choose your KPI:
    1 - Employee's Female to Male Ratio
    2 - Employee's Satisfaction
    3 - Customer's churn rate
    0 - finish
    Your answer: """

# static files objects.
EMPLOYEES_FILE = 'employees.txt'
CUSTOMERS_FILE = 'costumers.dat'
SATISFACTION_FILE = 'satisfaction.dat'
CUSTOMERS_COUNTER_FILE = 'customer_counter.dat'
CHURN_COUNTER_FILE = 'churn_counter.dat'

# the target KPI'S
SATISFACTION_KPI = 4.3
CHURN_KPI = 0.68

# counter for operations the user do in the system
counter_operation = 0


def main():
    try:
        # this is the main func which show the main menu
        print('*** WELCOME to Beinleumi Bank! ***')
        action = int(input(MAIN_MENU))
        # sends to each relevant func
        while action != 0:
            if action == 1:
                employees()
            elif action == 2:
                customers()
            elif action == 3:
                statistics()

            action = int(input(MAIN_MENU))

        print('Total actions made this time: ' + str(counter_operation))
        print('Thank you, bye bye')
    except ValueError:
        print('Error: please enter a valid number from the menu')
        main()


def employees():
    # this is the main func of the employees
    try:
        # create file if not exist
        infile = open(EMPLOYEES_FILE, 'a')
        # read from file to list
        infile = open(EMPLOYEES_FILE, 'r')
        employees_list = infile.readlines()
        infile.close()

        # strip the \n from each element
        index = 0
        while index < len(employees_list):
            employees_list[index] = employees_list[index].rstrip('\n')
            index += 1

        action = int(input(EMPLOYEES_MENU))

        # sends to each relevant func
        while action != 0:
            if action == 1:
                check_in_employee(employees_list)
            elif action == 2:
                get_details_employee(employees_list)
            elif action == 3:
                change_password_employee(employees_list)
            elif action == 4:
                delete_employee(employees_list)
            elif action == 5:
                print_employees(employees_list)

            action = int(input(EMPLOYEES_MENU))

        # write the list to the file
        infile = open(EMPLOYEES_FILE, 'w')
        for item in employees_list:
            infile.write(item + '\n')
        infile.close()
    except ValueError:
        print('Error: please enter a valid number from the menu')
    except UnboundLocalError:
        print("Error: there's not enough data")


def check_in_employee(employees_list):
    # check in employee to the system
    global counter_operation
    try:
        id_num = input('Enter employee ID (8 number): ')
        # id input validation check
        while not id_num.isdigit() or len(id_num) != 8:
            id_num = input('ID num must have 8 digits only, try again: ')
        # check if id is available
        id_available = check_available(employees_list, id_num, 0)
        while not id_available:
            id_num = input('The ID is taken, please enter a new id number: ')
            id_available = check_available(employees_list, id_num, 0)
        # get name
        name = input('Enter employee name:')
        # input validation for name
        while not name.isalpha():
            name = input('Name must have letters only and no spaces: ')
        # get gender
        choose = int(input('''Enter employee gender:
        1 - Male
        2 - Female
        your answer: '''))
        if choose != 1 and choose != 2:
            choose = int(input('''Please choose between these two options:
        1 - Male
        2 - Female
        your answer: '''))
        if choose == 1:
            gender = 'male'
        elif choose == 2:
            gender = 'female'
        # get phone
        phone = input('Enter employee phone:')
        # check phone input validation
        while not phone.isdigit():
            phone = input('Phone number must have digits only, try again: ')
        # get password
        new_password = input('Enter employee password (must have big letter and numbers, min 7): ')
        # checks if the password by the rules
        password_available = check_password(new_password)
        while not password_available:
            new_password = input('Incorrect password, enter a new one. Hint: Follow the rules: ')
            password_available = check_password(new_password)

        # write to the list
        employees_list.append(id_num)
        employees_list.append(name)
        employees_list.append(gender)
        employees_list.append(phone)
        employees_list.append(new_password)

        # add global operation counter
        counter_operation = counter_operation + 1
        print("The employee was added successfully")
    # checks if there's no errors
    except ValueError:
        print('Error: There was a value error')
    except FileNotFoundError:
        print('Error: File not found')


def get_details_employee(employees_list):
    # this func prints details of employee by his id.
    global counter_operation
    try:
        # get the id of the employee
        search = input('Which employee would you like to get details by ID number?: ')
        # search for item on the list and get index
        id_index = employees_list.index(search)

        # get details from list
        name = employees_list[id_index + 1]
        gender = employees_list[id_index + 2]
        phone = employees_list[id_index + 3]
        password = employees_list[id_index + 4]
        # print details
        print('ID Number:' + search)
        print('Name:' + name)
        print('Gender:' + gender)
        print('Phone Number:' + phone)
        print('Password Number:' + password)

        # add global operation counter
        counter_operation = counter_operation + 1
    # checks if there's no value error
    except ValueError:
        print('Error: there is a value error or the employee not found')
    except FileNotFoundError:
        print('Error: File not found')


def check_available(employees_list, num, line):
    # this func check if the value is already exist
    # by parameter (line) as: 0=id, 1=name, 2=gender, 3=phone, 4=password
    try:
        available = True
        # checks if the value exist in his parameter lines
        while line < len(employees_list):
            list_line = employees_list[line]
            if list_line == num:
                available = False
            line += 5

        # return if available
        return available
    except FileNotFoundError:
        print('Error: File not found')


def delete_employee(employees_list):
    # this func delete employee from the system
    global counter_operation
    try:
        # get the id of the employee
        search = input('Which employee would you like to delete by ID number?: ')
        # search for item on the list and get index
        id_index = employees_list.index(search)
        # delete the employee
        for x in range(5):
            del employees_list[id_index]

        # add global operation counter
        counter_operation = counter_operation + 1
    except ValueError:
        print('Error: Employee not found')
    except FileNotFoundError:
        print('Error: File not found')
    else:
        print('The employee had been deleted')


def change_password_employee(employees_list):
    # this func changes the password of a employee by his id
    global counter_operation
    try:
        # get the id of the employee
        search = input('Which employee would you like to change password by ID number?: ')
        # search for item on the list and get index
        id_index = employees_list.index(search)
        # get the new password
        new_password = input('Enter a new employee password (must have big letter and numbers, 7 min): ')
        # checks if the password by the rules
        password_available = check_password(new_password)
        while not password_available:
            new_password = input('Incorrect password, enter a new one: ')
            password_available = check_password(new_password)
        # change to a new password
        employees_list[id_index + 4] = new_password

        # add global operation counter
        counter_operation = counter_operation + 1
    except ValueError:
        print('Error: Employee not found')
    except FileNotFoundError:
        print('Error: File not found')
    else:
        print('The password has been changed')


def check_password(password):
    # this func check if the password is by the rules.
    # flag for password verification
    available = False
    # checks if a least 7 char
    if len(password) < 7:
        return False
    # checks if the password has a least one num or one letter
    if not password.isalnum():
        return False
    # checks if there is at least one upper-case letter
    uppercase_flag = False
    for c in password:
        if c.isupper():
            uppercase_flag = True
    # checks if there is at least one digit char
    digit_flag = False
    for c in password:
        if c.isdigit():
            digit_flag = True

    if uppercase_flag is True and digit_flag is True:
        available = True
    # return if available
    return available


def print_employees(employees_list):
    # this func prints all employees beautifully
    global counter_operation
    try:
        table = BeautifulTable()
        table.column_headers = ["ID", "Name", "Gender", "Phone", "Password"]
        for line in range(0, len(employees_list), 5):
            table.append_row([employees_list[line], employees_list[line+1],
                              employees_list[line+2], employees_list[line+3],
                              employees_list[line+4]])
        print(table)
        # add global operation counter
        counter_operation = counter_operation + 1
    except ValueError:
        print('Error: error')


def customers():
    # this is the main func of customers
    try:
        try:
            # read from file to list
            input_file = open(CUSTOMERS_FILE, 'rb')
            customers_dic = pickle.load(input_file)
            input_file.close()
        except OSError:
            # open if not exist
            input_file = open(CUSTOMERS_FILE, 'wb')
        except (EOFError, UnboundLocalError):
            # create dictionary if not exist
            customers_dic = {}

        action = int(input(CUSTOMERS_MENU))

        # sends to each relevant func
        while action != 0:
            if action == 1:
                check_in_customer(customers_dic)
            elif action == 2:
                get_details_customer(customers_dic)
            elif action == 3:
                change_balance_customer(customers_dic)
            elif action == 4:
                delete_customer(customers_dic)
            elif action == 5:
                print_customer(customers_dic)

            action = int(input(CUSTOMERS_MENU))

        # write to pickle file the dic data
        output_file = open(CUSTOMERS_FILE, 'wb')
        pickle.dump(customers_dic, output_file)
        output_file.close()
    except ValueError:
        print('Error: Please enter a valid number from the menu')
    except UnboundLocalError:
        print("Error: There's not enough data")


def check_in_customer(customers_dic):
    # this func checks in a customer
    global counter_operation
    try:
        # get id
        id_num = input('Enter costumer ID ( 8 digits): ')
        # check id input validation
        while not id_num.isdigit() or len(id_num) != 8:
            id_num = input('ID num must have 8 digits only, try again: ')
        # check if id is available
        id_available = check_id_customer(id_num, customers_dic)
        while not id_available:
            id_num = input('The id is taken, enter a new id number')
            id_available = check_id_customer(id_num, customers_dic)
        # get name
        name = input('Enter costumer name:')
        # input validation for name
        while not name.isalpha():
            name = input('Name must have letters only and no space: ')
        # get address
        address = input('Enter costumer address:')
        # get phone
        phone = input('Enter costumer phone:')
        # check phone input validation
        while not phone.isdigit():
            phone = input('Phone number must have digits only, try again: ')
        # get password
        new_password = make_password_customer(id_num)
        # get balance
        balance = input('Enter costumer balance:')
        # balance input validation
        while not balance.isdigit():
            balance = input('Balance number must have digits only, try again: ')

        # write to the dictionary
        customers_dic.update({id_num: {'name': name, 'address': address, 'phone': phone,
                                       'password': new_password, 'balance': balance}})
        print('Customer added successfully')

        # increase customer counter by 1
        add_to_customer_counter(1)
        # add global operation counter
        counter_operation = counter_operation + 1
    # checks if there's no value error
    except ValueError:
        print('Error: there was a value error')
    except FileNotFoundError:
        print('Error: File not found')


def get_details_customer(customers_dic):
    # this func prints details of customer by his id.
    global counter_operation
    try:
        # get the id of the customer
        id_num = input('Which costumer would you like to get details by ID number?: ')
        print(customers_dic[id_num])

        # add global operation counter
        counter_operation = counter_operation + 1
    except KeyError:
        print('Error: Costumer not found')


def delete_customer(customers_dic):
    # this func deletes details of customer by his id.
    global counter_operation
    try:
        # get the id of the customer
        id_num = input('Which costumer would you like to delete by ID number?: ')
        del customers_dic[id_num]
        print('Costumer deleted properly')
    except ValueError:
        print('There was an error, try again')
    except KeyError:
        print('Error: Customer not found')
    else:
        # increase leaving counter by 1
        add_to_churn_counter(1)
        # add global operation counter
        counter_operation = counter_operation + 1


def change_balance_customer(customers_dic):
    # this func change customer's balance by his id
    global counter_operation
    try:
        # get the id of the customer
        id_num = input('Which customer would you like to change balance by ID number?: ')
        # choose action to do on the balance
        choose = int(input('''What would you like to do?
    1 - Deposit money
    2 - Withdraw money
    your answer: '''))
        if choose != 1 and choose != 2:
            choose = int(input('''Please choose between these two options:
    1 - Deposit money
    2 - Withdraw money
    your answer: '''))
        amount = input('''How much?
    your answer: ''')
        # amount input validation
        while not amount.isdigit():
            amount = input('Amount must have digits only, try again: ')
        # get the customer balance
        costumer_balance = int(customers_dic[id_num]['balance'])
        # do action
        if choose == 1:
            costumer_balance += int(amount)
        elif choose == 2:
            costumer_balance -= int(amount)
        # change the customer balance
        customers_dic[id_num]['balance'] = str(costumer_balance)

        # add global operation counter
        counter_operation = counter_operation + 1
        print('Costumers balance changed properly')
    except ValueError:
        print('Error: There was an error, try again')
    except KeyError:
        print('Error: Customer not found')


def check_id_customer(id_num, customers_dic):
    # this func checks if the customer's id is not taken
    try:
        available = True
        # checks if the value exist in his parameter lines
        if id_num in customers_dic.keys():
            available = False
        # return if available
        return available
    except ValueError:
        print('Error: There was an error, try again')


def make_password_customer(id_num):
    # this func make customer password
    # by first 4 digit from id number + 4 random digits
    password = random.randint(10, 9999) + (int(id_num) // 10000) * 10000
    return password


def print_customer(customers_dic):
    # this func prints all customers
    global counter_operation
    try:
        table = BeautifulTable()
        table.column_headers = ["ID", "Name", "Address", "Phone", "Password", "Balance"]
        for key in customers_dic.keys():
            table.append_row([key, customers_dic[key]['name'],
                              customers_dic[key]['address'], customers_dic[key]['phone'],
                              customers_dic[key]['password'], customers_dic[key]['balance']])
        print(table)

        # add global operation counter
        counter_operation = counter_operation + 1
    except ValueError:
        print('Error: error')
    except UnboundLocalError:
        print("Error: There's no data to show")


def add_to_customer_counter(action):
    # this func add 1 to customer's counter
    # or return the counter, depends on the action
    customers_counter = 0
    try:
        # read from file to list
        input_file = open(CUSTOMERS_COUNTER_FILE, 'rb')
        customers_counter = pickle.load(input_file)
        input_file.close()
    except OSError:
        # open if not exist
        input_file = open(CUSTOMERS_COUNTER_FILE, 'wb')
    except EOFError:
        # create object if not exist
        customers_counter = 0

    if action == 1:
        customers_counter = customers_counter + 1
        # write the object to pickle file
        output_file = open(CUSTOMERS_COUNTER_FILE, 'wb')
        pickle.dump(customers_counter, output_file)
        output_file.close()

    elif action == 2:
        return customers_counter


def add_to_churn_counter(action):
    # this func add 1 to customer's churn counter
    # or return the counter, depends on the action
    churn_counter = 0
    try:
        # read from file to list
        input_file = open(CHURN_COUNTER_FILE, 'rb')
        churn_counter = pickle.load(input_file)
        input_file.close()
    except OSError:
        # open if not exist
        input_file = open(CHURN_COUNTER_FILE, 'wb')
    except EOFError:
        # create object if not exist
        churn_counter = 0

    if action == 1:
        churn_counter = churn_counter + 1
        # write the object to pickle file
        output_file = open(CHURN_COUNTER_FILE, 'wb')
        pickle.dump(churn_counter, output_file)
        output_file.close()

    elif action == 2:
        return churn_counter


def statistics():
    # shows the kpi menu
    try:
        action = int(input(KPI_MENU))
        # sends to each relevant func
        while action != 0:
            if action == 1:
                gender_statics()
            elif action == 2:
                satisfaction_statistic()
            elif action == 3:
                churn_statistic()

            action = int(input(KPI_MENU))
    except ValueError:
        print('Error: Please enter a valid number from the menu')


def satisfaction_statistic():
    # this func shows the employees satisfaction kpi
    # https://www.datapine.com/kpi-examples-and-templates/finance
    global counter_operation
    try:
        satisfaction_list = []
        try:
            # read from file to list
            input_file = open(SATISFACTION_FILE, 'rb')
            satisfaction_list = pickle.load(input_file)
            input_file.close()
        except OSError:
            # open if not exist
            input_file = open(SATISFACTION_FILE, 'wb')
        except EOFError:
            # create dictionary if not exist
            satisfaction_list = []

        try:
            # read from file to list
            infile = open(EMPLOYEES_FILE, 'r')
            employees_list = infile.readlines()
            infile.close()

            # strip the \n from each element
            index = 0
            while index < len(employees_list):
                employees_list[index] = employees_list[index].rstrip('\n')
                index += 1

        except FileNotFoundError:
            print('Error: File not found, you dont have employees')
        try:
            choose = int(input("""Welcome to the daily employees's satisfaction data!
             What would you like to do?
             1 - Insert daily employees's satisfaction survey
             2 - Watch existing data
             Your answer: """))
            # input validation
            if choose != 1 and choose != 2:
                choose = int(input("""Please choose between these two options:
                     1 - Insert daily employees's satisfaction survey
                     2 - Watch existing data
                     Your answer: """))

            # insert satisfaction data for each employee
            if choose == 1:
                for index in range(0, len(employees_list), 5):
                    grade = int(input(f"Enter {employees_list[index+1]} employee satisfaction (1-5): "))
                    # input validation
                    while not (0 < grade < 6):
                        grade = int(input(f"Error: Enter {employees_list[index + 1]} employee satisfaction (1-5): "))
                    # add to satisfaction list
                    satisfaction_list.append(grade)

            # show data
            elif choose == 2:
                # calculate the satisfaction statistics
                counter1 = counter2 = counter3 = counter4 = counter5 = sum_grade = 0
                for index in range(len(satisfaction_list)):
                    sum_grade += satisfaction_list[index]
                    if satisfaction_list[index] == 1:
                        counter1 += 1
                    elif satisfaction_list[index] == 2:
                        counter2 += 1
                    elif satisfaction_list[index] == 3:
                        counter3 += 1
                    elif satisfaction_list[index] == 4:
                        counter4 += 1
                    elif satisfaction_list[index] == 5:
                        counter5 += 1

                plt.title("Employee Satisfaction\n" +
                          "The KPI is " + str(round(sum_grade / (len(satisfaction_list)), 2)) +
                          "\nThe minimun target KPI is " + str(SATISFACTION_KPI))

                # create a list of values
                values = [counter1, counter2, counter3, counter4, counter5]
                # create a tuple of labels
                values_labels = ('Very Dissatisfied (' + str(values[0]) + ')',
                                'Dissatisfied (' + str(values[1]) + ')',
                                'OK (' + str(values[2]) + ')',
                                'Satisfied (' + str(values[3]) + ')',
                                'Very Satisfied (' + str(values[4]) + ')')
                # add colors
                colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'pink']
                # create a pie chart from the values
                plt.pie(values, labels=values_labels, autopct='%1.1f%%',
                        colors=colors, shadow=True, startangle=90)
                # add side labels
                plt.legend(values_labels, loc='lower center', fontsize='x-small')
                # display the pie chart
                plt.show()
            # add global operation counter
            counter_operation = counter_operation + 1
            # write to pickle file the list data
            output_file = open(SATISFACTION_FILE, 'wb')
            pickle.dump(satisfaction_list, output_file)
            output_file.close()
        except UnboundLocalError:
            print("Error: there's not enough data")
    except ZeroDivisionError:
        print("Error: There's not enough data")
    except ValueError:
        print("Error: A value error accrued")


def churn_statistic():
    # this func shows the customers churn rate kpi
    # https://www.datapine.com/kpi-examples-and-templates/sales
    global counter_operation
    try:
        # get counters
        counter_total_leaving = add_to_churn_counter(2)
        counter_total_customers = add_to_customer_counter(2)
        # calculate the leaving percentage
        percentage = counter_total_leaving / counter_total_customers * 100
        # calculate the kpi by the company rules
        churn_kpi = round((1-(counter_total_leaving / counter_total_customers)), 2)

        plt.title("Churn Statistics\n" +
                  "The KPI is " + str(churn_kpi) +
                  "\nThe minimum KPI needed is " + str(CHURN_KPI))

        # create a list of values
        values = [counter_total_leaving, counter_total_customers]
        # create a tuple of labels
        values_labels = ('Total leaving customers (' + str(values[0]) + ')',
                         'Total customers registration (' + str(values[1]) + ')')
        # add colors
        colors = ['pink', 'purple', 'lightskyblue', 'lightcoral']
        # create a pie chart from the values
        plt.pie(values, labels=values_labels, autopct='%1.1f%%',
                colors=colors, shadow=True, startangle=90)
        # add side labels
        plt.legend(values_labels, loc='lower right')
        # display the pie chart
        plt.show()
        # add global operation counter
        counter_operation = counter_operation + 1
    except ZeroDivisionError:
        print("Error: There's not enough data")
    except ValueError:
        print("Error: A value error accrued")


def gender_statics():
    # this func shows the female to male ratio rate kpi
    # https://www.datapine.com/kpi-examples-and-templates/human-resources\
    global counter_operation
    try:
        # create file if not exist
        infile = open(EMPLOYEES_FILE, 'a')
        # read from file to list
        infile = open(EMPLOYEES_FILE, 'r')
        employees_list = infile.readlines()
        infile.close()

        # count how much male & female from employees list
        male_counter = female_counter = 0
        for index in range(2, len(employees_list), 5):
            gender = employees_list[index].rstrip('\n')
            if gender == 'male':
                male_counter += 1
            elif gender == 'female':
                female_counter += 1

        # make plt title
        plt.title("Female to Male Ratio")
        # create a list of values
        values = [male_counter, female_counter]
        # create a tuple of labels
        values_labels = ('Male (' + str(values[0]) + ')',
                         'Female (' + str(values[1]) + ')')
        # add colors
        colors = ['blue', 'pink']
        # create a pie chart from the values
        plt.pie(values, labels=values_labels, autopct='%1.1f%%',
                colors=colors, shadow=True, startangle=90)
        # add side labels
        plt.legend(values_labels)
        # display the pie chart
        plt.show()
        # add global operation counter
        counter_operation = counter_operation + 1
    except ValueError:
        print('Error: Please enter a valid number from the menu')


# thank u for reading!
# call the main func
main()
